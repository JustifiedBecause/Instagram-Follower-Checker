import json
from datetime import datetime
from pathlib import Path
from utils import mode_select, get_folder
from modes import *


def main():
    try:
        export_folder = None
        while not export_folder:
            export_folder = get_folder()

        while True:
            choice = mode_select()
            if choice == 9:
                print("Exiting...")
                return
            mode = MODES.get(choice)    
            if mode is None:
                print("Not a valid mode")
            else:    
                mode(export_folder).run()

    except KeyboardInterrupt:
        print("Exiting...")
        return


if __name__ == '__main__':
    main()
