"""Generate random data files."""

# Utilities
from pathlib import Path
import os

dir_home = str(Path.home())
os.mkdir(os.path.join(dir_home, 'exam1'))
os.mkdir(os.path.join(dir_home, 'exam2'))

with open(os.path.join(dir_home, 'exam1', 'first.txt'), 'w') as f:
    f.write('This is exam1')

with open(os.path.join(dir_home, 'exam2', 'second.txt'), 'w') as f:
    f.write('This is exam2')
