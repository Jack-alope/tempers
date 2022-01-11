"""Schema for tissue caculated"""

from pydantic import BaseModel


class TissueCalculatedDataBase(BaseModel):
    """Base schema for tisssue caculated"""

    dev_force: float
    dev_force_std: float
    sys_force: float
    sys_force_std: float
    dias_force: float
    dias_force_std: float
    beat_rate_cov: float
    beating_freq: float
    beating_freq_std: float
    t2pk: float
    t2pk_std: float
    t2rel50: float
    t2rel50_std: float
    t2rel80: float
    t2rel80_std: float
    t2rel90: float
    t2rel90_std: float
    t50: float
    t50_std: float
    c50: float
    c50_std: float
    r50: float
    r50_std: float
    dfdt: float
    dfdt_std: float
    negdfdt: float
    negdfdt_std: float


class TissueCalculatedDataFull(TissueCalculatedDataBase):
    """schema for to json"""

    id: int
    tissue_id: int
