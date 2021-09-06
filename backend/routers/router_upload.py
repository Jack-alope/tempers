"""
Router for upload
"""
import os
from typing import List
import shutil
import json
import logging

from werkzeug.utils import secure_filename

from fastapi import APIRouter, Form, File, UploadFile, Depends

from sqlalchemy.orm import Session


import pandas as pd


import models
from database import get_db
from crud import crud_video, crud_tissue, crud_tissue_tracking, \
    crud_experiment, crud_bio_reactor, crud_post, crud_tissue_caculations
from schemas import schema_video, schema_tissue, schema_experiment


router = APIRouter()

UPLOAD_FOLDER = models.UPLOAD_FOLDER


def _save_file(file, path: str):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file, buffer)


def _save_video_file(vid_info, vid_file, database_session):
    """Saves vid file to disk and adds to db"""
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')

    experiment_info = crud_experiment.get_experiment(
        database_session, vid_info.experiment_id)

    vid = crud_video.create_video(database_session, vid_info)

    # gets save loaction uploadfolder/expermentnum/date/vid
    where_to_save = os.path.join(
        UPLOAD_FOLDER, experiment_info.id, 'videos')

    # cheacks to make sure the save location exists if not exists
    models.check_path_exisits(where_to_save)

    orginal_filename = vid_file.filename
    extenstion = orginal_filename.rsplit('.', 1)[1].lower()

    bio_reactor_info = crud_bio_reactor.get_bio_reactor(
        database_session, vid_info.bio_reactor_id)
    # makes new file name for the vid format date_frewnum_bionum.ext
    new_filename = f"{date_string}_Freq{str(vid_info.frequency).replace('.','-')}_Bio\
        {str(bio_reactor_info.bio_reactor_number)}_{str(vid.id)}.{extenstion}"

    # makes sure file name is correct formats
    safe_filename = secure_filename(new_filename)

    # creates path to file
    path_to_file = os.path.join(where_to_save, safe_filename)

    crud_video.update_save_location(database_session, vid.id, path_to_file)

    # saves file
    _save_file(vid_file.file, path_to_file)

    return vid.id


def _save_csv_file(vid_info, file, database_session):
    """Saves csv to disk and addes to db with fake vid"""
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')
    where_to_save = os.path.join(
        UPLOAD_FOLDER, str(vid_info.experiment_id), date_string, 'csvfiles')
    models.check_path_exisits(where_to_save)

    new_filename = date_string + "_" + \
        "Freq" + str(vid_info.frequency) + "_T1.csv"

    # makes sure file name is correct formats
    safe_filename = secure_filename(new_filename)

    vid_info.save_location = None
    vid_info.tracked = True

    # creates path to file
    path_to_file = os.path.join(where_to_save, safe_filename)

    _save_file(file.file, path_to_file)

    vid = crud_video.create_video(database_session, vid_info)
    return (vid.id, path_to_file)


def _add_tissues(tissue_li: List[schema_tissue.TissueCreate],
                 vid_id: int, database_session: Session):
    """Adds tissues to databse"""

    tissue_id = 0

    for tissue in tissue_li:
        tissue_id = crud_tissue.create_tissue(
            database_session, schema_tissue.create_tissue(tissue, vid_id))
    # REVIEW: Doeen't make much sense to return this
    return tissue_id


@router.post("/upload", tags=["upload"])
async def upload(info: str = Form(...), file: UploadFile = File(...),
                 database_session: Session = Depends(get_db)):
    """Upload csv or vid"""
    vid_info = schema_video.VideoCreate.parse_obj(json.loads(info))

    extension = file.filename.split(".")[-1]

    tup = ()

    if extension == "csv":
        tup = _save_csv_file(vid_info, file, database_session)
        vid_id = tup[0]

    else:
        vid_id = _save_video_file(vid_info, file, database_session)
    # REVIEW: doesnt make sense to assign tissue maybe only for CSV
    tissue = _add_tissues(
        vid_info.tissues, vid_id, database_session)

    if extension == "csv":
        dataframe = pd.read_csv(tup[1])
        dataframe["tissue_id"] = tissue.id
        crud_tissue_tracking.create_tissue_tracking(
            database_session, tissue.id, dataframe)
        models.delete_file(tup[1])

    return {200: "OK"}


def _unzip_and_delete(archive_path, where_to_save):
    shutil.unpack_archive(archive_path, where_to_save)
    os.remove(archive_path)


def _add_experiment_to_db(database_session, experiment_info):

    # REVIEW: Proablly dont want to just delete
    crud_experiment.delete_experiment(database_session, experiment_info.id)

    delattr(experiment_info, "id")
    delattr(experiment_info, "vids")

    experiment = crud_experiment.create_experiment(
        database_session, experiment_info)

    return (experiment.id, experiment.experiment_idenifer)


