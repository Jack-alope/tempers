from typing import List

from database import get_db
from crud import crud_experiment
from schemas import schema_experiment

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/experiments", response_model=List[schema_experiment.Experiment], tags=["Experiment"])
def get_experiments(db: Session = Depends(get_db)):
    experiments = crud_experiment.get_experiments(db)
    if not experiments:
        raise HTTPException(status_code=404, detail="Experiments not found")
    return experiments


@router.delete("/experiment/{id}", tags=["Experiment"])
def delete_experiment(id: int, db: Session = Depends(get_db)):
    return crud_experiment.delete_experiment(db, id)


@router.post("/addExperiment", response_model=schema_experiment.Experiment, tags=["Experiment"])
def add_Experiment(experiment: schema_experiment.ExperimentBase, db: Session = Depends(get_db)):
    # TODO: error if exsists
    new_experiment = crud_experiment.create_experiment(db, experiment)
    return new_experiment
