# MCUSBDAQ

This module provides a library for interacting with the MCC USB-TEMP Temperature DAQ.

http://www.mccdaq.com/usb-data-acquisition/USB-TEMP-Series.aspx

## Installation

For convenience, this package provides a *testsuite* which can be
installed by typing at the prompt:

    make install_testsuite

Alternatively, you can install this module with `pip`:

    pip install git+https://github.com/TESScience/MCUSBDAQ.git

It is also necessary to place [99-mcc.rules][1] in `/etc/udev/rules.d` ; see [INSTALL][2] for details.

[1]: https://raw.githubusercontent.com/TESScience/MCUSBDAQ/master/99-mcc.rules
[2]: https://raw.githubusercontent.com/TESScience/MCUSBDAQ/master/INSTALL

## Usage

### `temperature_monitor`

To run the `temperature_monitor` script, type in this directory:


    (make testsuite_install ;
     source testsuite/venv/bin/activate ;
     temperature_monitor)


Alternatively, if you installed this module via `pip` you can just type:

    temperature_monitor
