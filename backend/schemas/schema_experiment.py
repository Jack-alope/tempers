from typing import List
from datetime import date

from pydantic import BaseModel

from . import schema_video


class ExperimentBase(BaseModel):
    experiment_idenifer: str
    date_started: date

    class Config:
        orm_mode = True


class Experiment(ExperimentBase):
    id: int


class Experiment(Experiment):
    videos: List[schema_video.Video] = []
