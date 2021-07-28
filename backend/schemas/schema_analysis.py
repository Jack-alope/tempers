"""
Schema for analysis
"""
from typing import List, Optional


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
    experiment_identifier: Optional[str]
    tissue_number: Optional[int]

    class Config:
        orm_mode = True
