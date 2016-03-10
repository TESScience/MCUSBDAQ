import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


VERSION = "0.0.1"

setup(
    name="mcc",
    version=VERSION,
    author="Charles Risicato",
    description=("A library for interacting with the MCC USB-TEMP DAQ"),
    license="GPL3",
    keywords="hardware daq usb hidapi",
    url="https://github.com/TESScience/MCUSBDAQ",
    packages=['mcc'],
    download_url='https://github.com/TESScience/MCUSBDAQ/tarball/{VERSION}'.format(VERSION=VERSION),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    scripts=['temperature_monitor'],
    requires=['hidapi']
)
