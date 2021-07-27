"""
CRUD for tissues
"""

from sqlalchemy.orm import Session

import models
from schemas import schema_tissue

from crud import crud_video


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


def get_tissue_number_by_id(tissue_id: int, database_session: Session):
    """returns tissue number for a tissue id"""
    return database_session.query(models.Tissue).filter(models.Tissue.id == tissue_id).first().tissue_number


def get_frequency_by_tissue_id(tissue_id: int, database_session: Session):
    """Returns the Frequency by tissue id"""

    video_id = database_session.query(models.Tissue).filter(
        models.Tissue.id == tissue_id).first().vid_id

    return crud_video.get_frequency_by_id(database_session, video_id)
