import logging
import threading
import glob
import json
from typing import List

from template_config import templates
from database import get_db
from schemas import schema_analysis
from crud import crud_video, crud_tissue
from analysisFolder import analysis as analysis
from analysisFolder import calculations as calcs

from fastapi import APIRouter, Request, Form,  Depends, Query, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from sqlalchemy.orm import Session

import pandas as pd

router = APIRouter()

glob_data = []


@router.get('/analyze', tags=["analysis"])
async def analyze(video_id: int = Query(...), db: Session = Depends(get_db)):
    video = video_id

    json_list = []
    video_object = crud_video.get_vid_by_id(db, video)
    # date = form.date.data
    # exp = form.experiment.data
    exp = video_object.experiment_id
    date = video_object.date_recorded
    # date = date.replace('/', '_')
    date = date.strftime("%m_%d_%Y")
    files = glob.glob('static/uploads/' + str(exp) +
                      '/' + date + '/csvfiles/*')
    tiss_nums = []
    tiss_freq = []
    tiss_types = []
    dataframes = []
    global glob_data
    for i, file in enumerate(files):
        # Reads each file in as a dataframe
        glob_data.append([])
        tissue_object = crud_tissue.get_tissue_by_csv(db, file)
        tiss_freq.append(tissue_object.video.frequency)
        tiss_types.append(tissue_object.tissue_type)
        tiss_nums.append(tissue_object.tissue_number)
        dataframes.append(pd.read_csv(file))
        dataframe_smooth, peaks, basepoints, frontpoints, ten, fifty, eighty, ninety = analysis.findpoints(
            dataframes[i]['disp'], dataframes[i], 3, 3, 13, .6, 5, 0, 0)
        glob_data[i] = analysis.findpoints(
            dataframes[i]['disp'], dataframes[i], 3, 3, 13, .6, 5, 0, 0)
        json_list.append(dataframe_smooth.to_json(orient='columns'))

    json_list = json.dumps(json_list)

    res = jsonable_encoder({'json_data_list': json_list,
                            'nums': tiss_nums, 'freqs': tiss_freq, 'types': tiss_types, "files": files})

    return JSONResponse(content=res)


@router.post("/graphUpdate", tags=["analysis"])
def graphUpdate(data: schema_analysis.AnalysisBase):
    print(data)

    #data = json.loads(data).get("data")

    global glob_data
    files = data.files_value
    datafram = []
    raw = []
    for i, file in enumerate(files):
        datafram.append(pd.read_csv(file))
        raw.append(pd.read_csv(file))

    raw[int(data.value)]['disp'] = raw[int(data.value)]['disp'] * -1
    dataframe_smooth, peaks, basepoints, frontpoints, ten, fifty, eighty, ninety = analysis.findpoints(raw[int(data.value)]['disp'], datafram[int(data.value)],
                                                                                                       int(data.buffers), int(data.polynomials), int(
        data.windows), float(data.thresholds), int(data.minDistances),
        int(data.xrange[0]), int(data.xrange[1]))
    glob_data[int(data.value)] = analysis.findpoints(raw[int(data.value)]['disp'], datafram[int(data.value)],
                                                     int(data.buffers), int(data.polynomials), int(
        data.windows), float(data.thresholds), int(data.minDistances),
        int(data.xrange[0]), int(data.xrange[1]))
    rawx = raw[int(data.value)]['time'].tolist()
    rawy = raw[int(data.value)]['disp'].tolist()
    times = dataframe_smooth['time'].to_list()
    disps = dataframe_smooth['disp'].to_list()
    peaksx = dataframe_smooth['time'][peaks].to_list()
    peaksy = dataframe_smooth['disp'][peaks].to_list()
    basex = dataframe_smooth['time'][basepoints].to_list()
    basey = dataframe_smooth['disp'][basepoints].to_list()
    frontx = dataframe_smooth['time'][frontpoints].to_list()
    fronty = dataframe_smooth['disp'][frontpoints].to_list()
    tencontx = ten[0]
    tenconty = ten[1]
    tenrelx = ninety[2]
    tenrely = ninety[3]

    fifcontx = fifty[0]
    fifconty = fifty[1]
    fifrelx = fifty[2]
    fifrely = fifty[3]

    ninecontx = ninety[0]
    nineconty = ninety[1]
    ninerelx = ten[2]
    ninerely = ten[3]

    return {'status': 'OK', 'data': {'xs': times, 'ys': disps,
                                     'peaksx': peaksx, 'peaksy': peaksy,
                                     'basex': basex, 'basey': basey,
                                     'frontx': frontx, 'fronty': fronty,
                                     'tencontx': tencontx, 'tenconty': tenconty,
                                     'tenrelx': tenrelx, 'tenrely': tenrely,
                                     'fifcontx': fifcontx, 'fifconty': fifconty,
                                     'fifrelx': fifrelx, 'fifrely': fifrely,
                                     'ninecontx': ninecontx, 'nineconty': nineconty,
                                     'ninerelx': ninerelx, 'ninerely': ninerely,
                                     'rawx': rawx, 'rawy': rawy
                                     }}


@ router.post('/call_calcs', tags=["analysis"])
def call_calcs(files: List[str], db: Session = Depends(get_db)):
    global glob_data
    calcs.carry_calcs(db, glob_data, files)
    return {"ok": 200}
