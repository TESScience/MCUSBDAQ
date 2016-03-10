# MCUSBDAQ

This module provides a library for interacting with the MCC USB-TEMP Temperature DAQ.

http://www.mccdaq.com/usb-data-acquisition/USB-TEMP-Series.aspx

## Installation

For convenience, this package provides a *testsuite* which can be
installed by typing at the prompt:

```bash
make install_testsuite
```

Alternatively, you can install this module with `pip`

```bash
pip install git+https://github.com/TESScience/MCUSBDAQ.git
```

It is also necessary to place [99-mcc.rules](https://raw.githubusercontent.com/TESScience/MCUSBDAQ/master/99-mcc.rules) in `/etc/udev/rules.d` ; see [INSTALL](https://raw.githubusercontent.com/TESScience/MCUSBDAQ/master/INSTALL) for details.

## Usage

### `temperature_monitor`

To run the `temperature_monitor` script, type in this directory:

```bash
(make testsuite_install ;
 source testsuite/venv/bin/activate ;
 temperature_monitor)
```

Alternatively, if you installed this module via `pip` you can type:

```bash
temperature_monitor
```
