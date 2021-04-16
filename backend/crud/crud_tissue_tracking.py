"""
CRUD for tissue tracking data
used for all DB interation for the tissue tracking data
"""
from sqlalchemy.orm import Session

import pandas as pd

import models
import database


def create_tissue_tracking(db: Session, tissue_id: int, dataframe):
    db = database.SessionLocal()
    db.query(models.TissueTracking).filter(models.TissueTracking.tissue_id ==
                                           tissue_id).delete(synchronize_session=False)
    db.bulk_insert_mappings(models.TissueTracking,
                            dataframe.to_dict(orient="records"))
    db.commit()


def get_tracking_by_id(db: Session, tissue_id: int):
    query = db.query(models.TissueTracking).filter(
        models.TissueTracking.tissue_id == tissue_id).order_by(models.TissueTracking.time.asc())

    print(query.statement)
    return pd.read_sql_query(query.statement, db.bind)
