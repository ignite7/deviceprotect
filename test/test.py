"""Test."""

# Testing
import unittest
from pyunitreport import HTMLTestRunner

# Utilities
from pathlib import Path
import subprocess
import shutil
import os
import sys

# Base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


class EncryptionTest(unittest.TestCase):
    """Encryption test class."""

    dir_home = os.path.join(str(Path.home()), 'test_deviceprotect')
    dir_app = os.path.join(BASE_DIR, 'main.py')

    def setUp(self):
        """Init method."""

        # Create new folder
        folders = ['folder1', 'folder2']

        for folder in folders:
            os.makedirs(os.path.join(self.dir_home, folder), exist_ok=True)

        # Create two files to encrypt
        for number in range(1, 3):
            files_path = os.path.join(
                self.dir_home,
                'example{}.txt'.format(number)
            )

            with open(files_path, 'w') as f:
                f.write('This is the first example number: {}'.format(number))

        # Create new files to encrypt
        for number in range(1, 7):
            if number <= 3:
                files_path = os.path.join(
                    self.dir_home,
                    'folder1',
                    'example{}.txt'.format(number)
                )
            else:
                files_path = os.path.join(
                    self.dir_home,
                    'folder2',
                    'example{}.txt'.format(number)
                )

            with open(files_path, 'w') as f:
                f.write('This is the example number: {}'.format(number))

    def test_one_file_one_key(self):
        """
        This test it gonna to encrypt
        and decrypt only one file
        with one key.
        PATH: `{home}/test_files/{files}`.
        """

        path = os.path.join(self.dir_home, 'example1.txt')

        # Encrypt
        output = subprocess.check_output(
            'python {} encrypt -f {}'.format(
                self.dir_app,
                path
            ).split()
        ).decode().split(':')[1].strip().replace('"', '').rstrip('.')

        # Check if the file has been encrypted
        with open(path, 'r') as f:
            self.assertNotEqual(
                'This is the first example number: 1',
                f.read()
            )

        # Decrypt
        keys = []

        with open(output, 'r') as f:
            for key in f.read().split('|'):
                if 'KEY' in key:
                    keys.append(key.split('KEY: ')[1].rstrip())

        subprocess.call('python {} decrypt -f {} -k {}'.format(
            self.dir_app,
            path,
            keys[0]
        ).split())

        # Check the content inside the file is decrypted
        with open(path, 'r') as f:
            self.assertEqual(
                'This is the first example number: 1',
                f.read()
            )

        self.finish_test(output)

    def test_several_files_multiple_keys(self):
        """
        This test it gonna to encrypt and decrypt
        several files with multiple keys.
        PATH: '{home}/test_files/{files}`.
        """

        path_1 = os.path.join(self.dir_home, 'example1.txt')
        path_2 = os.path.join(self.dir_home, 'example2.txt')

        # Encrypt
        output = subprocess.check_output(
            'python {} encrypt -f {} -f {} -m'.format(
                self.dir_app,
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
        self.assertNotEqual(keys[0], keys[1])

        # Check if the file has been encrypted
        for number in range(1, 3):
            files_path = os.path.join(
                self.dir_home,
                'example{}.txt'.format(number)
            )
            with open(files_path, 'r') as f:
                self.assertNotEqual(
                    'This is the first example number: {}'.format(number),
                    f.read()
                )

        # Decrypt
        subprocess.call('python {} decrypt -b {}'.format(
            self.dir_app,
            output.replace('summary.txt', 'backup.db')
        ).split())

        # Check the files has been decrypted
        for number in range(1, 3):
            files_path = os.path.join(
                self.dir_home,
                'example{}.txt'.format(number)
            )
            with open(files_path, 'r') as f:
                self.assertEqual(
                    'This is the first example number: {}'.format(number),
                    f.read()
                )

        self.finish_test(output)

    def test_several_devices_one_key(self):
        """
        This test it gonna to encrypt and
        decrypt several directories with
        only one key.
        PATH: `{home}/test_deviceprotect`
        """

        path_1 = os.path.join(self.dir_home, 'folder1')
        path_2 = os.path.join(self.dir_home, 'folder2')

        # Encrypt
        output = subprocess.check_output(
            'python {} encrypt -d {} -d {}'.format(
                self.dir_app,
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

        # Decrypt
        subprocess.call('python {} decrypt -b {}'.format(
            self.dir_app,
            output.replace('summary.txt', 'backup.db')
        ).split())

        # Check the files has been decrypted
        for number in range(1, 7):
            if number <= 3:
                files_path = os.path.join(path_1, f'example{number}.txt')
            else:
                files_path = os.path.join(path_2, f'example{number}.txt')

            with open(files_path, 'r') as f:
                self.assertEqual(
                    'This is the example number: {}'.format(number),
                    f.read()
                )

        self.finish_test(output)

    def test_several_devices_multiple_keys(self):
        """
        This test it gonna to encrypt and decrypt
        several directories with only multiple keys.
        PATH: `{home}/test_deviceprotect`
        """

        path_1 = os.path.join(self.dir_home, 'folder1')
        path_2 = os.path.join(self.dir_home, 'folder2')

        # Encrypt
        output = subprocess.check_output(
            'python {} encrypt -d {} -d {} -m'.format(
                self.dir_app,
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

        # Decrypt
        subprocess.call('python {} decrypt -b {}'.format(
            self.dir_app,
            output.replace('summary.txt', 'backup.db')
        ).split())

        # Check the files has been decrypted
        for number in range(1, 7):
            if number <= 3:
                files_path = os.path.join(path_1, f'example{number}.txt')
            else:
                files_path = os.path.join(path_2, f'example{number}.txt')

            with open(files_path, 'r') as f:
                self.assertEqual(
                    'This is the example number: {}'.format(number),
                    f.read()
                )

        self.finish_test(output)

    def test_save_path(self):
        """
        This test it gonna to encrypt and decrypt
        one file and save the summary in a custom
        directory.
        PATH: `{home}/test_encrypt/{file}`
        """

        path = os.path.join(self.dir_home, 'example1.txt')

        # Encrypt
        output = subprocess.check_output(
            'python {} encrypt -f {} -s {}'.format(
                self.dir_app,
                path,
                '/var/tmp'
            ).split()
        ).decode().split(':')[1].strip().replace('"', '').rstrip('.')

        # Check if the summary has been saved in the custom path
        self.assertTrue(os.path.exists(output))

        # Check if the file has been encrypted
        with open(path, 'r') as f:
            self.assertNotEqual(
                'This is the first example number: 1',
                f.read()
            )

        # Decrypt
        subprocess.call('python {} decrypt -b {}'.format(
            self.dir_app,
            output.replace('summary.txt', 'backup.db')
        ).split())

        # Check if the file has been decrypted
        with open(path, 'r') as f:
            self.assertEqual(
                'This is the first example number: 1',
                f.read()
            )

        self.finish_test(output, True)

    def finish_test(self, output, end=False):
        """
        First it gonna call the
        method `tearDown` and
        then the method `setUp`
        for init again new files
        for the next test.
        """

        try:
            shutil.rmtree(output.rstrip('summary.txt'))
            shutil.rmtree(self.dir_home)
            print('Test files generated deleted.')

            if not end:
                self.setUp()
                print('New test starting.')
        except FileNotFoundError:
            pass

    def tearDown(self):
        """Finish."""

        try:
            shutil.rmtree(self.dir_home)
            print('Finish.')
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(
            output=os.path.join(BASE_DIR, 'test', 'reports'),
            report_name='encryption_test'
        )
    )
