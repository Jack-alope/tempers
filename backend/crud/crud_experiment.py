
"""
CRUD for experiments
"""
import shutil
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import exists

import models
from schemas import schema_experiment


def get_experiments(database_session: Session):
    """Returns all experiments"""
    return database_session.query(models.Experiment).all()


def get_experiment(database_session: Session, exp_id: str):
    """Returns experiment by id"""
    return database_session.query(models.Experiment).filter(
        models.Experiment.id == exp_id).first()


def get_experiment_vid(database_session: Session, exp_id: str):
    """Returns experiment by id"""
    return database_session.query(models.Experiment, models.Video.id).join(
        models.Video).filter(models.Experiment.id == exp_id).first()


def create_experiment(database_session: Session, experiment: schema_experiment.ExperimentBase):
    """Add Experiment to DB"""
    db_experiment = models.Experiment(**experiment.dict())
    database_session.add(db_experiment)
    database_session.commit()
    database_session.refresh(db_experiment)
    return db_experiment


def delete_experiment(database_session: Session, exp_id: str):
    """Deletes expeiments returns false if cannot delete bc has children"""
    try:
        experiment = get_experiment(database_session, exp_id)

        if experiment.vids:
            # returns false so that the experiemnt does not delete
            # if exp has vids
            return False
        database_session.delete(experiment)
        database_session.commit()
        shutil.rmtree(
            f"{models.UPLOAD_FOLDER}/{experiment.id}")
        return True
    except IntegrityError:
        return False
    except FileNotFoundError:
        logging.info("file doesnt not exsit")
        return True
    except UnmappedInstanceError:
        logging.info("Experiment does not exist")
        return False


def check_experiment_id_exsits(database_session: Session, experiment_id: str):
    """Returns true if experiment_idenifier is in DB"""
    return database_session.query(exists().where(
        models.Experiment.id == experiment_id)).scalar()
