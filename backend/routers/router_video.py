"""
Router for Video
"""
import os
from typing import List, Dict
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import cv2


from database import get_db as get_database
from crud import crud_video, crud_bio_reactor
from schemas import schema_video


router = APIRouter()


def get_video_info(database, vid_id):
    '''
     Find the video and gets an image from that vid saveing that image
     returning the image path and the number of tissues as a tup
    '''

    video_object = crud_video.get_vid_by_id(database, vid_id)
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


@router.get('/videos', response_model=List[schema_video.VideoInfo], tags=["Videos"])
async def get_videos(database: Session = Depends(get_database)):
    """returns all vids"""
    return crud_video.get_all_vids(database)


@router.get('/selectedVideo', tags=["Videos"])
async def selected_video(video_id: int = Query(...), database: Session = Depends(get_database)):
    """
    accepts vid id from query string and
    returns info on that vid image path and nunmber of tissues
    """
    tup_path_num_tissues = get_video_info(database, video_id)

    res = jsonable_encoder({'image_path': tup_path_num_tissues[0],
                            'number_tissues': tup_path_num_tissues[1]})

    return JSONResponse(content=res)


@router.get("/videos_show", response_model=Dict[str, List[schema_video.VideoShow]], tags=["Videos"])
def get_vids_reactors(database: Session = Depends(get_database)):
    """
    Gets all vids from db
    returns 404 if none
    """
    videos = crud_video.get_videos(database)

    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")

    result = defaultdict(list)

    for vid in videos:
        result[vid.experiment_idenifer].append(
            schema_video.VideoShow(**vid.__dict__))

    return dict(result)


@router.delete("/video/{vid_id}", tags=["Videos"])
def delete_video(vid_id: int, database: Session = Depends(get_database)):
    """
    endpoint to delete vid from DB
    """

    return crud_video.delete_video(database, vid_id)
