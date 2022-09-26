#!/usr/bin/env python3
# Copyright (c) 2020 embyt GmbH. See LICENSE for further details.
# Author: Roman Morawek <roman.morawek@embyt.com>
"""setup module for enoceanmqtt"""
import setuptools

# needed packages
REQUIRES = [
    'enocean',
    'paho-mqtt',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='enocean-mqtt',
    version='0.1.3',
    author='Roman Morawek',
    author_email='roman.morawek@embyt.com',
    description='Receives messages from an enOcean serial interface (USB) and provides selected messages to an MQTT broker.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/embyt/enocean-mqtt',
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    keywords='enOcean MQTT IoT',
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=REQUIRES,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'enoceanmqtt=enoceanmqtt.enoceanmqtt:main',
        ],
    },
)
