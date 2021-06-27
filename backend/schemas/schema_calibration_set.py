"""Schema calibration set"""
from pydantic import BaseModel


class CalibrationSet(BaseModel):
    calibration_set_identifier: str
    calibration_factor: float

    class Config:
        orm_mode = True
