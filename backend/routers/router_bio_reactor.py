from typing import List
from database import get_db
from crud import crud_bio_reactor, crud_post
from schemas import schema_bio_reactor

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/bio_reactors", response_model=List[schema_bio_reactor.BioReactor], tags=["Bio_reactor"])
def get_bio_reactors(db: Session = Depends(get_db)):
    bio_reactors = crud_bio_reactor.get_bio_reactors(db)
    if not bio_reactors:
        raise HTTPException(status_code=404, detail="Bio Reactos not found")
    return bio_reactors


@router.post("/addBioReactor", response_model=schema_bio_reactor.BioReactorBase, tags=["Bio_reactor"])
def add_BioReactor(bio_reactor: schema_bio_reactor.BioReactorCreate, db: Session = Depends(get_db)):
    new_bio_reactor = crud_bio_reactor.create_bio_reactor(db, bio_reactor)

    for post in bio_reactor.posts:
        crud_post.create_post(db, post, new_bio_reactor.id)
    return bio_reactor


@router.delete("/bio_reactor/{bio_id}", tags=["Bio_reactor"])
def delete_bio_reactor(bio_id: int, db: Session = Depends(get_db)):
    return crud_bio_reactor.delete_bio_reactor(db, bio_id)
