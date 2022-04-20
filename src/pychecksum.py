#!/usr/bin/python3
# Copyright (C) 2022  Pham Ngoc Vinh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import sys
import os
import hashlib
import getopt
import requests
from progress.bar import IncrementalBar

VERSION = 'v1.1.0'
HASHED_FILE = 'PyChecksum.hash'
RESULT_FILE = 'PyCheckResult.txt'
HELP_TEXT = """
Usage:
    PyChecksum.exe [option] [command]

Options:
    -h  --help          Show this help message
    -v  --version       Show current version
    -u  --update        Check for update

Commands:
    -f  --folder        Specify target folder
    -a  --algorithm     Specify hash algorithm, seperated by comma

Available Algorithm:
    MD5
    SHA256
    SHA512
    SHA3-256
    SHA3-512
    BLAKE2b
    BLAKE2s
"""


# Process Bar
class ProcessBar(IncrementalBar):
    message = 'Loading'
    suffix = '%(percent)d%% [%(index)d/%(max)d] - %(eta_td)s'


# Main process
def main(argv):

    global application_path
    global executable_name
    global algorithm_options
    global is_user_set_algorithm

    application_path = ''
    is_update = False
    is_user_set_path = False
    is_user_set_algorithm = False

    # Get user input command
    try:
        opts, args = getopt.getopt(
            argv, "hvuf:a:",
            ["help", "version", "update", "folder=", "algorithm="])
    except getopt.GetoptError:
        print('Use PyChecksum.exe -h or --help for more informations')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(HELP_TEXT)
            sys.exit()
        elif opt in ("-v", "--version"):
            print(VERSION)
            sys.exit()
        elif opt in ("-u", "--update"):
            is_update = True
        elif opt in ("-f", "--folder"):
            application_path = arg.strip()
            is_user_set_path = True
        elif opt in ("-a", "--algorithm"):
            algorithm_options = arg.strip().lower().split(',')
            is_user_set_algorithm = True

    # Check for Application update
    if is_update:
        update_app()
        sys.exit()

    print(f'PyChecksum-{VERSION} Copyright (C) 2022  Pham Ngoc Vinh')
    license_info = """
    This program comes with ABSOLUTELY NO WARRANTY;
    This is free software, and you are welcome to redistribute it
    under certain conditions;
    """
    print(license_info)

    # If run as exe
    if getattr(sys, 'frozen', False):
        # If path is not set by argument,
        # get execution file path
        if len(application_path) == 0:
            application_path = os.path.dirname(sys.executable)
        executable_name = sys.executable
    else:  # If run as script
        # If path is not set by argument,
        # get execution file path
        if len(application_path) == 0:
            application_path = os.path.dirname(os.path.abspath(__file__))
        executable_name = os.path.basename(__file__)

    # Check valid algorithm
    if is_user_set_algorithm and len(algorithm_options) == 0:
        print('Error: No algorithm was specified')
        input('Press enter to exit')
        return

    # Check valid directory
    if not os.path.isdir(application_path):
        print('Warning: Invalid folder path')
        input('Press enter to exit')
        return

    # Check for empty directory
    files = os.listdir(application_path)
    if not is_user_set_path:
        if len(files) == 1:
            print('Warning: Directory is empty')
            input('Press enter to exit')
            return
    else:
        if len(files) == 0:
            print('Warning: Directory is empty')
            input('Press enter to exit')
            return

    # Check if hashed file exists
    is_hash_exists = os.path.exists(os.path.join(application_path,
                                                 HASHED_FILE))

    # If hashed file not exists, run Generate hash
    if not is_hash_exists:
        print('Generate Hashes')
        generate_hash()
    # If hashed file exists, run Verify hash
    else:
        print('Verify Hashes')
        verify_file()

    print('\rOK')
    input('\rPress enter to exit')
    return


# Check for application update
def update_app():
    response = requests.get(
        "https://api.github.com/repos/phamngocvinh/py-checksum/releases/latest"
    )
    latest_version = response.json()["tag_name"]
    if latest_version > VERSION:
        print(f'Current version: {VERSION}')
        print(f'New version availible: {latest_version}')
        print(
            'Download link: https://github.com/phamngocvinh/py-checksum/releases/latest'
        )
    else:
        print('You\'re using the latest version')


