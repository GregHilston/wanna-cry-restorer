PYTHON=python3
.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

manual_test: ## Tests script using a sample infected directory and a sample backup dir.
	python3 ~/Git/wanna-cry-replacer/wanna_cry_restorer.py \
		--rootdir ~/Git/wanna-cry-replacer/test-infected \
		--backupdir ~/Git/wanna-cry-replacer/test-backup

test: ## Runs unit tests
	python3 -m pytest

real: ## Real script using real infected directory and real backup dir.
	python3 ~/Git/wanna-cry-replacer/wanna_cry_restorer.py \
		--rootdir /run/user/1000/gvfs/smb-share:server=10.0.0.213,share=music \
		--backupdir "/media/ghilston/My Passport"