"""
Database models for rianu
"""

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
    """Experiment model for DB"""
    __tablename__ = "experiment"

    id: int = Column(Integer, primary_key=True)
    experiment_idenifer: String = Column(
        String(120), nullable=False, unique=True)
    start_date: Date = Column(Date, nullable=True, default=datetime.now(tz))

    vids: List = relationship("Video", back_populates="experiment")


@dataclass
class Video(Base):
    """Video model for DB"""
    __tablename__ = "video"

    id: int = Column(Integer, primary_key=True)

    date_uploaded: Date = Column(
        Date, nullable=False, default=datetime.now(tz))
    date_recorded: Date = Column(Date, nullable=False)
    frequency: float = Column(Float, nullable=False)

    calibration_distance: float = Column(Float, nullable=True)

    calibration_factor: float = Column(Float, nullable=True)

    save_location: String = Column(String(120), nullable=True)

    experiment_id: int = Column(Integer, ForeignKey('experiment.id'))
    experiment = relationship("Experiment", back_populates="vids")

    bio_reactor_id: int = Column(Integer, ForeignKey('bio_reactor.id'))
    bio_reactor = relationship("BioReactor", back_populates="vids")

    tissues = relationship("Tissue", back_populates="video",
                           cascade="all, delete-orphan")


@dataclass
class Tissue(Base):
    """Tissie model for DB"""
    __tablename__ = "tissue"

    id: int = Column(
        Integer, primary_key=True, autoincrement=True)
    tissue_number: int = Column(Integer, nullable=False)
    tissue_type: str = Column(String(120), nullable=False)
    # REVIEW: maybe this should be a relationship
    post_number: int = Column(Integer, nullable=False)
    cross_section_dist: float = Column(Float, nullable=True)

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates="tissues")

    vid_id = Column(Integer, ForeignKey('video.id'))
    video = relationship("Video", back_populates="tissues")

    tissue_tracking = relationship(
        "TissueTracking", back_populates="tissue",
        cascade="all, delete-orphan", passive_deletes=True)
    tissue_caculated_data = relationship(
        "TissueCalculatedData", back_populates="tissue",
        cascade="all, delete-orphan", passive_deletes=True)


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


class TissueCalculatedData(Base):
    """Tissue Cacualtion data model for DB"""
    __tablename__ = "tissue_calculated_data"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    tissue_id: int = Column(Integer, ForeignKey(
        "tissue.id", ondelete="CASCADE"))
    tissue = relationship("Tissue", back_populates="tissue_caculated_data")

    dev_force: float = Column(Float)
    dev_force_std: float = Column(Float)
    dias_force: float = Column(Float)
    dias_force_std: float = Column(Float)
    beat_rate_COV: float = Column(Float)
    beat_rate_COV_std = Column(Float)
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

    date_added: datetime.date = Column(Date, nullable=False)

    vids = relationship("Video", back_populates="bio_reactor")

    posts = relationship("Post", back_populates="bio_reactor",
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

    bio_reactor_id = Column(Integer, ForeignKey("bio_reactor.id"))
    bio_reactor = relationship("BioReactor", back_populates="posts")

    tissues = relationship("Tissue", back_populates="post")


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
            print("The file does not exist")
