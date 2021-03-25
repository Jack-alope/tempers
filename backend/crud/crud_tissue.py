import logging

import models
from schemas import schema_tissue

from sqlalchemy.orm import Session


def create_tissue(db: Session, tissue: schema_tissue.TissueCreate):

    db_tissue = models.Tissue()
    [setattr(db_tissue, i[0], i[1]) for i in tissue]
    db.add(db_tissue)
    db.commit()
    db.refresh(db_tissue)
    return db_tissue

def get_tissue_by_id(db: Session, tissue_id: int):
    return db.query(models.Tissue).filter(models.Tissue.id == tissue_id).first()

def get_tissue_by_csv(db: Session, csv: str):
    return db.query(models.Tissue).filter(models.Tissue.csv_path==csv).first()

def add_tissue_csv(db: Session, tissue_id:int ,csv:str):
    tissue_object = get_tissue_by_id(db, tissue_id)

    tissue_object.csv_path = csv

    db.commit()
    db.refresh(tissue_object)