# Run verify process
def verify_file():

    passed_list = []
    failed_list = []

    # File path for writing result.
    # Cannot use line in loop because line
    # will be replace with new value when write.
    file_path = ''

    # If one hash is not matched,
    # don't need to check other.
    # Skip to next file
    is_next = False

    is_passed_md5 = False
    is_passed_sha256 = False
    is_passed_sha512 = False
    is_passed_sha3_256 = False
    is_passed_sha3_512 = False
    is_passed_blake2b = False
    is_passed_blake2s = False

    is_check_md5 = False
    is_check_sha256 = False
    is_check_sha512 = False
    is_check_sha3_256 = False
    is_check_sha3_512 = False
    is_check_blake2b = False
    is_check_blake2s = False

    # Open hashed files list
    file_hash = open(os.path.join(application_path, HASHED_FILE), 'r')

    # Read entire file
    lines = file_hash.readlines()

    # Get all files count
    bar_count = 0
    for line in lines:
        line = line.strip()
        if (line.startswith('sha256:') or line.startswith('sha512:')
                or line.startswith('sha3-256:') or line.startswith('sha3-512:')
                or line.startswith('blake2b:') or line.startswith('blake2s:')
                or line.startswith('md5:')):
            bar_count += 1

    # Process bar
    bar = ProcessBar('Processing', max=bar_count)

    for line in lines:
        line = line.strip()

        # If empty line
        if not line:
            if len(file_path) != 0:
                # Check result
                is_check_ok = True
                if is_check_md5 and not is_passed_md5:
                    is_check_ok = False
                if is_check_sha256 and not is_passed_sha256:
                    is_check_ok = False
                if is_check_sha512 and not is_passed_sha512:
                    is_check_ok = False
                if is_check_sha3_256 and not is_passed_sha3_256:
                    is_check_ok = False
                if is_check_sha3_512 and not is_passed_sha3_512:
                    is_check_ok = False
                if is_check_blake2b and not is_passed_blake2b:
                    is_check_ok = False
                if is_check_blake2s and not is_passed_blake2s:
                    is_check_ok = False
                if is_check_ok:
                    passed_list.append(file_path)
                    is_passed_md5 = False
                    is_passed_sha256 = False
                    is_passed_sha512 = False
                    is_passed_sha3_256 = False
                    is_passed_sha3_512 = False
                    is_passed_blake2b = False
                    is_passed_blake2s = False
                continue

        # If already failed one check, skip others
        if (line.startswith('sha256:') or line.startswith('sha512:')
                or line.startswith('sha3-256:') or line.startswith('sha3-512:')
                or line.startswith('blake2b:') or line.startswith('blake2s:')
                or line.startswith('md5:')) and is_next:
            continue
        # If line is file name
        else:
            is_next = False

        if line.startswith('md5:'):
            is_check_md5 = True
            md5 = hashlib.md5()
            md5.update(content)

            if line.split(':')[1] == md5.hexdigest():
                is_passed_md5 = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        elif line.startswith('sha256:'):
            is_check_sha256 = True
            sha256 = hashlib.sha256()
            sha256.update(content)

            if line.split(':')[1] == sha256.hexdigest():
                is_passed_sha256 = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        elif line.startswith('sha512:'):
            is_check_sha512 = True
            sha512 = hashlib.sha512()
            sha512.update(content)

            if line.split(':')[1] == sha512.hexdigest():
                is_passed_sha512 = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        elif line.startswith('sha3-256:'):
            is_check_sha3_256 = True
            sha3_256 = hashlib.sha3_256()
            sha3_256.update(content)

            if line.split(':')[1] == sha3_256.hexdigest():
                is_passed_sha3_256 = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        elif line.startswith('sha3-512:'):
            is_check_sha3_512 = True
            sha3_512 = hashlib.sha3_512()
            sha3_512.update(content)

            if line.split(':')[1] == sha3_512.hexdigest():
                is_passed_sha3_512 = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        elif line.startswith('blake2b:'):
            is_check_blake2b = True
            blake2b = hashlib.blake2b()
            blake2b.update(content)

            if line.split(':')[1] == blake2b.hexdigest():
                is_passed_blake2b = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        elif line.startswith('blake2s:'):
            is_check_blake2s = True
            blake2s = hashlib.blake2s()
            blake2s.update(content)

            if line.split(':')[1] == blake2s.hexdigest():
                is_passed_blake2s = True
            else:
                failed_list.append(file_path)
                is_next = True

            bar.next()
        # If line is file name
        else:
            if len(file_path) != 0 or line:
                is_next = False

                path = os.path.join(application_path, line.strip(os.sep))

                file_target = open(path, 'rb')
                content = file_target.read()

                file_path = line

    bar.finish()

    # Write result
    file_result = open(os.path.join(application_path, RESULT_FILE), 'w')

    file_result.write('PASSED:\n')
    for file in passed_list:
        file_result.write(f'{file}\n')
    file_result.write('\n\n')

    file_result.write('FAILED:\n')
    for file in failed_list:
        file_result.write(f'{file}\n')

    file_result.close()

    return


