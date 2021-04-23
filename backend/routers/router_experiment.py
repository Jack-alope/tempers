"""
Router for experiment
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from database import get_db
from crud import crud_experiment
from schemas import schema_experiment


router = APIRouter()


@router.get("/experiments", response_model=List[schema_experiment.Experiment], tags=["Experiment"])
def read_experiments(database_session: Session = Depends(get_db)):
    """retunrs all experiment"""
    experiments = crud_experiment.get_experiments(database_session)
    if not experiments:
        raise HTTPException(status_code=404, detail="Experiments not found")
    return experiments


@router.delete("/experiment/{exp_id}", tags=["Experiment"])
def delete_experiment(exp_id: int, database_session: Session = Depends(get_db)):
    """Delete expirment by id"""
    return crud_experiment.delete_experiment(database_session, exp_id)


@router.post("/addExperiment", response_model=schema_experiment.Experiment,
             status_code=status.HTTP_201_CREATED, tags=["Experiment"])
def add_experiment(experiment: schema_experiment.ExperimentBase,
                   database_session: Session = Depends(get_db)):
    """Add experiment"""
    if crud_experiment.check_experiment_idetifyer_exsits(
            database_session, experiment.experiment_idenifer):
        raise HTTPException(status.HTTP_409_CONFLICT)
    new_experiment = crud_experiment.create_experiment(
        database_session, experiment)
    return new_experiment
