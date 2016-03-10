import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mcc",
    version = "0.0.1",
    author = "Charles Risicato",
    description = ("A library for interacting with the MCC USB-TEMP DAQ"),
    license = "GPL3",
    keywords = "hardware daq usb hidapi",
    url = "https://github.com/TESScience/MCUSBDAQ",
    packages = ['mcc'],
    long_description = read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    requires=['hidapi']
)
