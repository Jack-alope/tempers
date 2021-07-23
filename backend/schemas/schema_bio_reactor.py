"""
Schema for Bio Reactor
"""

from typing import List
from datetime import date

from pydantic import BaseModel
from typing import Optional

from . import schema_post


class BioReactorBase(BaseModel):
    date_added: date
    bio_reactor_number: int
    post_distance: Optional[float]
    youngs_modulus: Optional[float]

    class Config:
        orm_mode = True


class BioReactorCreate(BioReactorBase):
    posts: List[schema_post.PostCreate]


class BioReactor(BioReactorBase):
    id: int


class BioReactorWithPosts(BioReactorBase):
    id: int
    posts: List[schema_post.PostWithHeights]
