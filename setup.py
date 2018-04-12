#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='uncurl',
    version='0.0.8.1',
    description='A library to convert curl requests to python-requests.',
    author='Steve Pulec',
    author_email='spulec@gmail',
    url='https://github.com/spulec/uncurl',
    entry_points={
        'console_scripts': [
            'uncurl = uncurl.bin:main',
        ],
    },
    install_requires=['xerox', 'six'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
