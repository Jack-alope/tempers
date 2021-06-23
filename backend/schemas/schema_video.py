"""Schema for video"""
from typing import List, Optional
from datetime import date

from pydantic import BaseModel

from . import schema_tissue


class VideoBase(BaseModel):
    date_recorded: date
    frequency: float

    class Config:
        orm_mode = True


class VideoCreate(VideoBase):
    tissues: List[schema_tissue.TissueBase]
    bio_reactor_id: int
    experiment_id: int
    tracked: bool = False
    analyzed: bool = False
    save_location: Optional[str]


class VideoInfo(VideoBase):
    id: int
    experiment_id: int
    save_location: Optional[str]


class Video(VideoBase):
    bio_reactor_id: int
    experiment_id: str
    tissues: List[schema_tissue.Tissue]
    calibration_distance: Optional[float]
    calibration_factor: Optional[float]
    save_location: Optional[str]


class VideoShow(VideoBase):
    id: int
    date_recorded: date
    bio_reactor_number: int
    experiment_idenifer: str
    tracked: bool
    anaylized: bool
    save_location: Optional[str]


class PostSelection(BaseModel):
    boxes: List[List[float]]
    cross_points: List[List[float]]
    cal_points: List[List[float]]
    video_id: int
    calibration_distance: int
