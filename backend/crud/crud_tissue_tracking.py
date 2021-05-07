"""
CRUD for tissue tracking data
used for all DB interation for the tissue tracking data
"""
from sqlalchemy.orm import Session

import pandas as pd

import models


def delete(database_session: Session, tissue_id: int):
    database_session.query(models.TissueTracking).filter(
        models.TissueTracking.tissue_id ==
        tissue_id).delete(synchronize_session=False)


def create_tissue_tracking(database_session: Session, tissue_id: int, dataframe):
    """
    Accepts the DB Session, tissue_id and a data frame
    Inserts tissue tracking data to databse
    """
    delete(database_session, tissue_id)
    database_session.bulk_insert_mappings(models.TissueTracking,
                                          dataframe.to_dict(orient="records"))
    database_session.commit()


def get_tracking_by_id(database_session: Session, tissue_id: int):
    """
    Gets all the tissue tracking data for a tissue
    returns the tissue data as a pandas df
    """
    query = database_session.query(models.TissueTracking).filter(
        models.TissueTracking.tissue_id == tissue_id).order_by(models.TissueTracking.time.asc())

    return pd.read_sql_query(query.statement, database_session.bind)
