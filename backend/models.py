from datetime import datetime
from dataclasses import dataclass
from typing import List
import os

from pytz import timezone
from sqlalchemy import (Column, Date, ForeignKey, Integer,
                        String, Float)
from sqlalchemy.orm import relationship

from database import Base

    

tz = timezone('EST')


# TODP: Move this to diffent file
UPLOAD_FOLDER = "static/uploads"


@dataclass
class Experiment(Base):
    __tablename__ = "experiment"

    id: int = Column(Integer, primary_key=True)
    experiment_idenifer: String = Column(
        String(120), nullable=False, unique=True)
    start_date: Date = Column(Date, nullable=True, default=datetime.now(tz))

    vids: List = relationship("Video", back_populates="experiment")


@dataclass
class Video(Base):
    __tablename__ = "video"

    id: int = Column(Integer, primary_key=True)

    date_uploaded: Date = Column(
        Date, nullable=False, default=datetime.now(tz))
    date_recorded: Date = Column(Date, nullable=False)
    frequency: float = Column(Float, nullable=False)

    # bio_reactor_number = Column(Integer, nullable=True)

    calibration_distance: float = Column(Float, nullable=True)

    calibration_factor: float = Column(Float, nullable=True)

    save_location: String = Column(String(120), nullable=True)

    experiment_id: int = Column(Integer, ForeignKey('experiment.id'))
    experiment = relationship("Experiment", back_populates="vids")

    bio_reactor_id: int = Column(Integer, ForeignKey('bio_reactor.id'))
    bio_reactor = relationship("Bio_reactor", back_populates="vids")

    tissues = relationship("Tissue", back_populates="video")


@dataclass
class Tissue(Base):
    __tablename__ = "tissue"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    tissue_number: int = Column(Integer, nullable=False)
    tissue_type: str = Column(String(120), nullable=False)
    # REVIEW: maybe this should be a relationship
    post_number: int = Column(Integer, nullable=False)
    csv_path: str = Column(String(120), nullable=True)
    cross_section_dist: float = Column(Float, nullable=True)

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates="tissues")

    vid_id = Column(Integer, ForeignKey('video.id'))
    video = relationship("Video", back_populates="tissues")


@dataclass
class Bio_reactor(Base):
    __tablename__ = "bio_reactor"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    bio_reactor_number: int = Column(Integer, nullable=False)

    date_added: datetime.date = Column(Date, nullable=False)

    vids = relationship("Video", back_populates="bio_reactor")

    posts = relationship("Post", back_populates="bio_reactor")


@dataclass
class Post(Base):
    __tablename__ = "post"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    post_number: int = Column(Integer, nullable=False)

    left_post_height: float = Column(Float, nullable=False)
    left_tissue_height: float = Column(Float, nullable=False)
    right_post_height: float = Column(Float, nullable=False)
    right_tissue_height: float = Column(Float, nullable=False)
    radius: float = Column(Float, nullable=True)

    bio_reactor_id = Column(Integer, ForeignKey("bio_reactor.id"))
    bio_reactor = relationship("Bio_reactor", back_populates="posts")

    tissues = relationship("Tissue", back_populates="post")


def check_path_exisits(file_path_passed):
    # TODO: move this to diffrent file
    if not os.path.exists(file_path_passed):
        os.makedirs(file_path_passed)
