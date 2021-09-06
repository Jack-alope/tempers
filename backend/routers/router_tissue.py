"""Router for Tissues"""

from fastapi import APIRouter,  Depends, Query

from sqlalchemy.orm import Session

from database import get_db
from crud import crud_tissue, crud_experiment

router = APIRouter()


@router.get('/tissues_in_experiment', tags=["tissues"])
async def tissues_in_experiment(experiment_id: str = Query(...),
                                database: Session = Depends(get_db)):
    """Returns tissues within an experiment"""
    return crud_tissue.get_tissue_numbers_in_experiment(
        database, experiment_id)


@ router.get('/tissues_in_experiment_by_date_recorded', tags=["tissues"])
async def tissues_in_experiment_by_date(experiment_id: str = Query(...),
                                        date_recorded: str = Query(...),
                                        database: Session = Depends(get_db)):
    """Returns tissues within an experiment on date"""
    return crud_tissue.get_tissue_numbers_in_experiment_on_date(
        database, experiment_id, date_recorded)
