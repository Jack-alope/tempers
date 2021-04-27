"""Schema expirment"""
from typing import List
from datetime import date

from pydantic import BaseModel

from . import schema_video, schema_bio_reactor


class ExperimentBase(BaseModel):
    experiment_idenifer: str
    start_date: date

    class Config:
        orm_mode = True


class Experiment(ExperimentBase):
    vids: List[schema_video.Video]


class ExperimentFull(Experiment):
    id: int


class ExperimentShow(ExperimentBase):
    id: int


class ExperimentDownload(BaseModel):
    experiment: Experiment
    bio_reactors: List[schema_bio_reactor.BioReactorFull]
