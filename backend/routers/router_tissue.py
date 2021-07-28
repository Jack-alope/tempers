"""Router for Tissues"""

from fastapi import APIRouter,  Depends, Query

from sqlalchemy.orm import Session

from database import get_db
from crud import crud_tissue, crud_experiment

router = APIRouter()


@router.get('/tissues_in_experiment', tags=["tissues"])
async def tissues_in_experiment(experiment_identifier: str = Query(...),
                                database: Session = Depends(get_db)):
    """Returns tissues within an experiment"""
    experiment_id = crud_experiment.get_experiment_by_idenifier(
        database, experiment_identifier).id
    return crud_tissue.get_tissue_numbers_in_experiment(
        database, experiment_id)
