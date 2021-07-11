from config import NEO4J_DATABASE_URL
from containers.profile_dataclass import Profile
from database.neo4j.models import Account as ProfileModel, Post as PostModel, Comment as CommentModel
from dataclasses import asdict
from typing import List
from neomodel import config

config.DATABASE_URL = NEO4J_DATABASE_URL


def insert(profile: Profile, friends: List[Profile]):
    profile_neo = ProfileModel(profile_id=profile.id, name=profile.name, basic_info=profile.basic_info,
                               education=profile.education, cover_photo=profile.cover_photo,
                               places_lived=profile.places_lived, work=profile.work, about=profile.about,
                               profile_picture=profile.profile_picture, tag_line=profile.tag_line,
                               life_events=profile.life_events, cover_photo_text=profile.cover_photo_text).save()

    for post in profile.posts:
        post_neo = PostModel(**asdict(post)).save()
        profile_neo.posts_link.connect(post_neo)

        for comment in post.comments:
            comment_neo = CommentModel(**asdict(comment)).save()

            post_neo.comments_link.connect(comment_neo)

    for friend in friends:
        neo_friend = ProfileModel(profile_id=friend.id, name=friend.name, basic_info=friend.basic_info,
                                  education=friend.education, cover_photo=friend.cover_photo,
                                  places_lived=friend.places_lived, work=friend.work, about=friend.about,
                                  profile_picture=friend.profile_picture, tag_line=friend.tag_line,
                                  life_events=friend.life_events, cover_photo_text=friend.cover_photo_text).save()

        profile_neo.friends.connect(neo_friend)
