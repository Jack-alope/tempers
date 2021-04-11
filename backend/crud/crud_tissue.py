from sqlalchemy.orm import Session

import models
from schemas import schema_tissue
from crud import crud_post


def create_tissue(db: Session, tissue: schema_tissue.TissueCreate):

    # TODO: add catch for error if there is no post on that bio
    post_id = crud_post.get_post_by_num_and_bio(
        db, tissue.bio_reactor_id, tissue.post_number).id

    print(post_id)
    print(tissue)
    db_tissue = models.Tissue(post_id=post_id)
    [setattr(db_tissue, i[0], i[1]) for i in tissue]
    print(db_tissue)
    db.add(db_tissue)
    db.commit()
    db.refresh(db_tissue)
    return db_tissue


def get_tissue_by_id(db: Session, tissue_id: int):
    return db.query(models.Tissue).filter(models.Tissue.id == tissue_id).first()


def get_tissue_by_csv(db: Session, csv: str):
    return db.query(models.Tissue).filter(models.Tissue.csv_path == csv).first()


def add_tissue_csv(db: Session, tissue_id: int, csv: str):
    tissue_object = get_tissue_by_id(db, tissue_id)

    tissue_object.csv_path = csv

    db.commit()
    db.refresh(tissue_object)
