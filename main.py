import json
from datetime import datetime

def main():
    mode = mode_select()
    if mode == 0:
        not_following_back()
    elif mode == 1:
        pending_followers()
    else:
        print("Not a valid mode")
        main()


######## MODE FUNCTIONS ########

#Generate lists of people you follow who don't follow back. Includes deactivated accounts
def not_following_back() -> None:
        follower_file = input("Enter Followers path: ")
        followers_json = load_file(follower_file)
        if not followers_json:
            print("Error loading follower file")
            return
        following_file = input("Enter Following path: ")
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

#List of pending follow requests and how long they've been pending
def pending_followers() -> None:
    pending_file = input("Enter Pending Followers path: ")
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
    

######## HELPER FUNCTIONS ########

#Datastructure is inconsistent, need to return the object and type
def load_file(path: str) -> dict | list | None:
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
        return int(input("""Mode?\n0) Not following back\n1) Pending Requests\n> """))
    except ValueError:
        return -1


if __name__ == '__main__':
    main()
    input("Press Enter to continue...")
