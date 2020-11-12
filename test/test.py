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
    app_dir = os.path.join(BASE_DIR, 'main.py')

    def setUp(self):
        """Init method."""

        # Create new folder
        folders = ['folder1', 'folder2']

        for folder in folders:
            os.makedirs(os.path.join(self.home_dir, folder), exist_ok=True)

        # Crete one file to encrypt
        with open(os.path.join(self.home_dir, 'example.txt'), 'w') as f:
            f.write('This is the first example.')

        # Create new files to encrypt
        for number in range(1, 7):
            if number <= 3:
                files_path = os.path.join(
                    self.home_dir,
                    'folder1',
                    'example{}.txt'.format(number)
                )
            else:
                files_path = os.path.join(
                    self.home_dir,
                    'folder2',
                    'example{}.txt'.format(number)
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
        subprocess.call('python {} encrypt -f {}'.format(
            self.app_dir,
            path
        ).split())

        # Check if the file has been encrypted
        with open(path, 'r') as f:
            self.assertNotEqual('This is the first example', f.read())

        self.finish_test()

    def test_encrypt_devices_one_key(self):
        """
        This test it gonna to encrypt
        several directories with only
        one key.
        PATH: `{home}/test_deviceprotect`
        """

        path_1 = os.path.join(self.home_dir, 'folder1')
        path_2 = os.path.join(self.home_dir, 'folder2')
        output = subprocess.check_output(
            'python {} encrypt -d {} -d {}'.format(
                self.app_dir,
                path_1,
                path_2
            ).split()
        ).decode().split(':')[1].strip().replace('"', '').rstrip('.')

        keys = []
        with open(output, 'r') as f:
            for key in f.read().split('|'):
                if 'KEY' in key:
                    keys.append(key.split('KEY: ')[1].rstrip())

        # Check if the keys are the same
        self.assertEqual(keys[0], keys[4])

        # Check if the file has been encrypted
        for number in range(1, 7):
            if number <= 3:
                files_path = os.path.join(path_1, f'example{number}.txt')
            else:
                files_path = os.path.join(path_2, f'example{number}.txt')

            with open(files_path, 'r') as f:
                self.assertNotEqual(
                    'This is the example number: {}'.format(number),
                    f.read()
                )

        self.finish_test()

    def test_encrypt_devices_multiple_key(self):
        """
        This test it gonna to encrypt
        several directories with only
        multiple keys.
        PATH: `{home}/test_deviceprotect`
        """

        path_1 = os.path.join(self.home_dir, 'folder1')
        path_2 = os.path.join(self.home_dir, 'folder2')
        output = subprocess.check_output(
            'python {} encrypt -d {} -d {} -m'.format(
                self.app_dir,
                path_1,
                path_2
            ).split()
        ).decode().split(':')[1].strip().replace('"', '').rstrip('.')

        keys = []
        with open(output, 'r') as f:
            for key in f.read().split('|'):
                if 'KEY' in key:
                    keys.append(key.split('KEY: ')[1].rstrip())

        # Check if the keys are not the same
        self.assertNotEqual(keys[0], keys[4])

        # Check if the file has been encrypted
        for number in range(1, 7):
            if number <= 3:
                files_path = os.path.join(path_1, f'example{number}.txt')
            else:
                files_path = os.path.join(path_2, f'example{number}.txt')

            with open(files_path, 'r') as f:
                self.assertNotEqual(
                    'This is the example number: {}'.format(number),
                    f.read()
                )

        self.finish_test()

    def finish_test(self):
        """
        First it gonna call the
        method `tearDown` and
        then the method `setUp`
        for init again new files
        for the next test.
        """

        self.tearDown()
        self.setUp()
        print('New test starting.')

    def tearDown(self):
        """Finished test."""

        shutil.rmtree(self.home_dir)
        print('Test files generated deleted.')


if __name__ == '__main__':
    unittest.main()
