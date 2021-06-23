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
    id: int


class ExperimentWithVids(ExperimentBase):
    id: int
    vids: List[schema_video.Video]


class ExperimentDownload(BaseModel):
    experiment: ExperimentWithVids
    bio_reactors: List[schema_bio_reactor.BioReactorWithPosts]
