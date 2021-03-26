import logging

import models
from schemas import schema_experiment

from sqlalchemy.orm import Session



def get_experiments(db: Session):
    return db.query(models.Experiment).all()

def get_experiment(db: Session, exp_id: int):
    return db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()

def create_experiment(db: Session, experiment: schema_experiment.ExperimentBase):

    db_experiment = models.Experiment()
    [setattr(db_experiment, i[0], i[1]) for i in experiment]
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


def delete_experiment(db: Session, exp_id: int):
    db_experiment = get_experiment(db, exp_id)
    if db_experiment:
        db.delete(db_experiment)
        db.commit()
        return True
    else:
        return False