#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='uncurl-pk',
    version='0.0.4',
    description='A library to convert curl requests to python-requests. Forked version of spulec/uncurl ',
    author='Pankaj Kumar',
    author_email='pnkjpvt@gmail.com',
    url='https://github.com/pnkjkpvt/uncurl/tree/master',
    entry_points={
        'console_scripts': [
            'uncurl = uncurl.bin:main',
        ],
    },
    install_requires=['pyperclip', 'six'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
