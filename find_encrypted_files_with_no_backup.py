# Quick script to walk the two output files and find which encrypted files have no backup
import typing
import json


def get_encrypted_filepaths(encrypted_drive_dataset_filename: str) -> typing.List[str]:
    """Gets a list of all encrypted filepaths by parsing an outputted encrypted_drive_dataset_filename (ex: encrypted_drive_dataset.json)"""
    with open(encrypted_drive_dataset_filename) as file:
        data = json.load(file)
        return data["encrypted"]["filepaths"]


def get_filepaths_without_backup(encrypted_filepaths: typing.List[str], encrypted_filepath_to_backup_filepath_filename: str) -> typing.List[str]:
    """Gets a list of all encrypted filepaths where a backup was not found. Does this by walking all the encrypted_filepaths and seeing if such file exists as a key in an outputted encrypted_filepath_to_backup_filepath_filename (ex: encrypted_filepath_to_backup_filepath.json)"""
    filepaths_without_backup = []

    with open(encrypted_filepath_to_backup_filepath_filename) as file:
        data = json.load(file)
        for encrypted_filepath in encrypted_filepaths:
            if encrypted_filepath not in data:
                filepaths_without_backup.append(encrypted_filepath)

    return filepaths_without_backup

encrypted_filepaths = get_encrypted_filepaths("encrypted_drive_dataset.json")
# print(encrypted_filepaths)

filepaths_without_backup = get_filepaths_without_backup(encrypted_filepaths, "encrypted_filepath_to_backup_filepath.json")
# print(filepaths_without_backup)
# print(len(filepaths_without_backup))

d = {}
d["filepaths"] = filepaths_without_backup
d["count"] = len(filepaths_without_backup)

with open("encrypted_files_with_no_backup.json", 'w') as f:
    json.dump(d, f)
