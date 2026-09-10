import json
from datetime import datetime
from pathlib import Path


def main():
    try:
        export_folder = None
        while True:
            while not export_folder:
                export_folder = get_folder()
            mode = -1
            while mode < 0:
                mode = mode_select()
                if mode == 0:
                    not_following_back(export_folder)
                elif mode == 1:
                    pending_followers(export_folder)
                elif mode == 9:
                    print("Exiting...")
                    return
                else:
                    print("Not a valid mode")
                    mode = -1
    except KeyboardInterrupt:
        print("Exiting...")
        return


######## MODE FUNCTIONS ########

#Generate lists of people you follow who don't follow back. Includes deactivated accounts
def not_following_back(export_folder: Path) -> None:
        follower_file = export_folder / 'connections/followers_and_following/followers_1.json'
        if not follower_file.exists():
            print(f"Follower file at {follower_file} not found.")
            return
        followers_json = load_file(follower_file)
        if not followers_json:
            print("Error loading follower file")
            return
        following_file = export_folder / 'connections/followers_and_following/following.json'
        if not following_file.exists():
            print(f"Following file at {following_file} not found.")
            return
        following_json = load_file(following_file)
        if not following_json:
            print("Error loading following file")
            return

        followers = set(user['string_list_data'][0]['value'] for user in followers_json)
        following = set(user['title'] for user in following_json['relationships_following'])

        exclude = following - followers
        print("The following do not follow you back:")
        for ex in exclude:
            print(f"    {ex}")
        print()

#List of pending follow requests and how long they've been pending
def pending_followers(export_folder: Path) -> None:
    pending_file = export_folder / 'connections/followers_and_following/pending_follow_requests.json'
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
        time_since = td - datetime.fromtimestamp(float(user['timestamp']))
        username = next((label['value'] for label in user['label_values'] if label['label'] == 'Username'))
        pending.append((username,time_since))
    pending.sort(key=lambda x: x[1])
    column_width = max(len(item[0]) for item in pending)
    padding = 1
    print("Username  Days Since Request")
    print("-"*28)
    for p in pending:
        print(f"{p[0]} {p[1].days:>{column_width+padding-len(p[0])+len(str(p[1].days))}}")
    print()
    

######## HELPER FUNCTIONS ########

#Datastructure is inconsistent, need to return the object and type
def load_file(path: Path) -> dict | list | None:
    try:
        with open(path,'r') as f:
            js = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(e)
        return None
    return js

def mode_select() -> int:
    try:
        return int(input("""Mode?\n0) Not following back\n1) Pending Requests\n9) Exit\n> """))
    except ValueError:
        return -1

def get_folder() -> Path | None:
    path = Path(input("Path to export folder: ").strip('\"'))
    if not path.exists():
        print(f"{path} not found")
        return None
    return path


if __name__ == '__main__':
    main()
