"""
Schema for Bio Reactor
"""

from typing import List
from datetime import date

from pydantic import BaseModel

from . import schema_post


class BioReactorBase(BaseModel):
    date_added: date
    bio_reactor_number: int

    class Config:
        orm_mode = True


class BioReactorCreate(BioReactorBase):
    posts: List[schema_post.PostCreate]


class BioReactor(BioReactorBase):
    id: int
