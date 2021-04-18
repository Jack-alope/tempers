"""
CRUD for Bio reactor
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
from schemas import schema_bio_reactor


def get_bio_reactors(database_session: Session):
    """Returns all bio reactors"""
    return database_session.query(models.BioReactor).all()


def create_bio_reactor(database_session: Session, bio_reactor: schema_bio_reactor.BioReactorBase):
    """Adds bio reactor to DB"""
    db_bio_reactor = models.BioReactor(
        date_added=bio_reactor.date_added,
        bio_reactor_number=bio_reactor.bio_reactor_number)
    database_session.add(db_bio_reactor)
    database_session.commit()
    database_session.refresh(db_bio_reactor)

    return db_bio_reactor


def get_bio_reactor(database_session: Session, bio_id: int):
    """Returns bio reactor by for id"""
    return database_session.query(models.BioReactor).filter(models.BioReactor.id == bio_id).first()


def delete_bio_reactor(database_session: Session, bio_id: int):
    """Deletes bio Reactor"""
    try:
        database_session.delete(get_bio_reactor(database_session, bio_id))
        database_session.commit()
        return True
    except IntegrityError:
        return False
