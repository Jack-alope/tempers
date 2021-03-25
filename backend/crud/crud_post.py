import logging

import models
from schemas import schema_post

from sqlalchemy.orm import Session


def create_post(db: Session, post: schema_post.PostCreate, bio_reactor_id: int):

    db_post = models.Post()
    [setattr(db_post, i[0], i[1]) for i in post]
    db_post.bio_reactor_id = bio_reactor_id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
