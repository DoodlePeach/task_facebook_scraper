import json

from facebook_scraper import get_posts, set_cookies, get_profile, set_proxy, enable_logging

from config import *

from containers.post_dataclass import Posts
from containers.comment_dataclass import Comment
from containers.profile_dataclass import Profile

from database.database_repository import DatabaseRepository
from dataclasses import asdict

import logging
import time

set_cookies(COOKIE_FILE)
enable_logging(logging.INFO)

if PROXY is not None:
    set_proxy(PROXY)


# A post may contain threads of comments and their replies.
# This method parses out the replies of a top level comment
# down to the inner-most reply.
def recursive_reply_extraction(raw_comment_list: dict, comment: Comment):
    if raw_comment_list is not None and len(raw_comment_list) > 0:
        for raw_reply in raw_comment_list:
            reply = Comment(**raw_reply)
            reply.replies = []

            comment.replies.append(reply)

            if raw_reply.get('replies') is not None and len(raw_reply.get('replies')) > 0:
                for child_reply in raw_reply.get('replies'):
                    recursive_reply_extraction(child_reply, reply)


if __name__ == '__main__':
    posts = []

    logging.info("Retrieving posts")

    # start = time.time()
    fetched = list(get_posts(account=str(ROOT_NAME), pages=NUM_PAGES_TO_SCRAPE, timeout=30,
                        options={"comments": True, 'images': True, 'extra_info': True, 'reactors': True}))

    # logging.info(f"{len(posts)} posts retrieved in {round(time.time() - start, 2)}s")

    # Get the posts of a user.
    for raw_post in fetched:
        post = Posts(available=raw_post.get('available'), comments=[], likes=raw_post.get('likes'),
                     shares=raw_post.get('shares'), text=raw_post.get('text'), reactions=raw_post.get('reactions'),
                     reactors=raw_post.get('reactors'), time=raw_post.get('time'), images=raw_post.get('images'),
                     video=raw_post.get('video'))

        # Find out the comments of the post.
        if raw_post['comments_full'] is not None:
            for raw_comment in raw_post['comments_full']:
                comment = Comment(**raw_comment)
                comment.replies = []

                # Get the replies, and the replies of replies and so on.
                recursive_reply_extraction(raw_comment.get('replies'), comment)

                post.comments.append(comment)

        posts.append(post)

    # Extract profile information.
    extracted_profile = get_profile(str(ROOT_NAME), friends=20)

    logging.info("Retrieving basic information")
    start = time.time()

    # Finally consolidate everything together into a single object.
    profile = Profile(id=extracted_profile.get('id'), name=extracted_profile.get('Name'),
                      profile_picture=extracted_profile.get('profile_picture'),
                      tag_line=extracted_profile.get('tagline'),
                      places_lived=extracted_profile.get("Places lived"),
                      basic_info=extracted_profile.get("Basic info"),
                      life_events=extracted_profile.get("Life events"),
                      cover_photo=extracted_profile.get("cover_photo"),
                      cover_photo_text=extracted_profile.get("cover_photo_text"),
                      education=extracted_profile.get('Education'), work=extracted_profile.get('Work'),
                      about=extracted_profile.get('About'), posts=posts)

    friends = []

    for raw_friend in extracted_profile['Friends']:
        friends.append(Profile(id=raw_friend['id'], name=raw_friend['name'],
                               profile_picture=raw_friend['profile_picture']))

    logging.info(f"Basic information retrieved in {round(time.time() - start, 2)}s")

    # data = json.load(open('extracted.json', 'r'))
    #
    # profile = Profile(**data)
    # posts = profile.posts
    # profile.posts = []
    #
    # for post in posts:
    #     profile.posts.append(Posts(**post))

    logging.info("Uploading scraped data to database")
    start = time.time()

    DatabaseRepository.insert(profile, friends)

    logging.info(f"Uploaded data in {round(time.time() - start, 2)}s")

    if LOCAL_JSON_SAVE is not None:
        profile_json = json.dumps(asdict(profile))

        with open(LOCAL_JSON_SAVE, mode='w', encoding='utf-8') as outfile:
            outfile.write(profile_json)
