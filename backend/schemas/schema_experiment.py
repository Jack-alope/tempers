"""Schema expirment"""
from typing import List, Optional
from datetime import date

from pydantic import BaseModel

from . import schema_video, schema_bio_reactor


class ExperimentBase(BaseModel):
    id: str
    start_date: date

    class Config:
        orm_mode = True


class Experiment(ExperimentBase):
    id: str
    has_vids: Optional[bool]


class ExperimentWithVids(ExperimentBase):
    id: str
    vids: List[schema_video.Video]


class ExperimentDownload(BaseModel):
    experiment: ExperimentWithVids
    bio_reactors: List[schema_bio_reactor.BioReactorWithPosts]
