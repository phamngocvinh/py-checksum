#!/usr/bin/python3
from pickle import TRUE
import sys
import os
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

    is_hash_exists = os.path.exists(
        os.path.join(application_path, 'pychecksum.hash'))

    if not is_hash_exists:
        print('Generate Hash')
        generate_hash(application_path, sys.executable)
    else:
        print('Verify Hash')
        verify_file(application_path)

    input("Press enter to exit")
    return


def verify_file(path):

    passed_list = []
    failed_list = []
    file_path = ''
    is_next = False
    passed_md5 = False
    passed_sha256 = False
    passed_sha512 = False

    file_hash = open(os.path.join(path, 'pychecksum.hash'), 'r')
    lines = file_hash.readlines()
    for line in lines:
        line = line.strip()

        if line.startswith('@'):
            is_next = False
            file_target = open(line[1:], 'rb')
            content = file_target.read()

            md5 = hashlib.md5()
            md5.update(content)

            sha256 = hashlib.sha256()
            sha256.update(content)

            sha512 = hashlib.sha512()
            sha512.update(content)

            file_path = line[1:]

        elif is_next:
            continue

        elif line.startswith('md5:'):
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

        if passed_md5 and passed_sha256 and passed_sha512:
            passed_list.append(file_path)

    passed_list = list(dict.fromkeys(passed_list))

    file_result = open(os.path.join(path, 'check_result.txt'), 'w')

    file_result.write('PASSED:\n')
    for file in passed_list:
        file_result.write(f'{file}\n')
    file_result.write('\n\n')

    file_result.write('FAILED:\n')
    for file in failed_list:
        file_result.write(f'{file}\n')

    file_result.close()

    return


def generate_hash(path, appName):
    file_hash = open(os.path.join(path, 'pychecksum.hash'), 'w')

    for path, subdirs, files in os.walk(path):
        for name in files:
            if name == 'pychecksum.hash':
                continue
            elif name == os.path.basename(appName):
                continue

            file_path = os.path.join(path, name)
            file_target = open(file_path, 'rb')
            content = file_target.read()

            md5 = hashlib.md5()
            md5.update(content)

            sha256 = hashlib.sha256()
            sha256.update(content)

            sha512 = hashlib.sha512()
            sha512.update(content)

            file_hash.write(f'@{file_path}\n')
            file_hash.write(f'md5:{md5.hexdigest()}\n')
            file_hash.write(f'sha256:{sha256.hexdigest()}\n')
            file_hash.write(f'sha512:{sha512.hexdigest()}\n')
            file_hash.write('\n')

            print(f'Hashed: {file_path}')

    file_hash.close()
    return


if __name__ == "__main__":
    main()
