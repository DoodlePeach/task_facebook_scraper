from dataclasses import dataclass, field

from containers.default_value import DefaultVal, NoneRefersDefault
from containers.post_dataclass import Posts
from typing import List


@dataclass
class Profile(NoneRefersDefault):
    id: int
    name: str
    profile_picture: str = DefaultVal("")
    cover_photo_text: str = DefaultVal("")
    cover_photo: str = DefaultVal("")
    work: str = DefaultVal("")
    places_lived: str = DefaultVal("")
    education: str = DefaultVal("")
    tag_line: str = DefaultVal("")
    about: str = DefaultVal("")
    life_events: str = DefaultVal("")
    basic_info: dict = DefaultVal({})
    posts: List[Posts] = DefaultVal([])
