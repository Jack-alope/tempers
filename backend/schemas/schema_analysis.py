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
    files_value: List[str]

    class Config:
        orm_mode = True
