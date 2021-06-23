from pydantic import BaseModel


class PostBase(BaseModel):
    post_number: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    left_post_height: float
    left_tissue_height: float
    right_post_height: float
    right_tissue_height: float
    radius: float


class Post(PostBase):
    bio_reactor_id: int
    id: int


class PostWithHeights(PostCreate):
    id: int
