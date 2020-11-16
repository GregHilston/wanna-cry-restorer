PYTHON=python3
.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

mount_backup: ## Mounts the backup external drive we plug in via USB
	sudo mount /dev/sdb1 /media/external-usb

mount_samba: ## Mounts the music share from the NAS over SMB to our local mount point
	sudo mount -t cifs -o ghilston //10.0.0.213/music /mnt/dad_nas_musiclibrary

old_manual_test: ## Tests script using a sample infected directory and a sample backup dir.
	python3 ~/Git/wanna-cry-restorer/wanna_cry_restorer.py \
		--root_encrypted_dir ~/Git/wanna-cry-restorer/test-infected \
		--root_backup_dir ~/Git/wanna-cry-restorer/test-backup

manual_test: ## Tests script using a sample infected directory and a sample backup dir.
	python3 ~/Git/wanna-cry-restorer/src/wanna_cry_restorer.py \
		--root_encrypted_dir ~/Git/wanna-cry-restorer/fake_data/fake_root_encrypted_dir \
		--root_backup_dir ~/Git/wanna-cry-restorer/fake_data/fake_root_backup_dir \
		--dry_run

test: ## Runs unit tests
	python3 -m pytest

real: ## Real script using real infected directory and real backup dir.
	python3 ~/Git/wanna-cry-restorer/src/wanna_cry_restorer.py \
		--root_encrypted_dir /mnt/dad_nas_musiclibrary \
		--root_backup_dir "/media/external-usb" #\
	        # --dry_run

find_encrypted_files_without_backup: ## Finds encrypted files without backup. Run after running for real but as a dryrun.
	python3 find_encrypted_files_with_no_backup.py
