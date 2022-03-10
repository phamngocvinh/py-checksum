#!/usr/bin/python3
import sys, os
import hashlib

VERSION = 'v1.0'


def main():
    print(f"PyChecksum-{VERSION}")
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    list_file = []

    for path, subdirs, files in os.walk(application_path):
        for name in files:
            list_file.append(os.path.join(path, name))

    input("Press enter to exit")


if __name__ == "__main__":
    main()