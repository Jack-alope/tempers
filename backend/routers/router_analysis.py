"""
Router for analysis
"""
import json


from fastapi import APIRouter,  Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from scipy.signal import savgol_filter

from database import get_db
from schemas import schema_analysis
from crud import crud_video, crud_tissue_tracking, crud_tissue_caculations
from analysis.tissues import TissuePoints


router = APIRouter()


@router.get('/analyze', tags=["analysis"])
async def analyze(video_id: int = Query(...), db: Session = Depends(get_db)):
    video = video_id

    json_list = []
    video_object = crud_video.get_vid_by_id(db, video)

    tiss_nums = []
    tiss_freq = []
    tiss_types = []
    tissues = video_object.tissues
    for i, tissue_object in enumerate(tissues):
        # Reads each file in as a dataframe
        tiss_freq.append(video_object.frequency)
        tiss_types.append(tissue_object.tissue_type)
        tiss_nums.append(tissue_object.tissue_number)

        data = crud_tissue_tracking.get_tracking_by_id(db, tissue_object.id)

        # TODO: Change this is js not here
        data['disp'] = data['displacment']
        json_list.append(data.to_json(orient='columns'))

    json_list = json.dumps(json_list)

    res = jsonable_encoder({'json_data_list': json_list,
                            'nums': tiss_nums, 'freqs': tiss_freq, 'types': tiss_types})

    return JSONResponse(content=res)


@ router.post("/graphUpdate", tags=["analysis"])
def graph_update(data: schema_analysis.AnalysisBase, db: Session = Depends(get_db)):
    """Function gets called to uodate graph with new parameters"""

    video_object = crud_video.get_vid_by_id(db, data.video_id_value)
    tissue_obj = video_object.tissues[data.value]
    dataframe = crud_tissue_tracking.get_tracking_by_id(db, tissue_obj.id)
    tracking_obj = TissuePoints(
        dataframe['displacment'].to_list(), dataframe['time'].to_list())
    tracking_obj.smooth(int(data.windows), int(data.polynomials))
    tracking_obj.find_peaks(int(data.thresholds), int(data.minDistances))

    crud_tissue_caculations.create(db,
                                   tracking_obj.calculated_values, tissue_obj.id)
    return {'status': 'OK', 'data': {'xs': tracking_obj.time, 'ys': tracking_obj.smooth_disp.tolist(),
                                     'peaksx': tracking_obj.peaks[0], 'peaksy': tracking_obj.peaks[1],
                                     'basex': tracking_obj.basepoints[0], 'basey': tracking_obj.basepoints[1],
                                     'frontx': tracking_obj.frontpoints[0], 'fronty': tracking_obj.frontpoints[1],
                                     'tencontx': tracking_obj.contract_points[0][0], 'tenconty': tracking_obj.contract_points[0][1],
                                     'fifcontx': tracking_obj.contract_points[2][0], 'fifconty': tracking_obj.contract_points[2][1],
                                     'ninecontx': tracking_obj.contract_points[4][0], 'nineconty': tracking_obj.contract_points[4][1],
                                     'ninerelx': tracking_obj.relax_points[0][0], 'ninerely': tracking_obj.relax_points[0][1],
                                     'fifrelx': tracking_obj.relax_points[2][0], 'fifrely': tracking_obj.relax_points[2][1],
                                     # TODO: Rename to eighty
                                     'tenrelx': tracking_obj.relax_points[1][0], 'tenrely': tracking_obj.relax_points[1][1],
                                     }}
