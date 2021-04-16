"""
CRUD post 
Database interaction for posts
"""
from sqlalchemy.orm import Session

import models
from schemas import schema_post


def create_post(db: Session, post: schema_post.PostCreate, bio_reactor_id: int):

    db_post = models.Post()
    [setattr(db_post, i[0], i[1]) for i in post]
    db_post.bio_reactor_id = bio_reactor_id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post_by_num_and_bio(db: Session, bio_reactor_id: int, post_number: int):
    return db.query(models.Post).filter(models.Post.bio_reactor_id == bio_reactor_id,
                                        models.Post.post_number == post_number).first()
