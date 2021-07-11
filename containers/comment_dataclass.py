from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from containers.default_value import DefaultVal, NoneRefersDefault


@dataclass
class Comment(NoneRefersDefault):
    comment_id: str
    comment_image: str = DefaultVal("")
    comment_text: str = DefaultVal("")
    # comment_time is string, but the extraction process generates datetime objects.
    # So on initialization datetime objects are assigned to this field
    # and an post-initialization call converts that datetime object
    # into a string.
    comment_time: str or datetime = DefaultVal("")
    comment_url: str = DefaultVal("")
    commenter_id: str = DefaultVal("")
    commenter_meta: str = DefaultVal("")
    commenter_name: str = DefaultVal("")
    commenter_url: str = DefaultVal("")
    replies: List = DefaultVal([])

    def __post_init__(self):
        if type(self.comment_time) is not str and self.comment_time is not None:
            self.comment_time = self.comment_time.isoformat()
