import logging

import models
from schemas import schema_bio_reactor

from sqlalchemy.orm import Session


def create_bio_reactor(db: Session, bio_reactor: schema_bio_reactor.BioReactorBase):

    db_bio_reactor = models.Bio_reactor(
        date_added=bio_reactor.date_added, bio_reactor_number=bio_reactor.bio_reactor_number)
    db.add(db_bio_reactor)
    db.commit()
    db.refresh(db_bio_reactor)

    return db_bio_reactor
