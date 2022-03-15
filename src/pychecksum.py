#!/usr/bin/python3
import sys
import os
import hashlib
from progress.bar import IncrementalBar

VERSION = 'v1.1.0'
HASHED_FILE = 'PyChecksum.hash'
RESULT_FILE = 'PyCheckResult.txt'


# Process Bar
class ProcessBar(IncrementalBar):
    message = 'Loading'
    suffix = '%(percent)d%% [%(index)d/%(max)d] - %(elapsed)ds'


# Main process
def main():
    global application_path
    global executable_name

    print(f'PyChecksum-{VERSION}')

    if getattr(sys, 'frozen', False):
        # If run as exe
        application_path = os.path.dirname(sys.executable)
        executable_name = sys.executable
    else:
        # If run as script
        application_path = os.path.dirname(os.path.abspath(__file__))
        executable_name = os.path.basename(__file__)

    # Check for empty directory
    files = os.listdir(application_path)
    if len(files) == 1:
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

    passed_md5 = False
    passed_sha256 = False
    passed_sha512 = False
    passed_sha3_256 = False
    passed_sha3_512 = False
    passed_blake2b = False
    passed_blake2s = False

    # Open hashed files list
    file_hash = open(os.path.join(application_path, HASHED_FILE), 'r')

    # Read entire file
    lines = file_hash.readlines()

    # Get all files count
    bar_count = 0
    for line in lines:
        line = line.strip()
        if not (line.startswith('sha256:') or line.startswith('sha512:')
                or line.startswith('sha3-256:') or line.startswith('sha3-512:')
                or line.startswith('blake2b:') or line.startswith('blake2s:')
                or line.startswith('md5:') or line):
            bar_count += 1
    bar_count *= 7

    # Process bar
    bar = ProcessBar('Processing', max=bar_count)

    for line in lines:
        line = line.strip()

        if (passed_md5 and passed_sha256 and passed_sha512 and passed_sha3_256
                and passed_sha3_512 and passed_blake2b and passed_blake2s):
            passed_list.append(file_path)
            passed_md5 = False
            passed_sha256 = False
            passed_sha512 = False
            passed_sha3_256 = False
            passed_sha3_512 = False
            passed_blake2b = False
            passed_blake2s = False

        # If empty line
        if not line:
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
        elif line.startswith('sha3-256:'):
            if line.split(':')[1] == sha3_256.hexdigest():
                passed_sha3_256 = True
            else:
                failed_list.append(file_path)
                is_next = True
        elif line.startswith('sha3-512:'):
            if line.split(':')[1] == sha3_512.hexdigest():
                passed_sha3_512 = True
            else:
                failed_list.append(file_path)
                is_next = True
        elif line.startswith('blake2b:'):
            if line.split(':')[1] == blake2b.hexdigest():
                passed_blake2b = True
            else:
                failed_list.append(file_path)
                is_next = True
        elif line.startswith('blake2s:'):
            if line.split(':')[1] == blake2s.hexdigest():
                passed_blake2s = True
            else:
                failed_list.append(file_path)
                is_next = True
        # If line is file name
        else:
            is_next = False

            path = os.path.join(application_path, line.strip('\\'))
            # print(f'Verifing: {path}')

            file_target = open(path, 'rb')
            content = file_target.read()

            md5 = hashlib.md5()
            md5.update(content)
            bar.next()

            sha256 = hashlib.sha256()
            sha256.update(content)
            bar.next()

            sha512 = hashlib.sha512()
            sha512.update(content)
            bar.next()

            sha3_256 = hashlib.sha3_256()
            sha3_256.update(content)
            bar.next()

            sha3_512 = hashlib.sha3_512()
            sha3_512.update(content)
            bar.next()

            blake2b = hashlib.blake2b()
            blake2b.update(content)
            bar.next()

            blake2s = hashlib.blake2s()
            blake2s.update(content)
            bar.next()

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


def generate_hash():

    # Get all files count
    bar_count = 0
    for path, subdirs, files in os.walk(application_path):
        for file in files:
            if file != HASHED_FILE and file != os.path.basename(
                    executable_name):
                bar_count += 1
    bar_count *= 7

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

            md5 = hashlib.md5()
            md5.update(content)
            bar.next()

            sha256 = hashlib.sha256()
            sha256.update(content)
            bar.next()

            sha512 = hashlib.sha512()
            sha512.update(content)
            bar.next()

            sha3_256 = hashlib.sha3_256()
            sha3_256.update(content)
            bar.next()

            sha3_512 = hashlib.sha3_512()
            sha3_512.update(content)
            bar.next()

            blake2b = hashlib.blake2b()
            blake2b.update(content)
            bar.next()

            blake2s = hashlib.blake2s()
            blake2s.update(content)
            bar.next()

            file_hash.write(f'{write_path}\n')
            file_hash.write(f'md5:{md5.hexdigest()}\n')
            file_hash.write(f'sha256:{sha256.hexdigest()}\n')
            file_hash.write(f'sha512:{sha512.hexdigest()}\n')
            file_hash.write(f'sha3-256:{sha3_256.hexdigest()}\n')
            file_hash.write(f'sha3-512:{sha3_512.hexdigest()}\n')
            file_hash.write(f'blake2b:{blake2b.hexdigest()}\n')
            file_hash.write(f'blake2s:{blake2s.hexdigest()}\n')
            file_hash.write('\n')

    bar.finish()
    file_hash.close()
    return


if __name__ == '__main__':
    main()
