PYTHON=python3
.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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
	python3 ~/Git/wanna-cry-restorer/wanna_cry_restorer.py \
		--root_encrypted_dir /run/user/1000/gvfs/smb-share:server=10.0.0.213,share=music \
		--root_backup_dir "/media/ghilston/My Passport"
