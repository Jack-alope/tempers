
"""
CRUD for experiments
"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import exists

import models
from schemas import schema_experiment


def get_experiments(database_session: Session):
    """returns all experiments"""
    return database_session.query(models.Experiment).all()


def get_experiment(database_session: Session, exp_id: int):
    """Retunrs experiment by id"""
    return database_session.query(models.Experiment).filter(models.Experiment.id == exp_id).first()


def create_experiment(database_session: Session, experiment: schema_experiment.ExperimentBase):
    """Add Experiment to DB"""
    db_experiment = models.Experiment(**experiment.dict())
    database_session.add(db_experiment)
    database_session.commit()
    database_session.refresh(db_experiment)
    return db_experiment


def delete_experiment(database_session: Session, exp_id: int):
    """Deletes expeiments returns false if cannot delete bc has children"""
    # REVIEW: Smething weird with the delte no exception but does not delete
    try:
        database_session.delete(get_experiment(database_session, exp_id))
        database_session.commit()
        return True
    except IntegrityError:
        return False


def check_experiment_idetifyer_exsits(database_session: Session, experiment_idenifer: str):
    """Returns true if experiment_idenifier is in DB"""
    return database_session.query(exists().where(
        models.Experiment.experiment_idenifer == experiment_idenifer)).scalar()
