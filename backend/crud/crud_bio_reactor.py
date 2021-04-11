import logging

import models
from schemas import schema_bio_reactor

from sqlalchemy.orm import Session


def get_bio_reactors(db: Session):
    return db.query(models.Bio_reactor).all()


def create_bio_reactor(db: Session, bio_reactor: schema_bio_reactor.BioReactorBase):
    db_bio_reactor = models.Bio_reactor(
        date_added=bio_reactor.date_added, bio_reactor_number=bio_reactor.bio_reactor_number)

    db.add(db_bio_reactor)
    db.commit()
    db.refresh(db_bio_reactor)

    return db_bio_reactor


def get_bio_reactor(db: Session, bio_id: int):
    return db.query(models.Bio_reactor).filter(models.Bio_reactor.id == bio_id).first()


def delete_bio_reactor(db: Session, bio_id: int):
    db_bio_reactor = get_bio_reactor(db, bio_id)
    if db_bio_reactor:
        db.delete(db_bio_reactor)
        db.commit()
        return True
    else:
        return False
