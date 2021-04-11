from typing import Optional

from pydantic import BaseModel


class TissueBase(BaseModel):
    tissue_number: str
    tissue_type: str
    post_number: int

    class Config:
        orm_mode = True


class TissueCreate(TissueBase):
    vid_id: Optional[int]
    bio_reactor_id: Optional[int]


class TissueLater(TissueBase):
    csv_path: str
    cross_section_dist: float


class Tissue(TissueBase):
    id: int