def _add_bio_reactos_to_db(database_session: Session, bio_reactors_info):
    bio_ids = {}
    post_ids = {}
    for bio in bio_reactors_info:
        old_id = bio.id
        # REVIEW: Probally dont want to just delete
        crud_bio_reactor.delete_bio_reactor(database_session, old_id)
        posts = bio.posts
        delattr(bio, "id")
        delattr(bio, "posts")
        new_bio = crud_bio_reactor.create_bio_reactor(database_session, bio)
        bio_ids[old_id] = new_bio.id
        for post in posts:
            old_post_id = post.id
            delattr(post, "id")
            new_post = crud_post.create_post(
                database_session, post, new_bio.id)
            post_ids[old_post_id] = new_post.id

    return (bio_ids, post_ids)


def _tissue_tracking_csv_to_db(database_session: Session, new_tissue_id: int, old_tissue_id: int):

    csv_path = f"{UPLOAD_FOLDER}/temp/csvs"

    for file in os.listdir(csv_path):
        if int(file.split("_")[2].split(".")[0]) == old_tissue_id:
            try:
                tracking_df = pd.read_csv(os.path.join(csv_path, file), usecols=[
                    "tissue_id", "time", "displacement",
                    "odd_x", "odd_y", "even_x", "even_y"])

                tracking_df["tissue_id"] = tracking_df["tissue_id"].map(
                    {old_tissue_id: new_tissue_id}, na_action=None)

                # REVIEW: Maybe dont wanna just delete
                crud_tissue_tracking.delete(database_session, old_tissue_id)
                crud_tissue_tracking.create_tissue_tracking(
                    database_session, new_tissue_id, tracking_df)
            except pd.errors.EmptyDataError:
                logging.info("Tracking CSV Empty")


def _add_vids_to_db(database_session: Session, vids,
                    experiment_id: int, bio_ids: dict, post_ids: dict):
    for vid in vids:
        #old_id = vid.id
        # REVIEW: Probally dont want to just delete
        tissues = vid.tissues
        bio_id = bio_ids[vid.bio_reactor_id]
        delattr(vid, "bio_reactor_id")
        vid = schema_video.Video(
            **dict(vid),
            bio_reactor_id=bio_id,)
        setattr(vid, "experiment_id", experiment_id)
        new_vid_id = crud_video.create_video(database_session, vid).id

        for tissue in tissues:
            post_id = post_ids[tissue.post_id]
            old_tissue_id = tissue.id
            delattr(tissue, "post_id")
            delattr(tissue, "vid_id")
            delattr(tissue, "id")
            if tissue.tissue_caculated_data:
                tissue_caculated = dict(tissue.tissue_caculated_data)
            delattr(tissue, "tissue_caculated_data")

            tissue = schema_tissue.Tissue(
                **dict(tissue), vid_id=new_vid_id, post_id=post_id)
            new_tissue_id = crud_tissue.create_tissue(
                database_session, tissue).id

            if tissue.tissue_caculated_data:
                crud_tissue_caculations.create(
                    database_session, tissue_caculated, new_tissue_id)

            _tissue_tracking_csv_to_db(
                database_session, new_tissue_id, old_tissue_id)


def _expirment_file_unpack(database_session: Session,  dir_path: str):

    json_file, = [os.path.join(dir_path, f) for f in os.listdir(
        dir_path) if f.endswith('.json')]

    with open(json_file) as file:
        data: schema_experiment.ExperimentDownload = schema_experiment.ExperimentDownload(
            **json.load(file))

    vids = data.experiment.vids

    bio_ids, post_ids = _add_bio_reactos_to_db(
        database_session, data.bio_reactors)
    experiment_id, experiment_idenifer = _add_experiment_to_db(
        database_session, data.experiment)

    _add_vids_to_db(database_session, vids,
                    experiment_id, bio_ids, post_ids)

    return experiment_idenifer


@router.post("/upload/experiment_archive", tags=["upload", "Experiment"])
async def upload_experiment(file: UploadFile = File(...),
                            database_session: Session = Depends(get_db)):

    # TODO: add Tracking data

    where_to_save = os.path.join(UPLOAD_FOLDER, "temp")
    models.check_path_exisits(where_to_save)

    safe_filename = secure_filename(file.filename)

    archive_path = os.path.join(where_to_save, safe_filename)

    _save_file(file.file, archive_path)

    _unzip_and_delete(archive_path, where_to_save)

    experiment_idenifer = _expirment_file_unpack(
        database_session, where_to_save)

    shutil.move(os.path.join(where_to_save, "videos"), os.path.join(
        UPLOAD_FOLDER, experiment_idenifer, "videos"))

    shutil.rmtree(where_to_save)

    return {200: "OK"}
