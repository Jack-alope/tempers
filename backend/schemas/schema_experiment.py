"""Schema expirment"""
from typing import List
from datetime import date

from pydantic import BaseModel

from . import schema_video


class ExperimentBase(BaseModel):
    experiment_idenifer: str
    start_date: date

    class Config:
        orm_mode = True


class Experiment(ExperimentBase):
    id: int


class ExperimentWithVids(Experiment):
    videos: List[schema_video.Video] = []
