from dataclasses import asdict

from config import MONGO_DATABASE_URL
from containers.profile_dataclass import Profile
from typing import List
from pymongo import MongoClient


def insert(profile: Profile, friends: List[Profile]):
    client = MongoClient(MONGO_DATABASE_URL)

    db = client['scraping']
    collection = db['profiles']

    dict_profile = asdict(profile)

    dict_profile['Friends'] = []

    for friend in friends:
        dict_profile['Friends'].append(asdict(friend))

    collection.insert_one(dict_profile)
