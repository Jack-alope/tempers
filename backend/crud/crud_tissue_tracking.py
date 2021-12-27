"""
CRUD for tissue tracking data
used for all DB interation for the tissue tracking data
"""
from sqlalchemy.orm import Session

import pandas as pd

import models


def _get_tracking_by_id_query(database_session: Session, tissue_id: int):
    return database_session.query(models.TissueTracking).filter(
        models.TissueTracking.tissue_id == tissue_id).order_by(models.TissueTracking.time.asc())


def _delete(database_session: Session, tissue_id: int):
    database_session.query(models.TissueTracking).filter(
        models.TissueTracking.tissue_id ==
        tissue_id).delete(synchronize_session=False)


def create_tissue_tracking(database_session: Session, tissue_id: int, dataframe):
    """
    Accepts the DB Session, tissue_id and a data frame
    Inserts tissue tracking data to databse
    """
    _delete(database_session, tissue_id)
    database_session.bulk_insert_mappings(models.TissueTracking,
                                          dataframe.to_dict(orient="records"))
    database_session.commit()

def update_smooth_force(database_session: Session, tissue_id: int, smooth_force: list):
    
    query = _get_tracking_by_id_query(database_session, tissue_id)

    for i, row in enumerate(query):
        row.smooth_force = smooth_force[i]

    database_session.commit()

def update_raw_force(database_session: Session, tissue_id: int, raw_force: list):
    
    query = _get_tracking_by_id_query(database_session, tissue_id)

    for i, row in enumerate(query):
        row.raw_force = raw_force[i]

    database_session.commit()

def update_smooth_disp(database_session: Session, tissue_id: int, smooth_disp: list):
    query = _get_tracking_by_id_query(database_session, tissue_id)

    for i, row in enumerate(query):
        row.smooth_disp = smooth_disp[i]

    database_session.commit()

def update_forces_disp(database_session: Session, tissue_id: int, smooth_force: list, raw_force: list, smooth_disp: list):

    
    query = _get_tracking_by_id_query(database_session, tissue_id)


    # REVIEW: feels like there could be a faster way but haven't found it.  
    for i, row in enumerate(query):
        row.smooth_force = smooth_force[i]
        row.raw_force = raw_force[i]
        row.smooth_disp_norm = smooth_disp[i]
    database_session.commit()



def get_tracking_by_id(database_session: Session, tissue_id: int):
    """
    Gets all the tissue tracking data for a tissue
    returns the tissue data as a pandas df
    """
    query = _get_tracking_by_id_query(database_session, tissue_id)

    return pd.read_sql_query(query.statement, database_session.bind)
