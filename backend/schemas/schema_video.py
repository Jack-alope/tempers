from typing import List, Optional
from datetime import date


from . import schema_tissue

from pydantic import BaseModel


class VideoBase(BaseModel):
    date_recorded: Optional[date]
    experiment_id: Optional[str]
    frequency: Optional[int]

    # bio_reactor_number: int

    class Config:
        orm_mode = True


class VideoCreate(VideoBase):
    tissues: List[schema_tissue.TissueBase]
    bio_reactor_id: int
    save_location: Optional[str]


class VideoInfo(VideoBase):
    id: int
    bio_reactor_id: int


class VideoLater(VideoBase):
    date_uploaded: date
    calibration_distance: float
    calibration_factor: float


class Video(VideoBase):
    id: int


class PostSelection(BaseModel):
    boxes: List[List[float]]
    cross_points: List[List[float]]
    cal_points: List[List[float]]
    video_id_value: int
    calibration_distance: int
