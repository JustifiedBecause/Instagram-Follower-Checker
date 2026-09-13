from pathlib import Path
import json

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