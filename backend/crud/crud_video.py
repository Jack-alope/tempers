import logging
from dataclasses import asdict
from typing import List

import models
from schemas import schema_video

from sqlalchemy.orm import Session


def create_video(db: Session, video: schema_video.VideoCreate):
    db_video = models.Video()
    [setattr(db_video, i[0], i[1]) for i in video if i[0] != "tissues"]
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_all_vids(db: Session):
    result = []
    all_vids = db.query(models.Video).all()
    [result.append(asdict(row)) for row in all_vids]
    return result


def to_vid_show(row_vids: list):
    result = []
    for vid in row_vids:
        row_dict = dict(vid)
        show_vid = schema_video.VideoShow(row_dict.get("Video"))
        show_vid.bio_reactors_number = row_dict.get("bio_reactor_number")
        show_vid.experiment_idenifer = row_dict.get("experiment_idenifer")
        result.append(show_vid)

    return result


def get_videos(db: Session):
    # each vid is retuned as a tuple with the vid object, exp_idenifyer, bio_number
    result = db.query(models.Video, models.Experiment.experiment_idenifer, models.Bio_reactor.bio_reactor_number).join(
        models.Experiment).join(models.Bio_reactor).distinct(models.Video.id).all()

    def add_bio_and_exp_to_vid(tup):
        '''
        Accepts a tuple with a vid object, experiment_idenifer, bio_reactor_number
        Takes those vaules and addes them as attrubues of the vid object
        Returning the tup with the exp and bio attrubutes
        '''

        setattr(tup[0], "experiment_idenifer", tup[1])
        setattr(tup[0], "bio_reactor_number", tup[2])
        return tup[0]

    # the map fuctions is used to append the bio and exp attrubputs to the tissue object
    # retuens a list of vids with bio_number and exp_ideitfer
    return list(map(add_bio_and_exp_to_vid, result))


def delete_video(db: Session, vid_id: int):
    db_vid = get_vid_by_id(db, vid_id)
    if db_vid:
        db.delete(db_vid)
        db.commit()
        return True
    else:
        return False


def get_vid_by_id(db: Session, vid_id: int):
    return db.query(models.Video).filter(models.Video.id == vid_id).first()


def update_cal_cross(db: Session, video_id, cal_dist: float, cal_factor: float, cross_dist_passed: List):
    vid = get_vid_by_id(db, video_id)
    vid.calibration_distance = cal_dist
    vid.calibration_factor = cal_factor

    tissues = vid.tissues
    for i, tissue in enumerate(tissues):
        tissue.cross_section_dist = cross_dist_passed[i]

    db.commit()
    db.refresh(vid)
