from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from containers.comment_dataclass import Comment
from containers.default_value import DefaultVal, NoneRefersDefault


@dataclass
class Posts(NoneRefersDefault):
    available: bool = DefaultVal(False)
    comments: List[Comment] = DefaultVal([])
    likes: int = DefaultVal(0)
    shares: int = DefaultVal(0)
    reactions: dict = DefaultVal({})
    reactors: List = DefaultVal([])
    text: str = DefaultVal("")
    # time is string, but the extraction process generates datetime objects.
    # So on initialization datetime objects are assigned to this field
    # and an post-initialization call converts that datetime object
    # into a string.
    time: str or datetime = DefaultVal("")
    images: List[str] = DefaultVal([])
    video: str = DefaultVal("")

    def __post_init__(self):
        if type(self.time) is not str and self.time is not None:
            self.time = self.time.isoformat()
