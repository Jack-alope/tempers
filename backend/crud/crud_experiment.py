import logging

import models
from schemas import schema_experiment

from sqlalchemy.orm import Session


def create_experiment(db: Session, experiment: schema_experiment.ExperimentBase):

    db_experiment = models.Experiment()
    [setattr(db_experiment, i[0], i[1]) for i in experiment]
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment
