import sys
import os
import pytest
from pynt import task

test_dir = 'src/test/'

@task()
def test(*args):
    """Execute unit tests without coverage."""
    print(args)
    tests = [test_dir + module for module in args] if len(args) else [test_dir]
    print(tests)
    tests.append('-x')
    tests.append('--log-file-level=debug')
    tests.append('--verbose')
    result = pytest.main(tests)
    if result is None or result != 0:
        raise Exception("Unittests failed")

@task()
def coverage():
    """Runs unit test suite with coverage report"""
    subdirs = [os.path.join(test_dir, o) for o in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, o))]

    tests = [
        '-x',
        '--log-file-level=debug',
        '--verbose',
        '--cov-config=.coveragerc',
        '--cov=src',
        '--cov-report=html']

    ignore_dirs = ['__pycache__', 'src/rpgmanager/db.py']
    tests = tests + ['--ignore=' + d for d in ignore_dirs]

    tests.extend(subdirs)

    result = pytest.main(tests)

    if result is None or result != 0:
        raise Exception("One or more unit tests failed")