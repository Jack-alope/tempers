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
