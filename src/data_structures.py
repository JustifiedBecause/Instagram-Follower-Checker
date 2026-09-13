from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserFollower:
    username: str

def parse_follower(user: dict) -> UserFollower:
    username = user['string_list_data'][0]['value']
    return UserFollower(username)

def parse_following(user: dict) -> UserFollower:
    username = user['title']
    return UserFollower(username)

@dataclass
class PendingFollower:
    username: str
    days_since: int

def parse_pending_followers(user: dict) -> PendingFollower:
    days_since = (datetime.today() - datetime.fromtimestamp(user['timestamp'])).days
    username = next((label['value'] for label in user['label_values'] if label['label'] == 'Username'))
    return PendingFollower(username,days_since)