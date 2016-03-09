# -*- mode: python; encoding: utf-8 -*-
#
#  Support module to drive Measurement Computings USB-TEMP temperature
#  from a GNU/Linux environment.
#
#  This module was developed by:
#    Rattlesnake Hill Technologies Inc. <chuck@rattlesnake-hill.com>
#  for:
#    The TESS project at the MIT Kalvi Institute for Astrophysics and
#    Space Research 
#
#  The code is adapted from the GNU/Linux software available on the mccdaq
#  website.
#
#    ftp://lx10.tx.ncsu.edu/pub/Linux/drivers/USB/
#
#  This code is licensed under the terms of the GPL Version 2.  See the
#  file COPYING for a copy of the license or visit:
#
#    http://www.gnu.org/licenses/gpl-2.0.txt

import struct
import hid
import mccusbtemp


class usb_temp(object):
    def __init__(self, serial_number=None):
        from mccusbtemp import VENDOR_ID, PRODUCT_ID
        self._hid_device = hid.device()
        if serial_number is None:
            self._hid_device.open(VENDOR_ID, PRODUCT_ID, serial_number)
        else:
            found = False
            dev_list = hid.enumerate(VENDOR_ID, PRODUCT_ID)
            for test_dev in dev_list:
                if serial_number == test_dev['serial_number']:
                    found = True
                    self._hid_device.open_path(test_dev['path'])
                    break
            if not found:
                raise ValueError("Invalid serial number")

    def __del__(self):
        self._hid_device.close()

    def _waitWhileBusy(self):
        while self.getStatus() != 0:
            pass

    def _readData(self, report_id, length=129, timeout=500):
        try:
            d = self._hid_device.read(length, timeout)
        except IOError:
            pass
        return d

    def getStatus(self):
        "Report the status of the device"
        from mccusbtemp import GET_STATUS
        result = None
        self._hid_device.write([GET_STATUS, 0, 0])
        d = self._readData(GET_STATUS)
        if d:
            # TODO: Don't just throw this away
            reportId = d[0]
            result = d[1]
        return result

    def calibrate(self):
        from mccusbtemp import CALIBRATE
        self._hid_device.write([CALIBRATE])
        self._waitWhileBusy()

    def flashLED(self):
        from mccusbtemp import BLINK_LED
        self._hid_device.write([BLINK_LED, 0, 0])

    def reset(self):
        from mccusbtemp import RESET
        self._hid_device.write([RESET, 0, 0])

    def dConfigPort(self, direction):
        from mccusbtemp import DCONFIG
        self._hid_device.write([DCONFIG, direction])

    def dConfigBit(self, bit_num, direction):
        from mccusbtemp import DCONFIG_BIT
        self._hid_device.write([DCONFIG_BIT, bit_num, direction])

    def dinPort(self):
        from mccusbtemp import DIN
        result = None
        self._hid_device.write([DIN, 0, 0])
        d = self._readData(DIN, 2)
        if d:
            # TODO: Don't throw this away
            reportId = d[0]
            result = d[1]
        return result

    def dinBit(self):
        from mccusbtemp import DBIT_IN
        result = None
        self._hid_device.write([DBIT_IN])
        d = self._readData(DBIT_IN, 2)
        if d:
            reportId = d[0]
            result = d[1]
        return result

    def doutPort(self, value):
        from mccusbtemp import DOUT
        self._hid_device.write([DOUT, value])

    def doutBit(self, value):
        from mccusbtemp import DBIT_OUT
        self._hid_device.write([DBIT_OUT, value])

    def tin(self, channel, units=mccusbtemp.TEMPERATURE_UNITS):
        from mccusbtemp import TIN, CH0, CH7
        result = float('NaN')
        if not CH0 <= channel <= CH7:
            raise Exception("Channel {channel} out of range "
                            "(must be greater than or equal to 0x{CH0:02X} and "
                            "less than or equal to 0x{CH7:02X})".format(
                channel=channel,
                CH0=CH0,
                CH7=CH7))
        self._hid_device.write([TIN, channel, units, 0x0])
        d = self._readData(TIN, 5)
        if d:
            #reportId = d[0]
            cs = ""
            for b in d[1:]:
                cs = cs + chr(b)
            result = struct.unpack('f', ''.join(chr(b) for b in d[1:]))[0]
        return result

    def tinScan(self,
                start=mccusbtemp.CH0,
                end=mccusbtemp.CH7,
                units=mccusbtemp.TEMPERATURE_UNITS):
        from mccusbtemp import TIN_SCAN
        number_of_channels = 1 + (end - start)
        self._hid_device.write([TIN_SCAN, start, end, units, 0x0])
        d = self._readData(TIN_SCAN, 1 + (4 * number_of_channels))
        if d:
            # reportId = d[0]
            return struct.unpack(str(number_of_channels) + 'f', ''.join(chr(b) for b in d[1:]))
        return ()

    def readMemory(self, address, dtype, count):
        from mccusbtemp import MEM_READ
        memory = []
        if (count > 62) and (dtype == 0):
            count = 62
        if (count > 60) and (dtype == 1):
            count = 60
        self._hid_device.write([MEM_READ, address, dtype, count])
        d = self._readData(MEM_READ, 1 + count)
        if d:
            # reportId = d[0]
            memory.append(d[1:])
        return memory

    def writeMemory(self, address, dtype, count, data):
        from mccusbtemp import MEM_WRITE
        result = False
        if address < 0x0100:
            if (count > 59):
                count = 59
            self._hid_device.write([MEM_WRITE, address, dtype, count, data])
            result = True
        return result

    def getItem(self, item, sub_item):
        from mccusbtemp import GET_ITEM
        self._hid_device.write([GET_ITEM, item, sub_item])
        d = self._readData(GET_ITEM)
        if d:
            # reportId = d[0]
            return d[1:]

    def setItem(self, item, sub_item, value):
        from mccusbtemp import ADC_3, GET_ITEM
        low = 0
        high = ADC_3
        if not 0 <= item <= high:
            raise Exception("Could not set item {item}"
                            "(must be greater than or equal to {low}"
                            "and less than or equal to {high})".format(
                low=low, high=high
            ))
        self._hid_device.write([GET_ITEM, item, sub_item])

    def getBurnoutStatus(self, mask):
        from mccusbtemp import GET_BURNOUT_STATUS
        result = None
        self._hid_device.write([GET_BURNOUT_STATUS, 0, 0])
        d = self._readData(GET_BURNOUT_STATUS, 2)
        if d:
            reportId = d[0]
            result = d[1] & mask
        return result
