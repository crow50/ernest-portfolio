import os
import datetime
import gzip
import shutil
import json
import logging
from pathlib import Path
import argparse

# Define the supported file extensions
SUPPORTED_EXTENSIONS = ('.json',)

# Set up logging
logging.basicConfig(filename='file_operations.log', level=logging.INFO)


def unzip_files(root_dir):
    """Unzip any files with a file extension that is not in SUPPORTED_EXTENSIONS"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension not in SUPPORTED_EXTENSIONS:
                try:
                    with gzip.open(os.path.join(dirpath, filename), 'rb') as f_in:
                        with open(os.path.join(dirpath, filename) + '.json', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                except Exception as e:
                    logging.error(f"Error unzipping file {filename}: {e}")


def rename_files(root_dir):
    """Rename any .json files using the 'feederId' field from the JSON data"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension in SUPPORTED_EXTENSIONS:
                try:
                    with open(os.path.join(dirpath, filename), encoding='utf-8-sig') as f:
                        parsed_json = json.load(f)
                        feeder_id = parsed_json['feederId']
                        lastupdated = parsed_json['lastUpdatedDate']
                    updatetime = lastupdated[slice(10)]+"_"+lastupdated[slice(11,19,1)].replace(":","")
                    new_filename = f"{feeder_id}_{updatetime}{extension}"
                    os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
                except Exception as e:
                    logging.error(f"Error renaming file {filename}: {e}")


def move_files(root_dir):
    """Move any .json files up one level"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            _, extension = os.path.splitext(filename)
            if extension in SUPPORTED_EXTENSIONS:
                try:
                    path = os.path.join(dirpath, filename)
                    p = Path(path).absolute()
                    parent_dir = p.parents[1]
                    p.rename(parent_dir / p.name)
                except Exception as e:
                    logging.error(f"Error moving file {filename}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Perform file operations on a directory.')
    parser.add_argument('root_dir', type=str, help='the root directory to process')
    args = parser.parse_args()

    root_dir = args.root_dir

    # Perform file operations
    unzip_files(root_dir)
    rename_files(root_dir)
    move_files(root_dir)


if __name__ == '__main__':
    main()
