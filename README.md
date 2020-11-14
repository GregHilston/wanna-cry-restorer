# wanna-cry-restorer

A family member's NAS was hit with the Wanna Cry worm. This caused many files to be encrypted and also created a file called `README_FOR_DECRYPT.txt` in every directory.

We were fortunate to have a recent backup of the NAS. This script will walk the encrypted NAS drive and search for backed up files that it can replace the encrypted files with. Additionally it will delete the `README_FOR_DECRYPT.txt` files littered everywhere.

One of the implementation details that's important to note is the folder structure of the NAS and the backup differ. The content we're looking at is music, so the album and artist names will exactly match between the encrypted drive and the backup but the folders above that will not match. Therefore we match on the folder the encrypted file exists on, album, and its parent, artist. Otherwise all directories above that can differ.

Running this script produces two output files that one can look over manually to ensure their happy with the work:

1. `encrypted_drive_dataset.json`: This file will denote all the files that were found that were encrypted, by listing each file's filepath and the total count. Additionally, all the `README_FOR_DECRYPT.txt` filepaths that were found and their count. This so we can preprocess the encrypted drive to build up a dataset of what should be replaced, the encrypted files, and remove, the litter `README_FOR_DECRYPT.txt` files.
2. `encrypted_filepath_to_backup_filepath.json`: This file denotes a mapping of all encrypted filepaths to the filepath of the unencrypted backup file. This is a preprocessing of files that we can walk and replace each encrypted file with the unencrypted file.
