#!/usr/bin/python3
from http.server import executable
from pickle import TRUE
import sys
import os
import hashlib

VERSION = 'v1.0'
HASHED_FILE = 'PyChecksum.hash'


def main():
    global output_path
    global application_path
    global executable_name

    print(f"PyChecksum-{VERSION}")
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    output_path = os.path.basename(os.path.normpath(application_path))
    executable_name = sys.executable

    is_hash_exists = os.path.exists(os.path.join(application_path,
                                                 HASHED_FILE))

    if not is_hash_exists:
        print('Generate Hash')
        generate_hash()
    else:
        print('Verify Hash')
        verify_file()

    input("Press enter to exit")
    return


def verify_file():

    passed_list = []
    failed_list = []
    file_path = ''
    is_next = False
    passed_md5 = False
    passed_sha256 = False
    passed_sha512 = False

    file_hash = open(os.path.join(application_path, HASHED_FILE), 'r')
    lines = file_hash.readlines()
    for line in lines:
        line = line.strip()

        if passed_md5 and passed_sha256 and passed_sha512:
            passed_list.append(file_path)

        if not line:
            continue

        if (line.startswith('md5:') or line.startswith('sha256:')
                or line.startswith('sha512:')) and is_next:
            continue
        else:
            is_next = False

        if line.startswith('md5:'):
            if line.split(':')[1] == md5.hexdigest():
                passed_md5 = True
            else:
                failed_list.append(file_path)
                is_next = True
        elif line.startswith('sha256:'):
            if line.split(':')[1] == sha256.hexdigest():
                passed_sha256 = True
            else:
                failed_list.append(file_path)
                is_next = True
        elif line.startswith('sha512:'):
            if line.split(':')[1] == sha512.hexdigest():
                passed_sha512 = True
            else:
                failed_list.append(file_path)
                is_next = True
        else:
            is_next = False
            file_target = open(os.path.join(application_path, line), 'rb')
            content = file_target.read()

            passed_md5 = False
            md5 = hashlib.md5()
            md5.update(content)

            passed_sha256 = False
            sha256 = hashlib.sha256()
            sha256.update(content)

            passed_sha512 = False
            sha512 = hashlib.sha512()
            sha512.update(content)

            file_path = line

    passed_list = list(dict.fromkeys(passed_list))

    file_result = open(os.path.join(application_path, 'PyCheckResult.txt'),
                       'w')

    file_result.write('PASSED:\n')
    for file in passed_list:
        file_result.write(f'{file}\n')
    file_result.write('\n\n')

    file_result.write('FAILED:\n')
    for file in failed_list:
        file_result.write(f'{file}\n')

    file_result.close()

    return


def generate_hash():
    file_hash = open(os.path.join(application_path, HASHED_FILE), 'w')

    for path, subdirs, files in os.walk(application_path):
        for name in files:
            if name == HASHED_FILE:
                continue
            elif name == os.path.basename(executable_name):
                continue

            if path == application_path:
                write_path = name
            else:
                write_path = os.path.join(
                    os.path.basename(os.path.normpath(path)), name)

            file_path = os.path.join(path, name)
            file_target = open(file_path, 'rb')
            content = file_target.read()

            md5 = hashlib.md5()
            md5.update(content)

            sha256 = hashlib.sha256()
            sha256.update(content)

            sha512 = hashlib.sha512()
            sha512.update(content)

            file_hash.write(f'{write_path}\n')
            file_hash.write(f'md5:{md5.hexdigest()}\n')
            file_hash.write(f'sha256:{sha256.hexdigest()}\n')
            file_hash.write(f'sha512:{sha512.hexdigest()}\n')
            file_hash.write('\n')

            print(f'Hashed: {file_path}')

    file_hash.close()
    return


if __name__ == "__main__":
    main()
