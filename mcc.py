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
#
import struct
import hid
from mccusbtemp import *

class usb_temp(object):
    def __init__(self, serial_no = None):
        self.h = hid.device()
        if serial_no is None:
            self.h.open(VENDOR_ID, PRODUCT_ID, serial_no)
        else:
            found = False
            dev_list = hid.enumerate(VENDOR_ID, PRODUCT_ID)
            for test_dev in dev_list:
                if serial_no == test_dev['serial_number']:
                    found = True
                    self.h.open_path(test_dev['path'])
                    break
            if not found:
                raise ValueError("Invalid serial number")

    def __del__(self):
        self.h.close()

    def _waitWhileBusy(self):
        while self.getStatus() != 0:
            pass

    def _readData(self, report_id, length = 129, timeout = 500):
        try:
            d = self.h.read(length, timeout)
        except(IOError, ex):
            pass
        return d

    def getStatus(self):
        result = None
        self.h.write([GET_STATUS, 0, 0])
        d = self._readData(GET_STATUS)
        if d:
            reportId = d[0]
            result   = d[1]
        return result

    def calibrate(self):
        self.h.write([CALIBRATE])
        self._waitWhileBusy()

    def flashLED(self):
        self.h.write([BLINK_LED, 0, 0])

    def reset(self):
        self.h.write([RESET, 0, 0])

    def dConfigPort(self, direction):
        self.h.write([DCONFIG, direction])

    def dConfigBit(self, bit_num, direction):
        self.h.write([DCONFIG_BIT, bit_num, direction])

    def dinPort(self):
        result = None
        self.h.write([DIN, 0, 0])
        d = self._readData(DIN, 2)
        if d:
            reportId = d[0]
            result   = d[1]
        return result

    def dinBit(self):
        result = None
        self.h.write([DBIT_IN])
        d = self._readData(DBIT_IN, 2)
        if d:
            reportId = d[0]
            result   = d[1]
        return result

    def doutPort(self, value):
        self.h.write([DOUT, value])

    def doutBit(self, value):
        self.h.write([DBIT_OUT, value])

    def tin(self, channel, units = TEMPERATURE):
        result = -9999.9
        self.h.write([TIN, channel, units, 0x0])
        d = self._readData(TIN, 5)
        if d:
            reportId = d[0]
            cs = ""
            for b in d[1:]:
                cs = cs + chr(b)
            result = struct.unpack('f', cs)[0]
        return result

    def tinScan(self, start, end, units = TEMPERATURE):
        result = ()
        nchan = 1 + (end - start)
        self.h.write([TIN_SCAN, start, end, units, 0x0])
        d = self._readData(TIN_SCAN, 1 + (4 * nchan))
        if d:
            reportId = d[0]
            cs = ""
            for b in d[1:]:
                cs = cs + chr(b)
            result = struct.unpack(str(nchan) + 'f', cs)
        return list(result)

    def readMemory(self, address, dtype, count):
        memory = []
        if (count > 62) and (dtype == 0):
            count = 62
        if (count > 60) and (dtype == 1):
            count = 60
        self.h.write([MEM_READ, address, dtype, count])
        d = self._readData(MEM_READ, 1 + count)
        if d:
            reportId = d[0]
            memory.append(d[1:])
        return memory

    def writeMemory(self, address, dtype, count, data):
        result = False
        if address < 0x0100:
            if (count > 59):
                count = 59
            self.h.write([MEM_WRITE, address, dtype, count, data])
            result = True
        return result

    def getItem(self, item, sub_item):
        self.h.write([GET_ITEM, item, sub_item])
        d = self._readData(GET_ITEM)
        if d:
            reportId = d[0]
            value    = d[1:]
        return value

    def setItem(self, item, sub_item, value):
        if item > ADC_3:
            raiseException
        self.h.write([GET_ITEM, item, sub_item])

    def getBurnoutStatus(self, mask):
        result = None
        self.h.write([GET_BURNOUT_STATUS, 0, 0])
        d = self._readData(GET_BURNOUT_STATUS, 2)
        if d:
            reportId = d[0]
            result   = d[1] & mask
        return result
