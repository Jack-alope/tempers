"""
Router for analysis
"""
import json
import io
import logging
from typing import Optional

from fastapi import APIRouter,  Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse

from sqlalchemy.orm import Session

from database import get_db
from schemas import schema_analysis
from crud import crud_video, crud_tissue_tracking, crud_tissue_caculations, crud_tissue
from analysis.tissues import TissuePoints

import models

router = APIRouter()


@router.get('/analyze', tags=["analyze"])
async def analyze(video_id: Optional[int] = Query(None),
                  database: Session = Depends(get_db)):
    """Sets up the graphing areas and initally plots raw data"""

    json_list = []
    tiss_nums = []
    tiss_freq = []
    tiss_types = []

    video_object = crud_video.get_vid_by_id(database, video_id)
    tissues = video_object.tissues

    for tissue_object in tissues:
        tiss_freq.append(video_object.frequency)
        tiss_types.append(tissue_object.tissue_type)
        tiss_nums.append(tissue_object.tissue_number)

        data = crud_tissue_tracking.get_tracking_by_id(
            database, tissue_object.id)

        # TODO: Change this is js not here
        data['disp'] = data['displacement']
        json_list.append(data.to_json(orient='columns'))

    json_list = json.dumps(json_list)

    res = jsonable_encoder({'json_data_list': json_list,
                            'nums': tiss_nums, 'freqs': tiss_freq, 'types': tiss_types})

    return JSONResponse(content=res)


@router.get('/analyze/tissue_number', tags=["analyze"])
async def analyze_tissue_number(tissue_number: int = Query(...),
                                experiment_id: str = Query(...),
                                date_recorded: str = Query(None),
                                database: Session = Depends(get_db)):

    json_list = []
    tiss_nums = []
    tiss_freq = []
    tiss_types = []

    tissues_with_freq = []

    if date_recorded:
        tissues_with_freq = crud_tissue.get_tissues_by_experiment_and_tissue_number_and_date_recorded(
            database, experiment_id, tissue_number, date_recorded)
    else:
        tissues_with_freq = crud_tissue.get_tissues_by_experiment_and_tissue_number(
            database, experiment_id, tissue_number)

    for tissue_object, frequency in tissues_with_freq:
        tiss_freq.append(frequency)
        tiss_types.append(tissue_object.tissue_type)
        tiss_nums.append(tissue_object.tissue_number)

        data = crud_tissue_tracking.get_tracking_by_id(
            database, tissue_object.id)

        # TODO: Change this is js not here
        data['disp'] = data['displacement']
        json_list.append(data.to_json(orient='columns'))

    json_list = json.dumps(json_list)

    res = jsonable_encoder({'json_data_list': json_list,
                            'nums': tiss_nums, 'freqs': tiss_freq, 'types': tiss_types})

    return JSONResponse(content=res)


@ router.post("/graphUpdate", tags=["analyze"])
def graph_update(data: schema_analysis.AnalysisBase, database: Session = Depends(get_db)):
    """Function gets called to update graph with new parameters"""
    tissue_obj = 0
    if data.video_id:
        video_object = crud_video.get_vid_by_id(database, data.video_id)
        tissue_obj = video_object.tissues[data.value]
    elif data.date_recorded:
        tissue_with_freq = crud_tissue.get_tissues_by_experiment_and_tissue_number_and_date_recorded(
            database, data.experiment_id, data.tissue_number, data.date_recorded)[data.value]
        # the tissue object is in spot zero of the tuple frew in spot 1
        tissue_obj = tissue_with_freq[0]
    else:
        tissue_with_freq = crud_tissue.get_tissues_by_experiment_and_tissue_number(
            database, data.experiment_id, data.tissue_number)[data.value]
        # the tissue object is in spot zero of the tuple frew in spot 1
        tissue_obj = tissue_with_freq[0]

    dataframe = crud_tissue_tracking.get_tracking_by_id(
        database, tissue_obj.id)

    tracking_obj = TissuePoints(
        dataframe['displacement'].to_list(), dataframe['time'].to_list(), tissue_obj)
    tracking_obj.smooth(int(data.windows), int(
        data.polynomials), data.buttons[0], data.buttons[1])
    tracking_obj.find_peaks(float(data.thresholds), int(
        data.minDistances), data.xrange, int(data.buffers))

    crud_tissue_caculations.create(
        database, tracking_obj.calculated_values, tissue_obj.id)
    # TODO: add anaylized to tissue
    # crud_video.video_anaylized(database, data.video_id)

    crud_tissue_tracking.update_forces_disp(database, tissue_obj.id, tracking_obj.smooth_force, tracking_obj.raw_force, tracking_obj.smooth_disp)

    contractx = tracking_obj.contract_points[0][0].tolist() + \
        tracking_obj.contract_points[2][0].tolist(
    ) + tracking_obj.contract_points[4][0].tolist()
    contracty = tracking_obj.contract_points[0][1].tolist() + \
        tracking_obj.contract_points[2][1].tolist(
    ) + tracking_obj.contract_points[4][1].tolist()
    relaxx = tracking_obj.relax_points[0][0].tolist() + tracking_obj.relax_points[1][0].tolist() + \
        tracking_obj.relax_points[2][0].tolist(
    ) + tracking_obj.relax_points[4][0].tolist()
    relaxy = tracking_obj.relax_points[0][1].tolist() + tracking_obj.relax_points[1][1].tolist() + \
        tracking_obj.relax_points[2][1].tolist(
    ) + tracking_obj.relax_points[4][1].tolist()
    return {'status': 'OK', 'data': {
        'xs': tracking_obj.time, 'ys': tracking_obj.smooth_force.tolist(),
        'peaksx': tracking_obj.peaks[0], 'peaksy': tracking_obj.peaks[1],
        'basex': tracking_obj.basepoints[0], 'basey': tracking_obj.basepoints[1],
        'frontx': tracking_obj.frontpoints[0], 'fronty': tracking_obj.frontpoints[1],
        'contractx': contractx, 'contracty': contracty,
        'relaxx': relaxx, 'relaxy': relaxy,
        'dfdtx': tracking_obj.time, 'dfdty': tracking_obj.dfdt.tolist(),
        'rawx': tracking_obj.time, 'rawy': tracking_obj.raw_force.tolist()
    }}


@router.get("/caculate", tags=["analyze"])
def download_summary(video_id=Query(None), experiment_identifier=Query(None), tissue_number=Query(None), database_session=Depends(get_db)):
    """Download summary of vid caculatios"""

    tissues = []

    if video_id:
        tissues = crud_video.get_vid_by_id(database_session, video_id).tissues
    else:
        tissues = crud_tissue.get_tissues_by_experiment_and_tissue_number(
            database_session, experiment_identifier, tissue_number)
        # this returns a tuple with tissue, freq, only need the tissue object in this case
        tissues = [x[0] for x in tissues]

    tissue_ids = [tissue.id for tissue in tissues]

    caculations_df = crud_tissue_caculations.get_calculations(
        database_session, tissue_ids)

    caculations_df["tissue_number"] = caculations_df["tissue_id"].apply(
        crud_tissue.get_tissue_number_by_id, database_session=(database_session))

    caculations_df["pacing_frequency"] = caculations_df["tissue_id"].apply(
        crud_tissue.get_frequency_by_tissue_id, database_session=database_session)

    models.check_path_exisits(f"{models.UPLOAD_FOLDER}/temp/")

    response = StreamingResponse(io.StringIO(caculations_df.to_csv(index=False)),
                                 media_type="text/csv")

    response.headers["Content-Disposition"] = "attachment; filename=caculations.csv"

    return response
