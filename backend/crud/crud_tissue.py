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
    return database_session.query(models.Tissue).filter(
        models.Tissue.id == tissue_id).first()


def get_tissue_number_by_id(tissue_id: int, database_session: Session):
    """returns tissue number for a tissue id"""
    return database_session.query(models.Tissue).filter(
        models.Tissue.id == tissue_id).first().tissue_number


def get_tissue_numbers_in_experiment(database_session: Session, experiment_id: int):
    """Returns tissues within an experiment"""
    tissues = database_session.query(models.Tissue).join(models.Video).filter(
        models.Video.experiment_id == experiment_id).distinct().all()

    return {tissue.tissue_number for tissue in tissues}


def get_frequency_by_tissue_id(tissue_id: int, database_session: Session):
    """Returns the Frequency by tissue id"""

    video_id = database_session.query(models.Tissue).filter(
        models.Tissue.id == tissue_id).first().vid_id

    return crud_video.get_frequency_by_id(database_session, video_id)


def get_tissues_by_experiemnt_and_tissue_number(database_session: Session,
                                                experiment_id: str, tissue_number: int):
    """Returns the tissues within an experiemnt with the same tissue number"""

    return database_session.query(models.Tissue,
                                  models.Video.frequency).join(models.Video).filter(
        models.Video.experiment_id == experiment_id,
        models.Tissue.tissue_number == tissue_number).order_by(models.Tissue.id).all()
