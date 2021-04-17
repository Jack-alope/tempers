"""
CRUD for tissue caculations
"""
from sqlalchemy.orm import Session

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
