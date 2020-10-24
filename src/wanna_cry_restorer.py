# TODO only replace files that are encypted with the corresponding file name,
# without the encypt appendix, in a SAME folder name on the backup
# EX: replace "/run/user/1000/gvfs/smb-share:server=10.0.0.213,share=music/New Age/Steve Roach/Spiral Revelation/cover.jpg.encrypt" ONLY with a `cover.jpg` in a folder called Spiral Revelation


import os
import json 

import argparse

class WannaCryRestorer:
    def __init__(self, args):
        self.args = args

    def build_dataset_from_encrypted_drive(self, root_encrypted_dir: str, use_past_run_dataset = False):
        """Traverses the root_encrypted_dir and builds up a data structure of
        filepaths that are encrypted and filespaths of litter files.

        Will store the results in a locally created .json file to avoid running
        more than one, as the root_encrypted_dir can be large.
        """
        litter_file_left_behind_by_wanna_cry = "README_FOR_DECRYPT.txt"

        # if prior run's results were found
        if use_past_run_dataset and os.path.exists("encrypted_drive_dataset.json"):
            print("prior run's 'encrypted_drive_dataset.json' is found. Using that instead of recreating it")
            with open("encrypted_drive_dataset.json") as json_file: 
                encrypted_drive_dataset = json.load(json_file)
                return encrypted_drive_dataset

        # if no prior run's results were found

        # our datastructure of built up knowledge from the encrypted 
        # root_encrypted_derive
        encrypted_drive_dataset = {}

        # where we'll store filepaths of files that are encrypted
        encrypted_drive_dataset["encrypted"] = {}
        encrypted_drive_dataset["encrypted"]["filepaths"] = []
        
        # where we'll store filepaths of litter
        encrypted_drive_dataset["litter"] = {}
        encrypted_drive_dataset["litter"]["filepaths"] = []

        # recursively traverse every directory in root_encrypted_dir
        for subdir, dirs, files in os.walk(root_encrypted_dir):
            for file in files:
                # builds up the full file path
                filepath = subdir + os.sep + file

                # if litter
                if file == litter_file_left_behind_by_wanna_cry:
                    encrypted_drive_dataset["litter"]["filepaths"].append(filepath)

                # if encrypted
                if filepath.endswith(".encrypt"):
                    encrypted_drive_dataset["encrypted"]["filepaths"].append(filepath)

        # store total counts for roll up stats
        encrypted_drive_dataset["litter"]["count"] = len(encrypted_drive_dataset["litter"]["filepaths"])
        encrypted_drive_dataset["encrypted"]["count"] = len(encrypted_drive_dataset["encrypted"]["filepaths"])

        # write our results locally so we don't have to recompute
        with open("encrypted_drive_dataset.json", 'w') as outfile:
            json.dump(encrypted_drive_dataset, outfile)
    
        print("encrypted drive dataset built and dumped to encrypted_drive_dataset.json")
        return encrypted_drive_dataset

    def replace_encrypted_with_backup(self, root_backup_dir: str, encrypted_drive_dataset: dict):
        print("begin searching backup for files to use as replacements")

        # maps encrypted filepaths to backup filepaths that can be used to restore
        encrypted_filepath_to_backup_filepath = {}

        # recursively traverse every directory in root_backup_dir
        for subdir, dirs, backup_files in os.walk(root_backup_dir):
            for backup_file in backup_files:
                # builds up the full file path
                backup_filepath = subdir + os.sep + backup_file
                
                for encrypted_filepath in [entry for entry in encrypted_drive_dataset["encrypted"]["filepaths"] if entry.endswith("encrypt")]:
                    # print(f"encrypted_filepath {encrypted_filepath}")
                    encrypted_file = os.path.basename(encrypted_filepath)
                    # print(f"encrypted_file {encrypted_file}")
                    if backup_file + ".encrypt" == encrypted_file:
                        print(f'\tCan replace encrypted "{encrypted_filepath}" with "{backup_filepath}"')
                        encrypted_filepath_to_backup_filepath[encrypted_filepath] = backup_filepath

        # write our results locally so we don't have to recompute
        with open("encrypted_filepath_to_backup_filepath.json", 'w') as outfile:
                json.dump(encrypted_filepath_to_backup_filepath, outfile)
        
        print("mapping of encrypted files to backup files built and dumped to encrypted_filepath_to_backup_filepath.json")

        return encrypted_filepath_to_backup_filepath
    
    def restore(self):
        # traverse encrypted drive and figure out what litter we can remove and
        # what files are encrypted
        encrypted_drive_dataset = self.build_dataset_from_encrypted_drive(self.args.root_encrypted_dir) 

        # travese the backup drive and figure out what backups we can use to
        # replace encrypted files
        encrypted_filepath_to_backup_filepath = self.replace_encrypted_with_backup(
            self.args.root_backup_dir, 
            encrypted_drive_dataset
        )

        print(f"able to restore {len(encrypted_filepath_to_backup_filepath.keys())} files out of a total of {len(encrypted_drive_dataset['encrypted']['filepaths'])} encrypted files")
        print(f"able to remove {encrypted_drive_dataset['litter']['count']} litter files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_encrypted_dir", required=True, help="The root directory that was encrypted.")
    parser.add_argument("--root_backup_dir", required=True, help="The root backup directory.")
    
    args = parser.parse_args()

    wanna_cry_restorer = WannaCryRestorer(args)
    wanna_cry_restorer.restore()