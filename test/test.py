"""Test."""

# Testing
import unittest
#from pyunitreport import HTMLTestRunner

# Utilities
from pathlib import Path
import subprocess
import shutil
import os
import sys

# Base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Services
from app.service import Services

class TestEncryptation(unittest.TestCase):
    """Test encryptation class."""

    home_dir = os.path.join(str(Path.home()), 'test_deviceprotect')

    def setUp(self):
        """Init method."""

        # Create new folder
        try:
            folders = ['folder1', 'folder2']

            for folder in folders:
                os.makedirs(os.path.join(self.home_dir, folder))
        except OSError:
            shutil.rmtree(self.home_dir)
            print('Deleted old files test. please execute again the test.')

        # Crete one file to encrypt
        with open(os.path.join(self.home_dir, 'example.txt'), 'w') as f:
            f.write('This is the first example.')

        # Create new files to encrypt
        for number in range(7):
            if number < 3:
                files_path = os.path.join(
                    self.home_dir,
                    'folder1',
                    'example{}'.format(number)
                )
            else:
                files_path = os.path.join(
                    self.home_dir,
                    'folder2',
                    'example{}'.format(number)
                )

            with open(files_path, 'w') as f:
                f.write('This is the example number: {}'.format(number))


    def test_encrypt_files(self):
        """
        This test it gonna to encrypt
        only one file.
        PATH: `./test_files/example1.txt`.
        """

        path = os.path.join(self.home_dir, 'example.txt')
        subprocess.call('python3 {} encrypt -f {}'.format(
            os.path.join(BASE_DIR, 'main.py'),
            path
        ).split())

        with open(path, 'r') as f:
            self.assertNotEqual('This is the first example', f.read())


if __name__ == '__main__':
    unittest.main()
