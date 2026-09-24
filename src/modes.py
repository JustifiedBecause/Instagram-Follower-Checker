from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from zipfile import ZipFile
from utils import load_file_from_zip
from data_structures import *

class Mode(ABC):
    def __init__(self, path: Path):
        self.export_zip = ZipFile(path,'r')

    @abstractmethod
    def run(self):
        raise NotImplementedError("Mode is an abstract class. Derive and Override the run() method.")

class NotFollowingBackMode(Mode):
    def run(self):
        followers_json = load_file_from_zip(self.export_zip,'connections/followers_and_following/followers_1.json')
        following_json = load_file_from_zip(self.export_zip, 'connections/followers_and_following/following.json')
        if not following_json:
            print("Error loading following file")
            return
        followers = [UserFollower.parse_follower(user) for user in followers_json]
        following = [UserFollower.parse_following(user) for user in following_json['relationships_following']]
        exclude = [x for x in following if x not in followers]
        print("These users do not follow you back:")
        for ex in exclude:
            print(f"    {ex.username}")
        print()

class PendingFollowersMode(Mode):
    def run(self):
        pending_json = load_file_from_zip(self.export_zip, 'connections/followers_and_following/pending_follow_requests.json')
        if not pending_json:
            print("Error loading pending file")
            return
        td = datetime.now()
        pending = []
        print("Pending follow requests:")
        for user in pending_json:
            pending.append(PendingFollower.parse_pending_followers(user))
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