from typing import List

from pydantic import BaseModel


class PostBase(BaseModel):
    post_number: int
    left_post_height: float
    left_tissue_height: float
    right_post_height: float
    right_tissue_height: float

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    bio_reactor_id: int


class Post(PostBase):
    id: int
