"""
CRUD for tissues
"""

from sqlalchemy.orm import Session

import models
from schemas import schema_tissue
from crud import crud_post


def create_tissue(database_session: Session, tissue: schema_tissue.TissueCreate):
    """Create Tissue"""

    # TODO: add catch for error if there is no post on that bio
    """
    post_id = crud_post.get_post_by_num_and_bio(
        database_session, tissue.bio_reactor_id, tissue.post_number).id

    db_tissue = models.Tissue(post_id=post_id)
    """
    db_tissue = models.Tissue()
    print(tissue)
    [setattr(db_tissue, i[0], i[1]) for i in tissue]
    database_session.add(db_tissue)
    database_session.commit()
    database_session.refresh(db_tissue)
    return db_tissue


def get_tissue_by_id(database_session: Session, tissue_id: int):
    """Get tissue by id"""
    return database_session.query(models.Tissue).filter(models.Tissue.id == tissue_id).first()
