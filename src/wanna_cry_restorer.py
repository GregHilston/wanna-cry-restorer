# TODO only replace files that are encypted with the corresponding file name,
# without the encypt appendix, in a SAME folder name on the backup
# EX: replace "/run/user/1000/gvfs/smb-share:server=10.0.0.213,share=music/New Age/Steve Roach/Spiral Revelation/cover.jpg.encrypt" ONLY with a `cover.jpg` in a folder called Spiral Revelation


import argparse
import json 
import os

from shutil import copyfile


class WannaCryRestorer:
    def __init__(self, args):
        self.args = args

    def build_dataset_from_encrypted_drive(self, root_encrypted_dir: str, use_past_run_dataset = True):
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
        for root, subdirs, files in os.walk(root_encrypted_dir):
            # from https://stackoverflow.com/a/2212698/1983957
            # root: Current path which is "walked through"
            # subdirs: Files in root of type directory
            # files: Files in root (not in subdirs) of type other than directory
            for filename in files:
                # builds up the full file path
                filepath = os.path.join(root, filename)

                # if litter
                if filename == litter_file_left_behind_by_wanna_cry:
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
        for root, subdirs, files in os.walk(root_backup_dir):
            # from https://stackoverflow.com/a/2212698/1983957
            # root: Current path which is "walked through"
            # subdirs: Files in root of type directory
            # files: Files in root (not in subdirs) of type other than directory

            # the following code ensures that two filenames that match have the same
            # directory and directory above that matching
            # it is not performant. This ensures that each file we replace with a backup file
            # is the same file instead of clobbering based on same filenames
            # for every backup file
            for filename in files:
                # builds up the full file path
                backup_filepath = os.path.join(root, filename)

                # for every encrypted file
                for encrypted_filepath in [entry for entry in encrypted_drive_dataset["encrypted"]["filepaths"] if entry.endswith("encrypt")]:
                    encrypted_file = os.path.basename(encrypted_filepath)

                    backup_filepath_directory = os.path.basename(os.path.dirname(backup_filepath))
                    backup_filepath_parent_directory = os.path.basename(os.path.abspath(os.path.join(os.path.dirname(backup_filepath), "..")))
                    encrypted_filepath_directory = os.path.basename(os.path.dirname(encrypted_filepath))
                    encrypted_filepath_parent_directory = os.path.basename(os.path.abspath(os.path.join(os.path.dirname(encrypted_filepath), "..")))
                    
                    do_directories_match = backup_filepath_directory == encrypted_filepath_directory
                    do_parent_directories_match = backup_filepath_parent_directory == encrypted_filepath_parent_directory

                    if filename + ".encrypt" == encrypted_file and do_directories_match and do_parent_directories_match:
                        # print(f"\tencrypted_filepath {encrypted_filepath}")
                        # print(f"\tbackup_filepath {backup_filepath}")

                        # print(f"\tencrypted_file {encrypted_file}")
                        # print(f"\tbackup_file {filename}")

                        # print(f"\tbackup_filepath_directory {backup_filepath_directory}")
                        # print(f"\tbackup_filepath_parent_directory {backup_filepath_parent_directory}")
                        # print(f"\tencrypted_filepath_directory {encrypted_filepath_directory}")
                        # print(f"\tencrypted_filepath_parent_directory {encrypted_filepath_parent_directory}")

                        print(f'\tcan replace encrypted "{encrypted_filepath}" with "{backup_filepath}"')
                        encrypted_filepath_to_backup_filepath[encrypted_filepath] = backup_filepath

        # write our results locally so we don't have to recompute
        with open("encrypted_filepath_to_backup_filepath.json", 'w') as outfile:
                json.dump(encrypted_filepath_to_backup_filepath, outfile)
        
        print("mapping of encrypted files to backup files built and dumped to encrypted_filepath_to_backup_filepath.json")

        return encrypted_filepath_to_backup_filepath
    
    def remove_litter(self, litter_filepaths: list, dry_run=True):
        """Removes all files in litter_filepaths"""

        if dry_run:
            print(f"would remove {len(litter_filepaths)} litter filepaths")
        else:
            print(f"going to remove {len(litter_filepaths)} litter filepaths")


        for litter_filepath in litter_filepaths:
            if dry_run:
                print(f"\twould remove litter filepath at {litter_filepath}")
            else:
                os.remove(litter_filepath)
                print(f"\tremoved litter filepath at {litter_filepath}")

    def restore_encrypted_files_with_backups(self, encrypted_filepath_to_backup_filepath: dict, dry_run=True):
        """Restores all encrypted filepaths with backup filepaths"""

        if dry_run:
            print(f"would restore {len(encrypted_filepath_to_backup_filepath.keys())} encrypted filepaths with backup filepaths")
        else:
            print(f"going to restore {len(encrypted_filepath_to_backup_filepath.keys())} encrypted filepaths with backup filepaths")


        for key, value in encrypted_filepath_to_backup_filepath.items():
            if dry_run:
                print(f"\twould restore encrypted filepath at {key} with backup filepath at {value}")
            else:
                copyfile(value, key)
                print(f"\trestored encrypted filepath at {key} with backup filepath at {value}")

    def run(self):
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

        # perform the cleaning of litter
        self.remove_litter(encrypted_drive_dataset["litter"]["filepaths"], dry_run=self.args.dry_run)

        # perform the restoring of encrypted filepaths with backup filepaths
        self.restore_encrypted_files_with_backups(encrypted_filepath_to_backup_filepath, dry_run=self.args.dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_encrypted_dir", required=True, help="The root directory that was encrypted.")
    parser.add_argument("--root_backup_dir", required=True, help="The root backup directory.")
    parser.add_argument("--dry_run", action="store_true", help="Whether to just print out what we'd do and not actually do it or not.")
    
    args = parser.parse_args()

    wanna_cry_restorer = WannaCryRestorer(args)
    wanna_cry_restorer.run()
