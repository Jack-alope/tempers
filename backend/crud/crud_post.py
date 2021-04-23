"""
CRUD post
Database interaction for posts
"""
from sqlalchemy.orm import Session

import models
from schemas import schema_post


def create_post(database_session: Session, post: schema_post.PostCreate, bio_reactor_id: int):
    """Create Post"""

    db_post = models.Post()
    for i in post:
        setattr(db_post, i[0], i[1])
    db_post.bio_reactor_id = bio_reactor_id
    database_session.add(db_post)
    database_session.commit()
    database_session.refresh(db_post)
    return db_post


def get_post_by_num_and_bio(database_session: Session, bio_reactor_id: int, post_number: int):
    """Get post object by number and bio number"""
    return database_session.query(models.Post).filter(
        models.Post.bio_reactor_id == bio_reactor_id,
        models.Post.post_number == post_number).first()


def get_posts_by_bio_id(database_session: Session, bio_reactor_id: int):
    """Returns posts in a bio reactor"""
    return database_session.query(models.Post).filter(
        models.Post.bio_reactor_id == bio_reactor_id).all()
