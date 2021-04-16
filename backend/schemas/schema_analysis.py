from typing import List


from pydantic import BaseModel


class AnalysisBase(BaseModel):
    xrange: List
    value: int
    thresholds: float
    buffers: int
    polynomials: int
    windows: int
    minDistances: int
    video_id_value: int

    class Config:
        orm_mode = True
