"""
Schema for analysis
"""
from typing import List, Optional
from datetime import date


from pydantic import BaseModel


class AnalysisBase(BaseModel):
    """Base analysis class"""

    xrange: List
    value: int
    thresholds: float
    polynomials: int
    windows: int
    minDistances: int
    video_id: Optional[int]
    buffers: int
    experiment_id: Optional[str]
    tissue_number: Optional[int]
    buttons: List
    date_recorded: Optional[date]

    class Config:
        orm_mode = True
