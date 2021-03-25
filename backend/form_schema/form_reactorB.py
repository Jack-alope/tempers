from typing import Optional, List, Any
from datetime import date
from pydantic import BaseModel, Field


class reactorB(BaseModel):
    date_recorded: date
    posts: List
    bio_reactor: str
    experiment_num: str
    file: Any
