"""Schema for tissue"""
from typing import Optional

from pydantic import BaseModel

from . import schema_tissue_calculated_data


class TissueBase(BaseModel):
    tissue_number: str
    tissue_type: str
    post_id: int

    class Config:
        orm_mode = True


class TissueCreate(TissueBase):
    vid_id: Optional[int]


class TissueLater(TissueBase):
    cross_section_dist: float


class Tissue(TissueBase):
    id: Optional[int]
    vid_id: Optional[int]
    cross_section_dist: Optional[float]
    # tissue_tracking: List[schema_tissue_tracking.TissueTrackingBase]
    tissue_caculated_data: Optional[schema_tissue_calculated_data.TissueCalculatedDataBase]


class TissueFull(Tissue):
    """Schema for to JSON"""
    id: int
    vid_id: int
