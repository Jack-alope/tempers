"""
Database models for rianu
"""

from datetime import datetime
from dataclasses import dataclass
from typing import List
import os
import logging

from pytz import timezone
from sqlalchemy import (Column, Date, ForeignKey, Integer,
                        String, Float)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from database import Base

from schemas import schema_tissue, schema_tissue_calculated_data,\
    schema_video, schema_post

tz = timezone('EST')


UPLOAD_FOLDER = "static/uploads"


@dataclass
class Experiment(Base):
    """Experiment model for DB"""
    __tablename__ = "experiment"

    id: str = Column(String(120), primary_key=True)
    start_date: Date = Column(Date, nullable=True, default=datetime.now(tz))

    vids: List[schema_video.Video] = relationship(
        "Video", back_populates="experiment", cascade="all, delete-orphan")


@dataclass
class Video(Base):
    """Video model for DB"""
    __tablename__ = "video"

    id: int = Column(Integer, primary_key=True)

    date_uploaded: Date = Column(
        Date, nullable=False, default=datetime.now(tz))
    date_recorded: Date = Column(Date, nullable=False)
    frequency: float = Column(Float, nullable=False)

    save_location: str = Column(String(120), nullable=True)
    video_note: str = Column(String(240), nullable=True)

    tracked: bool = Column(Boolean, nullable=True, default=False)
    anaylized: bool = Column(Boolean, nullable=True, default=False)

    experiment_id: str = Column(String(120), ForeignKey('experiment.id'))
    experiment = relationship("Experiment", back_populates="vids")

    bio_reactor_id: int = Column(Integer, ForeignKey('bio_reactor.id'))
    bio_reactor = relationship("BioReactor", back_populates="vids")

    calibration_set_identifier: str = Column(
        String(120), ForeignKey('calibration_set.calibration_set_identifier'))
    calibration_set = relationship("CalibrationSet", back_populates="videos")

    tissues: List[schema_tissue.Tissue] = relationship(
        "Tissue", back_populates="video", cascade="all, delete-orphan")


@dataclass
class CalibrationSet(Base):
    """Calibration set for DB"""
    __tablename__ = "calibration_set"

    calibration_set_identifier: str = Column(
        String(120), primary_key=True, nullable=False, unique=True)
    calibration_factor: float = Column(Float, nullable=False)

    videos: List[schema_video.Video] = relationship(
        "Video", back_populates="calibration_set")


@dataclass
class Tissue(Base):
    """Tissie model for DB"""
    __tablename__ = "tissue"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    tissue_number: int = Column(Integer, nullable=False)
    tissue_type: str = Column(String(120), nullable=False)
    cross_section_dist: float = Column(Float, nullable=True)

    post_id: int = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates="tissues")

    vid_id = Column(Integer, ForeignKey('video.id'))
    video = relationship("Video", back_populates="tissues")

    tissue_tracking = relationship(
        "TissueTracking", back_populates="tissue", uselist=False,
        cascade="all, delete-orphan", passive_deletes=True)
    tissue_caculated_data: \
        schema_tissue_calculated_data.TissueCalculatedDataBase = \
        relationship(
            "TissueCalculatedData", back_populates="tissue", uselist=False,
            cascade="all, delete-orphan", passive_deletes=True)


@dataclass
class TissueTracking(Base):
    """Tissue Tracking model for DB"""
    __tablename__ = "tissue_tracking"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    tissue_id: int = Column(Integer, ForeignKey(
        "tissue.id", ondelete="CASCADE"))
    tissue = relationship("Tissue", back_populates="tissue_tracking")

    time: float = Column(Float)
    displacement: float = Column(Float)
    odd_x: float = Column(Float)
    odd_y: float = Column(Float)
    even_x: float = Column(Float)
    even_y: float = Column(Float)


@dataclass
class TissueCalculatedData(Base):
    """Tissue Cacualtion data model for DB"""
    __tablename__ = "tissue_calculated_data"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    tissue_id: int = Column(Integer, ForeignKey(
        "tissue.id", ondelete="CASCADE"))
    tissue = relationship("Tissue", back_populates="tissue_caculated_data")

    dev_force: float = Column(Float)
    dev_force_std: float = Column(Float)
    sys_force: float = Column(Float)
    sys_force_std: float = Column(Float)
    dias_force: float = Column(Float)
    dias_force_std: float = Column(Float)
    beat_rate_cov: float = Column(Float)
    beating_freq: float = Column(Float)
    beating_freq_std: float = Column(Float)
    t2pk: float = Column(Float)
    t2pk_std: float = Column(Float)
    t2rel50: float = Column(Float)
    t2rel50_std: float = Column(Float)
    t2rel80: float = Column(Float)
    t2rel80_std: float = Column(Float)
    t2rel90: float = Column(Float)
    t2rel90_std: float = Column(Float)
    t50: float = Column(Float)
    t50_std: float = Column(Float)
    c50: float = Column(Float)
    c50_std: float = Column(Float)
    r50: float = Column(Float)
    r50_std: float = Column(Float)
    dfdt: float = Column(Float)
    dfdt_std: float = Column(Float)
    negdfdt: float = Column(Float)
    negdfdt_std: float = Column(Float)


@dataclass
class BioReactor(Base):
    """Bio Reactor model for DB"""
    __tablename__ = "bio_reactor"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    bio_reactor_number: int = Column(Integer, nullable=False)

    date_added: Date = Column(Date, nullable=False)
    bio_reactor_note: str = Column(String(240), nullable=True)
    post_distance: Float = Column(Float, nullable=True)
    youngs_modulus: Float = Column(Float, nullable=True)

    vids: List[schema_video.Video] = relationship(
        "Video", back_populates="bio_reactor")

    posts: List[schema_post.Post] = relationship(
        "Post", back_populates="bio_reactor",
        cascade="all, delete-orphan")


@dataclass
class Post(Base):
    """Post model for DB"""
    __tablename__ = "post"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    post_number: int = Column(Integer, nullable=False)

    left_post_height: float = Column(Float, nullable=False)
    left_tissue_height: float = Column(Float, nullable=False)
    right_post_height: float = Column(Float, nullable=False)
    right_tissue_height: float = Column(Float, nullable=False)
    radius: float = Column(Float, nullable=True)

    bio_reactor_id: int = Column(Integer, ForeignKey("bio_reactor.id"))
    bio_reactor = relationship("BioReactor", back_populates="posts")

    tissues: List[schema_tissue.Tissue] = relationship(
        "Tissue", lazy='noload', back_populates="post")


def check_path_exisits(file_path_passed):
    """Make sure tha file path exisits"""
    if not os.path.exists(file_path_passed):
        os.makedirs(file_path_passed)


def delete_empties():
    """Deletes empty folders within the upload folder"""
    for (root, dirs, files) in os.walk('static/uploads/', topdown=False):
        if root == 'static/uploads/':
            break
        if not os.listdir(root):
            os.rmdir(root)


def delete_file(path):
    """Deletes path if exists"""

    if path is not None:
        if os.path.exists(path):
            os.remove(path)
            delete_empties()
        else:
            logging.info("The file does not exist")