# Run generate process
def generate_hash():

    # Get all files count
    bar_count = 0
    file_count = 0
    for path, subdirs, files in os.walk(application_path):
        for file in files:
            if file != HASHED_FILE and file != os.path.basename(
                    executable_name):
                file_count += 1
    if is_user_set_algorithm:
        bar_count = file_count * len(algorithm_options)
    else:
        bar_count = file_count * 7

    # Create hash output file
    file_hash = open(os.path.join(application_path, HASHED_FILE), 'w')

    # Process bar
    bar = ProcessBar('Processing', max=bar_count)

    # Loop through all files and directories in current path
    for path, subdirs, files in os.walk(application_path):
        for name in files:

            if name == HASHED_FILE:
                # Don't hash output file
                continue
            elif name == os.path.basename(executable_name):
                # Don't hash exe file
                continue

            # Remove abosolute path
            # Keep sub-folder and file name
            write_path = os.path.join(path.replace(application_path, ''), name)

            # Open file to hash
            file_path = os.path.join(path, name)

            file_target = open(file_path, 'rb')
            content = file_target.read()
            file_hash.write(f'{write_path}\n')

            md5 = hashlib.md5()
            sha256 = hashlib.sha256()
            sha512 = hashlib.sha512()
            sha3_256 = hashlib.sha3_256()
            sha3_512 = hashlib.sha3_512()
            blake2b = hashlib.blake2b()
            blake2s = hashlib.blake2s()

            if is_user_set_algorithm:
                if 'md5' in algorithm_options:
                    md5.update(content)
                    file_hash.write(f'md5:{md5.hexdigest()}\n')
                    bar.next()

                if 'sha256' in algorithm_options:
                    sha256.update(content)
                    file_hash.write(f'sha256:{sha256.hexdigest()}\n')
                    bar.next()

                if 'sha512' in algorithm_options:
                    sha512.update(content)
                    file_hash.write(f'sha512:{sha512.hexdigest()}\n')
                    bar.next()

                if 'sha3_256' in algorithm_options:
                    sha3_256.update(content)
                    file_hash.write(f'sha3-256:{sha3_256.hexdigest()}\n')
                    bar.next()

                if 'sha3_512' in algorithm_options:
                    sha3_512.update(content)
                    file_hash.write(f'sha3-512:{sha3_512.hexdigest()}\n')
                    bar.next()

                if 'blake2b' in algorithm_options:
                    blake2b.update(content)
                    file_hash.write(f'blake2b:{blake2b.hexdigest()}\n')
                    bar.next()

                if 'blake2s' in algorithm_options:
                    blake2s.update(content)
                    file_hash.write(f'blake2s:{blake2s.hexdigest()}\n')
                    bar.next()

            else:
                md5.update(content)
                file_hash.write(f'md5:{md5.hexdigest()}\n')
                bar.next()

                sha256.update(content)
                file_hash.write(f'sha256:{sha256.hexdigest()}\n')
                bar.next()

                sha512.update(content)
                file_hash.write(f'sha512:{sha512.hexdigest()}\n')
                bar.next()

                sha3_256.update(content)
                file_hash.write(f'sha3-256:{sha3_256.hexdigest()}\n')
                bar.next()

                sha3_512.update(content)
                file_hash.write(f'sha3-512:{sha3_512.hexdigest()}\n')
                bar.next()

                blake2b.update(content)
                file_hash.write(f'blake2b:{blake2b.hexdigest()}\n')
                bar.next()

                blake2s.update(content)
                file_hash.write(f'blake2s:{blake2s.hexdigest()}\n')
                bar.next()

            file_hash.write('\n')

    bar.finish()
    file_hash.close()
    return


# Main process
if __name__ == '__main__':
    main(sys.argv[1:])
