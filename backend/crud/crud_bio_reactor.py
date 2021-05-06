"""
CRUD for Bio reactor
"""
from typing import List

from sqlalchemy.orm import Session, noload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import exists

import models
from schemas import schema_bio_reactor


def get_bio_reactors(database_session: Session):
    """Returns all bio reactors"""
    return database_session.query(models.BioReactor).all()


def get_bio_reactor(database_session: Session, bio_id: int):
    """Returns bio reactor by for id"""
    return database_session.query(models.BioReactor).filter(
        models.BioReactor.id == bio_id).first()


def get_bio_reactors_by_li_id(database_session: Session, bio_ids: List[int]):
    return database_session.query(models.BioReactor).options(noload(models.BioReactor.vids)).filter(
        models.BioReactor.id.in_(bio_ids)).all()


def create_bio_reactor(database_session: Session,
                       bio_reactor: schema_bio_reactor.BioReactorBase):
    """Adds bio reactor to DB"""
    db_bio_reactor = models.BioReactor(
        date_added=bio_reactor.date_added,
        bio_reactor_number=bio_reactor.bio_reactor_number)
    database_session.add(db_bio_reactor)
    database_session.commit()
    database_session.refresh(db_bio_reactor)

    return db_bio_reactor


def delete_bio_reactor(database_session: Session, bio_id: int):
    """Deletes bio Reactor"""
    try:
        database_session.delete(get_bio_reactor(database_session, bio_id))
        database_session.commit()
        return True
    except IntegrityError:
        return False
    except UnmappedInstanceError:
        print("bio does not exsists")


def check_bio_reactor_number_exsits(database_session: Session,
                                    bio_reactor_number: int):
    """Retuns true if bio number exsits"""
    return database_session.query(exists().where(
        models.BioReactor.bio_reactor_number == bio_reactor_number)).scalar()
