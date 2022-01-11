"""
Router for bio reactor
"""
import json
from typing import List
import datetime
from dataclasses import asdict


from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from database import get_db
from crud import crud_bio_reactor, crud_post
from schemas import schema_bio_reactor, schema_post

import models

router = APIRouter()


def _check_bio_reactor_has_vids(bio_reactor):
    """
    Accepts a models.Bioreactor and returns
    bio reactor schema with attrbure has vids
    """
    has_vids = bool(bio_reactor.vids)
    bio_reactor = schema_bio_reactor.BioReactor(**bio_reactor.__dict__)
    if has_vids:
        setattr(bio_reactor, "has_vids", True)
    else:
        setattr(bio_reactor, "has_vids", False)

    return bio_reactor


@router.get(
    "/bio_reactors",
    response_model=List[schema_bio_reactor.BioReactor],
    tags=["Bio_reactor"],
)
def read_bio_reactors(database_session: Session = Depends(get_db)):
    """Returns all bio reactors"""
    bio_reactors = crud_bio_reactor.get_bio_reactors(database_session)

    if not bio_reactors:
        raise HTTPException(status_code=404, detail="Bio Reactos not found")

    bio_reactors = [
        _check_bio_reactor_has_vids(bio_reactor) for bio_reactor in bio_reactors
    ]

    return bio_reactors


@router.get("/posts", response_model=List[schema_post.Post])
def read_post_options(bio_id: int = Query(...), database_session=Depends(get_db)):
    """returns posts in bio reactor"""
    posts = crud_post.get_posts_by_bio_id(database_session, bio_id)
    if not posts:
        return None
    return posts


@router.post(
    "/addBioReactor", response_model=schema_bio_reactor.BioReactor, tags=["Bio_reactor"]
)
def add_bio_reactor(
    bio_reactor: schema_bio_reactor.BioReactorCreate,
    database_session: Session = Depends(get_db),
):
    """Add a new BioReactor"""
    if crud_bio_reactor.check_bio_reactor_number_exsits(
        database_session, bio_reactor.bio_reactor_number
    ):
        raise HTTPException(status.HTTP_409_CONFLICT)
    new_bio_reactor = crud_bio_reactor.create_bio_reactor(database_session, bio_reactor)

    for post in bio_reactor.posts:
        crud_post.create_post(database_session, post, new_bio_reactor.id)
    return new_bio_reactor


@router.delete("/bio_reactor/{bio_id}", tags=["Bio_reactor"])
def delete_bio_reactor(bio_id: int, database_session: Session = Depends(get_db)):
    """deletes bio reactor by id"""
    return crud_bio_reactor.delete_bio_reactor(database_session, bio_id)


@router.get("/download/bio_reactor_archive", tags=["Bio_reactor"])
def dowload_bio_reactor_archive(
    background_tasks: BackgroundTasks, database_session: Session = Depends(get_db)
):
    bio_reactor_archive_file_path = "{models.UPLOAD_FOLDER}/temp"
    date_time = datetime.datetime.now()
    json_file_name = f"bio_reactor_archive_{date_time.strftime('%Y')}-{date_time.strftime('%b')}-{date_time.strftime('%d')}"
    models.check_path_exisits(bio_reactor_archive_file_path)
    bio_reactors = crud_bio_reactor.get_bio_reactors_as_schema(database_session)
    with open(f"{bio_reactor_archive_file_path}/{json_file_name}", "w") as outfile:
        json.dump(
            jsonable_encoder(
                schema_bio_reactor.BioReactorArchive(bio_reactors=bio_reactors)
            ),
            outfile,
            indent=1,
        )

    background_tasks.add_task(
        models.delete_file, f"{bio_reactor_archive_file_path}/{json_file_name}"
    )

    return FileResponse(f"{bio_reactor_archive_file_path}/{json_file_name}")
