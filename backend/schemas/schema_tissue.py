"""Schema for tissue"""
from typing import Optional

from pydantic import BaseModel
from pydantic.types import OptionalInt

from . import schema_tissue_calculated_data


class TissueBase(BaseModel):
    tissue_number: str
    tissue_type: str
    post_id: int

    class Config:
        orm_mode = True


class TissueCreate(TissueBase):
    vid_id: int


class Tissue(TissueBase):
    id: Optional[int]
    vid_id: Optional[int]
    cross_section_dist: Optional[float]
    # REVIEW: tissie tracking
    # tissue_tracking: List[schema_tissue_tracking.TissueTrackingBase]
    tissue_caculated_data: Optional[schema_tissue_calculated_data.TissueCalculatedDataBase]


class TissueFull(Tissue):
    """Schema for to JSON"""
    id: int
    vid_id: int


def create_tissue(base_tissue: TissueBase, vid_id: int):
    """Converts TissueBase to TissueCreate"""
    tissue_dict = base_tissue.dict()
    tissue_dict['vid_id'] = (vid_id)

    return TissueCreate.parse_obj(tissue_dict)
