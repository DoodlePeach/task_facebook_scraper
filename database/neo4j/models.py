from neomodel import (StructuredNode, StringProperty, IntegerProperty, BooleanProperty, JSONProperty, ArrayProperty,
                      RelationshipTo, RelationshipFrom,
                      One)
from typing import List


class Comment(StructuredNode):
    comment_id: str = StringProperty(required=True)
    comment_image: str = StringProperty(default="")
    comment_text: str = StringProperty(default="")
    comment_time: str = StringProperty(default="")
    comment_url: str = StringProperty(default="")
    commenter_id: str = StringProperty(default="")
    commenter_meta: str = StringProperty(default="")
    commenter_name: str = StringProperty(default="")
    commenter_url: str = StringProperty(default="")

    post = RelationshipFrom('Comment', 'COMMENTS')

class Post(StructuredNode):
    available: bool = BooleanProperty(default=False)
    likes: int = IntegerProperty(default=0)
    shares: int = IntegerProperty(default=0)
    reactions: dict = JSONProperty(default={})
    reactors: List = ArrayProperty(default=[])
    text: str = StringProperty(default="")
    time: str = StringProperty(default="")
    images: List[str] = ArrayProperty(default=[])
    video: str = StringProperty(default="")

    profile = RelationshipFrom('Account', 'HAS_POSTED')
    comment = comments_link = RelationshipTo('Comment', 'COMMENTS')


class Account(StructuredNode):
    profile_id: int = IntegerProperty(required=True)
    name: str = StringProperty(required=True)
    profile_picture: str = StringProperty(default="")
    cover_photo_text: str = StringProperty(default="")
    cover_photo: str = StringProperty(default="")
    work: str = StringProperty(default="")
    places_lived: str = StringProperty(default="")
    education: str = StringProperty(default="")
    tag_line: str = StringProperty(default="")
    about: str = StringProperty(default="")
    life_events: str = StringProperty(default="")
    basic_info: dict = JSONProperty(default={})

    posts_link = RelationshipTo('Post', 'HAS_POSTED')
    friends = RelationshipTo('Account', 'HAS_FRIEND')
