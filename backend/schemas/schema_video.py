"""Schema for video"""
from typing import List, Optional
from datetime import date

from pydantic import BaseModel

from . import schema_tissue


class VideoBase(BaseModel):
    date_recorded: Optional[date]
    frequency: Optional[int]

    # bio_reactor_number: int

    class Config:
        orm_mode = True


class VideoCreate(VideoBase):
    tissues: List[schema_tissue.TissueBase]
    bio_reactor_id: int
    save_location: Optional[str]
    experiment_id: Optional[str]


class VideoInfo(VideoBase):
    id: int
    bio_reactor_id: int
    experiment_id: int


class Video(VideoBase):
    id: int


class VideoShow(VideoBase):
    id: int
    date_uploaded: date
    calibration_distance: Optional[float]
    calibration_factor: Optional[float]
    bio_reactor_number: int
    experiment_idenifer: str


class PostSelection(BaseModel):
    boxes: List[List[float]]
    cross_points: List[List[float]]
    cal_points: List[List[float]]
    video_id_value: int
    calibration_distance: int
