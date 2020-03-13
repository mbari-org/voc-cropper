#!/usr/bin/env python

__author__ = "Danelle Cline"
__copyright__ = "Copyright 2020, MBARI"
__credits__ = ["MBARI"]
__license__ = "GPL"
__maintainer__ = "Danelle Cline"
__email__ = "dcline at mbari.org"
__doc__ = '''

Python test using the nose python framework

@author: __author__
@status: __status__
@license: __license__
'''

import subprocess
import os
from nose import with_setup

print("")  # this is to get a newline after the dots
print("setup_module before anything in this file")

def teardown_module(module):
    '''
    Run after everything in this file completes
    :param module:
    :return:
    '''
    print('teardown_module')


def custom_setup_function():
    print("custom_setup_function")


def custom_teardown_function():
    print("custom_teardown_function")


@with_setup(custom_setup_function, custom_teardown_function)
def test_cropper():
    print('<============================ running test_cropper ============================ >')
    subprocess.check_call(['python3', '/app/run.py', '-d', '/data/annotations', '--image_dir',
                            '/data/imgs', '-o', '/data/out'], shell=False)
    exists = os.path.exists('/data/out/PENIAGONE_VITREA/IMG_5137_0.jpg')
    assert exists
