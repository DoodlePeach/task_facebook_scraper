from containers.profile_dataclass import Profile
import database.neo4j.crud as neo_crud
import database.mongodb.crud as mongo_crud
from typing import List


class DatabaseRepository:
    @staticmethod
    def insert(profile: Profile, friends: List[Profile]):
        neo_crud.insert(profile, friends)
        mongo_crud.insert(profile, friends)
