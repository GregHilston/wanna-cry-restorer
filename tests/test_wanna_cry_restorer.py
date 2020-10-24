import pytest
import argparse

from src.wanna_cry_restorer import WannaCryRestorer


def test_build_dataset_from_encrypted_drive():
    """Currently not used"""
    wanna_cry_restorer = WannaCryRestorer(args=None)

    wanna_cry_restorer.build_dataset_from_encrypted_drive(
        root_encrypted_dir="some_fake_directory",
        use_prior_results=False
    )