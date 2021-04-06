import logging
import threading
import os
from typing import List

import tracking
from template_config import templates
from database import get_db
from crud import crud_video, crud_experiment
from schemas import schema_video


from fastapi import APIRouter, Request, Form,  Depends, Query, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from sqlalchemy.orm import Session

import cv2

from scipy.spatial import distance


router = APIRouter()


def coord_distance(coords_list):
    '''
    Accepts a list of coords
    Returns a list of those coords coverted to distance in pixel
    '''
    dist_list = []
    for i in range(1, len(coords_list), 2):
        point_one = coords_list[i - 1]
        point_two = coords_list[i]

        d = float(distance.euclidean(point_one, point_two))

        dist_list.append(d)

    return dist_list


def get_video_info(db, vid_id):
    '''
     Find the video and gets an image from that vid saveing that image
     returning the image path and the number of tissues as a tup
    '''

    video_object = crud_video.get_vid_by_id(db, vid_id)
    file_path = video_object.save_location
    number_of_tisues = len(video_object.tissues)
    videostream = cv2.VideoCapture(file_path)
    image = videostream.read()[1]

    if not os.path.exists('static/uploads/img/'):
        os.makedirs('static/uploads/img/')

    image_path = 'static/uploads/img/' + \
        str(vid_id) + '.jpg'
    cv2.imwrite(image_path, image)
    # TODO: make sure image is horizonal
    return (image_path, number_of_tisues)


@router.get('/videos', response_model=List[schema_video.VideoInfo], tags=["tracking"])
async def get_videos(db: Session = Depends(get_db)):
    all_vids = crud_video.get_all_vids(db)
    return all_vids


@router.get('/selectedVideo/', tags=["tracking"])
async def selected_video(video_id: int = Query(...), db: Session = Depends(get_db)):
    tup_path_numTissues = get_video_info(db, video_id)

    res = jsonable_encoder({'image_path': tup_path_numTissues[0],
                            'number_tissues': tup_path_numTissues[1]})

    return JSONResponse(content=res)


@router.post('/boxCoordinates', tags=["tracking"])
async def boxCoordinates(postInfo: schema_video.PostSelection, db: Session = Depends(get_db)):

    # Get the distance in pix of the calibration line uses [0] b
    # since there are four points to the box passed but we only care
    # care ablout the length of the diagnal line
    cal_dist_pix = coord_distance(postInfo.cal_points)[0]

    cross_dist_pix = coord_distance(postInfo.cross_points)

    video_id = int(postInfo.video_id_value)

    cal_factor = postInfo.calibration_distance / cal_dist_pix

    cross_dist_mm = list(map(lambda x: x * cal_factor, cross_dist_pix))

    crud_video.update_cal_cross(
        db, postInfo.video_id_value, postInfo.calibration_distance, cal_factor, cross_dist_mm)

    video_object = crud_video.get_vid_by_id(db, postInfo.video_id_value)

    tissues = video_object.tissues
    tracking_thread = threading.Thread(
        target=tracking.start_trackig, args=(db, postInfo.boxes, postInfo.video_id_value, cal_factor, video_object, tissues))
    tracking_thread.start()
    return {"ok": 200}
