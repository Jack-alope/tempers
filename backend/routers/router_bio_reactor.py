"""
Router for bio reactor
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db
from crud import crud_bio_reactor, crud_post
from schemas import schema_bio_reactor


router = APIRouter()


@router.get("/bio_reactors",
            response_model=List[schema_bio_reactor.BioReactor],
            tags=["Bio_reactor"])
def read_bio_reactors(database_session: Session = Depends(get_db)):
    """Returns all bio reactors"""
    bio_reactors = crud_bio_reactor.get_bio_reactors(database_session)
    if not bio_reactors:
        raise HTTPException(status_code=404, detail="Bio Reactos not found")
    return bio_reactors


@router.post("/addBioReactor",
             response_model=schema_bio_reactor.BioReactorBase,
             tags=["Bio_reactor"])
def add_bio_reactor(bio_reactor: schema_bio_reactor.BioReactorCreate,
                    database_session: Session = Depends(get_db)):
    """Add a new BioReactor"""
    new_bio_reactor = crud_bio_reactor.create_bio_reactor(
        database_session, bio_reactor)

    for post in bio_reactor.posts:
        crud_post.create_post(database_session, post, new_bio_reactor.id)
    return bio_reactor


@router.delete("/bio_reactor/{bio_id}", tags=["Bio_reactor"])
def delete_bio_reactor(bio_id: int, database_session: Session = Depends(get_db)):
    """deletes bio reactor by id"""
    return crud_bio_reactor.delete_bio_reactor(database_session, bio_id)
