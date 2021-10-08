#!/usr/bin/env python
import os
from setuptools import setup


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)
    return open(path).read()

setup(
    name='spotify2m3u',
    version='0.0.2',
    description='spotify playlist recreation using local library',
    author='Jonathan Bartlett',
    author_email='jonathan@jonnobrow.co.uk',
    license='MIT',
    platforms='ALL',
    long_description=_read('README.md'),
    zip_safe=False,
    include_package_data=True,  # Install plugin resources.

    packages=[
        'spotify2m3u',
    ],
    entry_points={
        'console_scripts': [
            'spotify2m3u = spotify2m3u:main',
        ],
    },
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
)
