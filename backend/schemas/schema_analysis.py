"""
Schema for analysis
"""
from typing import List


from pydantic import BaseModel


class AnalysisBase(BaseModel):
    """Base analysis class"""
    xrange: List
    value: int
    thresholds: float
    polynomials: int
    windows: int
    minDistances: int
    video_id: int

    class Config:
        orm_mode = True
