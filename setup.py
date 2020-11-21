"""Setup."""

# Utilities
from setuptools import setup, find_packages
import sys
import subprocess
from os import path

# Base dir
BASE_DIR = path.abspath(path.dirname(__file__))

# Requirements
with open(path.join(BASE_DIR, 'requirements', 'base.txt'), 'r+') as f:
    requirements = f.read().splitlines()

    if not requirements:
        requirements = subprocess.call(
            'pip install -r ./requirements/prod.txt'
        ).split()

# Long description from README.md file
with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    read_me = f.read()

# Specifications of the setup
setup(
    name='deviceprotect',
    version='0.1',
    description='Encrypt your files safety!',
    long_description=read_me,
    url='https://www.sergiovanberkel.com/',
    author='Sergio van Berkel Acosta',
    author_mail='sergio.vanberkel@gmail.com',
    python_requires='>=3.6.*',
    install_requires=requirements,
    packages=find_packages(),
    py_modules=['main'],
    entry_points='''
        [console_scripts]
        deviceprotect=main:cli
    '''
)

# Warning dependencies message linux
if sys.platform == 'linux':
    print(
        'Please check the dependencies for linux users check out:',
        'https://cryptography.io/en/latest/installation.'
        'html#building-cryptography-on-linux'
    )
