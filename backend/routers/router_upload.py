import os
from typing import List
import shutil
import json

from werkzeug.utils import secure_filename

from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, Body
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session


import models
from database import get_db
from crud import crud_video, crud_tissue
from schemas import schema_video, schema_tissue


router = APIRouter()

UPLOAD_FOLDER = models.UPLOAD_FOLDER


def save_video_file(vid_info, vid_file, db):
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')
    # gets saves in experment folder
    experiment_num = str(vid_info.experiment_id)

    # bio_reactor_num = models.get_bio_reactor_number(bio_reactor_id)

    # gets save loaction uploadfolder/expermentnum/date/vid
    where_to_save = os.path.join(
        UPLOAD_FOLDER, vid_info.experiment_id, date_string, 'videoFiles')

    # cheacks to make sure the save location exists if not exists
    models.check_path_exisits(where_to_save)

    orginal_filename = vid_file.filename
    extenstion = orginal_filename.rsplit('.', 1)[1].lower()

    # makes new file name for the vid format date_frewnum_bionum.ext
    # REVIEW: bio id or number?
    new_filename = date_string + "_" + \
        "Freq" + str(vid_info.frequency) + "_" + \
        "Bio" + str(vid_info.bio_reactor_id) + "." + extenstion

    # makes sure file name is correct formats
    safe_filename = secure_filename(new_filename)

    # creates path to file
    path_to_file = os.path.join(where_to_save, safe_filename)

    vid_info.save_location = path_to_file

    # saves file
    with open(path_to_file, "wb") as buffer:
        shutil.copyfileobj(vid_file.file, buffer)

    vid = crud_video.create_video(db, vid_info)

    return vid.id


def save_csv_file(vid_info, file, db):
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')
    where_to_save = os.path.join(
        UPLOAD_FOLDER, vid_info.experiment_id, date_string, 'csvfiles')
    models.check_path_exisits(where_to_save)

    new_filename = date_string + "_" + \
        "Freq" + str(vid_info.frequency) + "_T1.csv"

    # makes sure file name is correct formats
    safe_filename = secure_filename(new_filename)

    vid_info.save_location = None

    # creates path to file
    path_to_file = os.path.join(where_to_save, safe_filename)

    with open(path_to_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    vid = crud_video.create_video(db, vid_info)
    return (vid.id, path_to_file)


def add_tissues(tissue_li: List[schema_tissue.TissueCreate], bio_reactor_id: int,
                vid_id: int, db: Session):

    for tissue in tissue_li:
        tissue_obj = schema_tissue.TissueCreate.parse_obj(tissue)
        tissue_obj.vid_id = vid_id
        tissue_obj.bio_reactor_id = bio_reactor_id
        crud_tissue.create_tissue(db, tissue_obj)

    return True


@router.post("/upload", tags=["upload"])
async def post_upload(info: str = Form(...), file: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    # TODO Add schema to this form and file make it weird
    vid_json: schema_video.VideoCreate = json.loads(info)
    vid_info = schema_video.VideoCreate.parse_obj(vid_json)

    extension = file.filename.split(".")[-1]

    if extension == "csv":
        tup = save_csv_file(vid_info, file, db)
        vid_id = tup[0]
        setattr(vid_info.tissues[0], "csv_path", tup[1])

    else:
        vid_id = save_video_file(vid_info, file, db)

    print("Here")

    add_tissues(vid_info.tissues, vid_info.bio_reactor_id, vid_id, db)

    return {200: "OK"}
