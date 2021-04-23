"""
CRUD for tissues
"""

from sqlalchemy.orm import Session

import models
from schemas import schema_tissue


def create_tissue(database_session: Session, tissue: schema_tissue.TissueCreate):
    """Create Tissue"""
    db_tissue = models.Tissue()
    for i in tissue:
        setattr(db_tissue, i[0], i[1])
    database_session.add(db_tissue)
    database_session.commit()
    database_session.refresh(db_tissue)
    return db_tissue


def get_tissue_by_id(database_session: Session, tissue_id: int):
    """Get tissue by id"""
    return database_session.query(models.Tissue).filter(models.Tissue.id == tissue_id).first()
