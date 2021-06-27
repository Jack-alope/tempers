"""CRUD for Calibration Set"""

from sqlalchemy.orm import Session

import models

from schemas import schema_calibration_set


def create(database_session: Session,
           calibration_set: schema_calibration_set.CalibrationSet):
    db_calibration_set = models.CalibrationSet(**calibration_set)
    database_session.add(db_calibration_set)
    database_session.commit()
    database_session.refresh(db_calibration_set)
    return db_calibration_set


def get_calibration_sets(database_session: Session):
    return database_session.query(models.CalibrationSet).all()


def get_calibration_set_by_identifier(database_session: Session, cal_ident: str):
    return database_session.query(models.CalibrationSet).filter(
        models.CalibrationSet.calibration_set_identifier == cal_ident).first()


def update_calibration_set(database_session: Session, calibration_identifier: str,
                           calibration_factor: float):
    cal_set_db = get_calibration_set_by_identifier(
        database_session, calibration_identifier)

    if cal_set_db is None:
        cal_set_db = create(database_session,
                            {"calibration_set_identifier": calibration_identifier,
                             "calibration_factor": calibration_factor})
        database_session.add(cal_set_db)
    else:
        cal_set_db.calibration_factor = calibration_factor

    database_session.commit()
    database_session.refresh(cal_set_db)
    return cal_set_db
