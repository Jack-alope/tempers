"""
CRUD for Video
"""

from dataclasses import asdict
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func

import models
from schemas import schema_video


def create_video(database_session: Session, video: schema_video.VideoCreate):
    """Adds vid to DB"""
    db_video = models.Video()
    for i in video:
        if i[0] != "tissues":
            setattr(db_video, i[0], i[1])

    database_session.add(db_video)
    database_session.commit()
    database_session.refresh(db_video)
    return db_video


def get_all_vids(database_session: Session):
    """Returns all vids"""
    return [asdict(row) for row in database_session.query(models.Video).all()]


def to_vid_show(row_vids: list):
    """
    not sure
    """
    result = []
    for vid in row_vids:
        row_dict = dict(vid)
        show_vid = schema_video.VideoShow(row_dict.get("Video"))
        show_vid.bio_reactors_number = row_dict.get("bio_reactor_number")
        show_vid.experiment_idenifer = row_dict.get("experiment_idenifer")
        result.append(show_vid)

    return result


def get_videos(database_session: Session):
    """
    Returns all vids
    """
    # each vid is retuned as a tuple with the vid object, exp_idenifyer, bio_number
    result = (
        database_session.query(
            models.Video, models.Experiment.id, models.BioReactor.bio_reactor_number
        )
        .join(models.Experiment)
        .join(models.BioReactor)
        .distinct(models.Video.id)
        .all()
    )

    def add_bio_and_exp_to_vid(tup):
        """
        Accepts a tuple with a vid object, experiment_idenifer, bio_reactor_number
        Takes those vaules and addes them as attrubues of the vid object
        Returning the tup with the exp and bio attrubutes
        """

        setattr(tup[0], "experiment_id", tup[1])
        setattr(tup[0], "bio_reactor_number", tup[2])
        return tup[0]

    # the map fuctions is used to append the bio and exp attrubputs to the tissue object
    # retuens a list of vids with bio_number and exp_ideitfer
    return list(map(add_bio_and_exp_to_vid, result))


def delete_video(database_session: Session, vid_id: int):
    """Delete vid by id"""
    try:
        vid_info = get_vid_by_id(database_session, vid_id)
        models.delete_file(vid_info.save_location)
        database_session.delete(vid_info)
        database_session.commit()
        return True
    except IntegrityError:
        return False


def get_vid_by_id(database_session: Session, vid_id: int):
    """return vid by id"""
    return (
        database_session.query(models.Video).filter(models.Video.id == vid_id).first()
    )


def update_cal_cross(
    database_session: Session, video_id, cal_identifer, cross_dist_passed: List
):
    """update calibration and cross section distance"""
    vid = get_vid_by_id(database_session, video_id)

    vid.calibration_set_identifier = cal_identifer

    tissues = vid.tissues
    for i, tissue in enumerate(tissues):
        tissue.cross_section_dist = cross_dist_passed[i]

    database_session.commit()
    database_session.refresh(vid)


def update_tracked_status(database_session: Session, vid_id: int, tracked_status: bool):
    """Updates the tracked status of a vid by id"""
    video = get_vid_by_id(database_session, vid_id)
    video.tracked = tracked_status
    database_session.commit()
    database_session.refresh(video)


def update_save_location(database_session: Session, video_id: int, save_location: str):
    """Added save location to Vid by id"""
    vid = get_vid_by_id(database_session, video_id)

    vid.save_location = save_location

    database_session.commit()
    database_session.refresh(vid)
    return vid


def video_anaylized(database_session: Session, vid_id: int):
    """Sets anaylized to true for vid by id"""
    vid = get_vid_by_id(database_session, vid_id)
    vid.anaylized = True
    database_session.commit()
    database_session.refresh(vid)


def get_next_video_id(database_session: Session):
    """Returns what the next vid id will be"""
    return database_session.query(func.max(models.Video.id)).scalar() + 1


def get_frequency_by_id(database_session: Session, vid_id: int):
    return (
        database_session.query(models.Video)
        .filter(models.Video.id == vid_id)
        .first()
        .frequency
    )
