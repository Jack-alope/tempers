"""Router for Calibration Set"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db as get_database

from crud import crud_calibration_set
from schemas import schema_calibration_set

router = APIRouter()


@router.get(
    "/calibrationSets",
    response_model=List[schema_calibration_set.CalibrationSet],
    tags=["Calibration Set"],
)
def get_calibration_sets(database: Session = Depends(get_database)):
    """Returns calibration sets"""

    return crud_calibration_set.get_calibration_sets(database)
