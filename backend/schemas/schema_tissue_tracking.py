"""Schema for tracking data"""

from pydantic import BaseModel


class TissueTrackingBase(BaseModel):
    """Base schema for Tissue Tracking"""

    time: float
    displacement: float
    odd_x: float
    odd_y: float
    even_x: float
    even_x: float


class TissueTrackingFull(TissueTrackingBase):
    """Schemea for to JSON"""

    id: int
    tissue_id: int
