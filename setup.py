#!/usr/bin/env python
import os
import shutil
import sys
from setuptools import setup, find_packages


version = '1.0.0'
readme = open('README.md').read()
requirements = [
    'jsonrpc_requests'
]

setup(
    # Metadata
    name='pyzen',
    version=version,
    author='Kendrick Tan',
    author_email='kendricktan0814@gmail.com',
    url='https://github.com/kendricktan/pyzen',
    description='Python API for the ZenCash daemon',
    long_description=readme,

    # Package info
    packages=find_packages(exclude=('test',)),
    zip_safe=True,
    install_requires=requirements,

    # CLI entry-points
    entry_points={
        'console_scripts': [
        ]
    }
)
