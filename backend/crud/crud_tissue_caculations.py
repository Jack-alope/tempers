"""
CRUD for tissue caculations
"""
from typing import List
from sqlalchemy.orm import Session
import pandas as pd

import models


def create(database_session: Session, caculations_dict: dict, tissue_id: int):
    """
    Create tissue caculations
    """
    # REVIEW: change to update maybe
    database_session.query(models.TissueCalculatedData).filter(
        models.TissueCalculatedData.tissue_id == tissue_id).delete(synchronize_session=False)
    caculations_dict["tissue_id"] = tissue_id
    db_tissue_caculation = models.TissueCalculatedData(**caculations_dict)
    database_session.add(db_tissue_caculation)
    database_session.commit()
    database_session.refresh(db_tissue_caculation)
    return db_tissue_caculation


def get_calculations(database_session: Session, tissue_ids: List[int]):
    """Gets caculation for tissue"""
    return pd.read_sql(database_session.query(models.TissueCalculatedData).filter(
        models.TissueCalculatedData.tissue_id.in_(tissue_ids)).statement, database_session.bind)
