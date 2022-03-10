#!/usr/bin/python3
import sys, os

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

    
    idx = 0
    for root, dirs, files in os.walk(application_path):
        print('1')
        print(dirs)
        print(files)
        # print(os.path.join(dirs[idx]), files[idx])
        idx += 1

    input("Press enter to exit")


if __name__ == "__main__":
    main()