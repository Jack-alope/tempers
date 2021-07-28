
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
    """returns all experiments"""
    return database_session.query(models.Experiment).all()


def get_experiment(database_session: Session, exp_id: int):
    """Retunrs experiment by id"""
    return database_session.query(models.Experiment).filter(
        models.Experiment.id == exp_id).first()


def get_experiment_by_idenifier(database_session: Session, experiment_idenifer: str):
    """Retunrs experiment by idenifer"""
    return database_session.query(models.Experiment).filter(
        models.Experiment.experiment_idenifer == experiment_idenifer).first()


def get_experiment_vid(database_session: Session, exp_id: int):
    """Retunrs experiment by id"""
    return database_session.query(models.Experiment, models.Video.id).join(
        models.Video).filter(models.Experiment.id == exp_id).first()


def create_experiment(database_session: Session, experiment: schema_experiment.ExperimentBase):
    """Add Experiment to DB"""
    db_experiment = models.Experiment(**experiment.dict())
    database_session.add(db_experiment)
    database_session.commit()
    database_session.refresh(db_experiment)
    return db_experiment


def delete_experiment(database_session: Session, exp_id: int):
    """Deletes expeiments returns false if cannot delete bc has children"""
    try:
        experiment = get_experiment(database_session, exp_id)
        database_session.delete(experiment)
        database_session.commit()
        shutil.rmtree(
            f"{models.UPLOAD_FOLDER}/{experiment.experiment_idenifer}")
        return True
    except IntegrityError:
        return False
    except FileNotFoundError:
        logging.info("file doesnt not exsit")
        return True
    except UnmappedInstanceError:
        logging.info("experiment does not exist")
        return False


def delete_experiment_by_identifer(database_session: Session, experiment_idenifer: str):
    exp = get_experiment_by_idenifier(database_session, experiment_idenifer)

    if exp:
        delete_experiment(database_session, exp.id)


def check_experiment_idetifyer_exsits(database_session: Session, experiment_idenifer: str):
    """Returns true if experiment_idenifier is in DB"""
    return database_session.query(exists().where(
        models.Experiment.experiment_idenifer == experiment_idenifer)).scalar()
