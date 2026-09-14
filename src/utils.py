from pathlib import Path
from zipfile import ZipFile
import json

def load_file_from_zip(zip_file: ZipFile, path: str) -> dict | list | None:
    try:
        with zip_file.open(path) as f:
            return json.load(f)
    except KeyError:
        print(f"File at {path} not found in the zip at {zip_file.filename}.")
        return None

def mode_select() -> int:
    try:
        return int(input("""Mode?\n0) Not Following Back\n1) Pending Requests\n9) Exit\n> """))
    except ValueError:
        return -1

def get_folder() -> Path | None:
    path = Path(input("Path to export zip: ").strip('\"'))
    if not path.exists():
        print(f"{path} not found")
        return None
    return path