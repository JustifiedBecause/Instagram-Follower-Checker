from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from utils import load_file, get_folder
from data_structures import *

class Mode(ABC):
    def __init__(self, path: Path):
        self.export_zip = path

    @abstractmethod
    def run(self):
        raise NotImplementedError("Mode is an abstract class. Derive and Override the run() method.")

class NotFollowingBackMode(Mode):
    def run(self):
        follower_file = self.export_zip / 'connections/followers_and_following/followers_1.json'
        if not follower_file.exists():
            print(f"Follower file at {follower_file} not found.")
            return
        followers_json = load_file(follower_file)
        if not followers_json:
            print("Error loading follower file")
            return
        following_file = self.export_zip / 'connections/followers_and_following/following.json'
        if not following_file.exists():
            print(f"Following file at {following_file} not found.")
            return
        following_json = load_file(following_file)
        if not following_json:
            print("Error loading following file")
            return

        followers = [parse_follower(user) for user in followers_json]
        following = [parse_following(user) for user in following_json['relationships_following']]

        exclude = [x for x in following if x not in followers]
        print("These users do not follow you back:")
        for ex in exclude:
            print(f"    {ex.username}")
        print()

class PendingFollowersMode(Mode):
    def run(self):
        pending_file = self.export_zip / 'connections/followers_and_following/pending_follow_requests.json'
        if not pending_file.exists():
            print(f"Follower file at {pending_file} not found.")
            return
        pending_json = load_file(pending_file)
        if not pending_json:
            print("Error loading pending file")
            return
        td = datetime.now()
        pending = []
        print("Pending follow requests:")
        for user in pending_json:
            pending.append(parse_pending_followers(user))
        pending.sort(key=lambda x: x.days_since)
        column_width = max(len(item.username) for item in pending)
        padding = 1
        print("Username  Days Since Request")
        print("-"*28)
        for p in pending:
            print(f"{p.username} {p.days_since:>{column_width+padding-len(p.username)+len(str(p.days_since))}}")
        print()


# Mode Menu Numbers
# 9 is reserved for Exit, do not place in this table
MODES = {
    0: NotFollowingBackMode,
    1: PendingFollowersMode
}