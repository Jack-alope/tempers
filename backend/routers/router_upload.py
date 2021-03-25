import logging
import os
from datetime import date
from typing import List, Optional
import shutil
import json

from werkzeug.utils import secure_filename

import models
from template_config import templates
from database import get_db
from crud import crud_video, crud_tissue
from schemas import schema_video, schema_tissue


from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, Body
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session


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

    '''
    # No idea what this is
    # TODO: write fuction to get the bio reactor id based on the number and date
    # bio_reactor_id = 1
    bio_reactor_id = models.calculate_bio_id(
        bio_reactor_num, form_passed.date_recorded.data)
    '''

    return vid.id


def add_tissues(tissue_li: List[schema_tissue.TissueCreate], vid_id: int, db: Session):

    for tissue in tissue_li:
        tissue_obj = schema_tissue.TissueCreate.parse_obj(tissue)
        tissue_obj.vid_id = vid_id
        crud_tissue.create_tissue(db, tissue_obj)

    return True


@router.post("/upload", tags=["upload"])
async def post_upload(info: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # TODO Add schema to this form anf file make it weird
    vid_json: schema_video.VideoCreate = json.loads(info)
    vid_info = schema_video.VideoCreate.parse_obj(vid_json)

    vid_id = save_video_file(vid_info, file, db)

    add_tissues(vid_info.tissues, vid_id, db)

    return {200: "OK"}
