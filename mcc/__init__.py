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

import hid
import mccusbtemp


class USBTemp(object):
    def __init__(self, serial_number,
                 parameters=mccusbtemp.parameters,
                 digital_port_direction="IN"):
        self.parameters = parameters
        self.vendor_id = self.parameters["VENDOR_ID"]
        self.product_id = self.parameters["PRODUCT_ID"]
        self._hid_device = hid.device()
        for device in hid.enumerate(self.vendor_id, self.product_id):
            if serial_number == device['serial_number']:
                self._hid_device.open_path(device['path'])
                break
        else:
            raise ValueError("Invalid serial number")

        self.serial_number = self._hid_device.get_serial_number_string()
        assert self.serial_number == serial_number, \
            "Incorrect serial number; expected {expected} but was {actual}".format(
                expected=serial_number, actual=self.serial_number)
        self.manufacturer = self._hid_device.get_manufacturer_string()
        self.product = self._hid_device.get_product_string()
        self.set_digital_port_direction(digital_port_direction)

    def __del__(self):
        self._hid_device.close()

    def _read_data(self, report_id, length=129, timeout=500, retries=10):
        """Read data from the device; output must have the designated report_id"""
        for _ in range(retries):
            output = self._hid_device.read(length, timeout)
            if len(output) is not 0:
                assert output[0] is report_id, \
                    "Expected output report id to be 0x{report_id:02X}, was 0x{actual:02X}".format(
                        report_id=report_id, actual=output[0] if isinstance(output, list) else None)
                return output

    def get_status(self):
        """Report the status of the device"""
        get_status = self.parameters["GET_STATUS"]
        self._hid_device.write([get_status, 0, 0])
        d = self._read_data(get_status)
        return d[1] if d else None

    def _wait_while_busy(self):
        """Spin wait while the device reports its status as non-zero (busy)"""
        while self.get_status() != 0:
            pass

    def calibrate(self):
        calibrate = self.parameters["CALIBRATE"]
        self._hid_device.write([calibrate])
        self._wait_while_busy()

    def blink(self):
        """Blink the on-board LED"""
        blink_led = self.parameters["BLINK_LED"]
        self._hid_device.write([blink_led, 0, 0])

    # TODO: I am broken; when I run I kill the device
    def reset(self):
        """Reset the device"""
        reset = self.parameters["RESET"]
        self._hid_device.write([reset, 0, 0])

    def set_digital_port_direction(self, direction):
        """
        Set the digital port direction
        :param direction: either "IN" or "OUT"
        """
        from mccusbtemp import DCONFIG
        assert direction in ["IN", "OUT"], \
            'Direction must be either "IN" or "OUT", was {}'.format(direction)
        dconfig = self.parameters["DCONFIG"]
        direction_code = {"IN": self.parameters["DIO_DIR_IN"],
                          "OUT": self.parameters["DIO_DIR_OUT"]}[direction]
        self._hid_device.write([dconfig, direction_code])

    # TODO: Test me
    def set_digital_port_bit_direction(self, bit_number, direction):
        """
        Set a digital port bit direction
        :param bit_number: The number of the bit to set
        :param direction: The direction to set the bit
        """
        assert direction in ["IN", "OUT"], \
            'Direction must be either "IN" or "OUT", was {}'.format(direction)
        dconfig_bit = self.parameters["DCONFIG_BIT"]
        direction_code = {"IN": self.parameters["DIO_DIR_IN"],
                          "OUT": self.parameters["DIO_DIR_OUT"]}[direction]
        self._hid_device.write([dconfig_bit, bit_number, direction_code])

    # TODO: Test me
    def read_digital_port(self):
        """Read the digital port"""
        din = self.parameters["DIN"]
        self._hid_device.write([din, 0, 0])
        d = self._read_data(din, 2)
        return d[1] if d else None

    # TODO: Test me ... also shouldn't this take a bit number as an argument or something?
    def read_digital_port_bit(self):
        """Read the digital port bit"""
        dbit_in = self.parameters["DBIT_IN"]
        self._hid_device.write([dbit_in])
        d = self._read_data(dbit_in, 2)
        return d[1] if d else None

    # TODO: Test me, write better documentation
    def write_digital_port(self, value):
        """
        Write to the digital output port
        :param value:
        :return:
        """
        return self._hid_device.write([self.parameters["DOUT"], value])

    # TODO: Test me, write better documentation
    def write_digital_port_bit(self, value):
        """
        Write to the digital output port bit
        :param value:
        :return:
        """
        return self._hid_device.write([self.parameters["DBIT_OUT"], value])

    # TODO: Test me
    def read_channel_temperature(self, channel):
        """
        Read the temperature from a particular channel
        :param channel: A channel number
        :return: A floating point temperature in Celsius from an attached RTD
        """
        from struct import unpack
        ch0 = self.parameters["CH0"]
        ch7 = self.parameters["CH7"]
        units = self.parameters["TEMPERATURE_UNITS"]  # or RAW_UNITS?!?
        tin = self.parameters["TIN"]
        assert ch0 <= channel <= ch7, \
            ("Channel {channel} out of range "
             "(must be greater than or equal to 0x{CH0:02X} and "
             "less than or equal to 0x{CH7:02X})").format(channel=channel, CH0=ch0, CH7=ch7)
        self._hid_device.write([tin, channel, units, 0x0])
        d = self._read_data(tin, 5)
        return unpack('f', ''.join(chr(b) for b in d[1:]))[0] if d else -9999.0

    def scan_channel_temperatures(self, start=None, end=None):
        """
        Scan channels for temperatures
        :param start: Starting channel for scan
        :param end: Ending channel for scan
        :return: A list of floating point temperatures in Celsius from attached RTDs
        """
        from struct import unpack
        ch0 = self.parameters["CH0"]
        ch7 = self.parameters["CH7"]
        if start is None:
            start = ch0
        if end is None:
            end = ch7
        assert ch0 <= start <= end <= ch7, \
            ("Invalid start and end channels "
             "(need 0x{CH0:02X} <= (start : 0x{start:02X}) <= (end : 0x{end:02X}) <= 0x{CH7:02X})").format(
                start=start, end=end, CH0=ch0, CH7=ch7)
        units = self.parameters["TEMPERATURE_UNITS"]  # or RAW_UNITS?!?
        tin_scan = self.parameters["TIN_SCAN"]
        number_of_channels = 1 + (end - start)
        self._hid_device.write([tin_scan, start, end, units, 0x0])
        d = self._read_data(tin_scan, 1 + (4 * number_of_channels))
        return unpack(str(number_of_channels) + 'f', ''.join(chr(b) for b in d[1:])) if d else ()

    # TODO: Test me
    def read_memory(self, address, data_type, count):
        """
        Read a memory address
        :param address: Integer representing the address to write to
        :param data_type: Either 0 or 1
        :param count: The number of values to read starting with the specified address
        :return: An array of values from the device memory
        """
        assert data_type in [0, 1], "The data_type specified must be 0 or 1, was {}".format(data_type)
        if (count > 62) and (data_type == 0):
            count = 62
        if (count > 60) and (data_type == 1):
            count = 60
        mem_read = self.parameters["MEM_READ"]
        self._hid_device.write([mem_read, address, data_type, count])
        d = self._read_data(mem_read, 1 + count)
        return d[1:] if d else []

    # TODO: Test me
    def write_memory(self, address, data_type, count, data):
        """
        Write to a memory address
        :param address: Integer address to write to
        :param data_type: Either 0 or 1
        :param count: The number of values to write
        :param data: The data to write (a list!??)
        :return: ?
        """
        from mccusbtemp import MEM_WRITE
        max_address = 0x0100
        assert address < 0x0100, \
            "Memory address out of range; address cannot exceed 0x{max_address:02X} (was 0x{actual:02X})".format(
                max_address=max_address, actual=address
            )
        # assert data_type in [0,1], "The data_type specified must be 0 or 1, was {}".format(data_type)
        count = min(count, 59)
        # Shouldn't count = len(data) if data is a list?
        return self._hid_device.write([MEM_WRITE, address, data_type, count, data])

    # TODO: Test me
    def get_item(self, item, sub_item):
        """
        Read the value in a item/sub-item pair
        :param item: The item to read (Integer)
        :param sub_item: The sub-item to read (Integer)
        :return: list of values associated with the item/sub-item pair
        """
        get_item = self.parameters["GET_ITEM"]
        self._hid_device.write([get_item, item, sub_item])
        d = self._read_data(get_item)
        return d[1:] if d else None

    # TODO: Test me
    # TODO: value isn't used! What is going on?!
    def set_item(self, item, sub_item, value):
        """
        Set an item/sub-item pair to a particular value
        :param item: The item to set (Integer)
        :param sub_item: The sub-item to set (Integer)
        :param value: The value to set the item/sub-item pair to
        :return: ?
        """
        from mccusbtemp import ADC_3, GET_ITEM
        low = 0
        high = ADC_3
        # Shouldn't this be 'value' not 'item'?
        if not 0 <= item <= high:
            raise Exception("Could not set item {item} "
                            "(must be greater than or equal to {low} "
                            "and less than or equal to {high})".format(low=low, high=high))
        return self._hid_device.write([GET_ITEM, item, sub_item])

    def get_burnout_status(self, mask):
        """
        Determine if a particular channel has a sensor attached
        :param mask:
        :return:
        """
        get_burnout_status = mccusbtemp.parameters["GET_BURNOUT_STATUS"]
        self._hid_device.write([get_burnout_status, 0, 0])
        d = self._read_data(get_burnout_status, 2)
        return d[1] & mask if d else None


def find_devices(vendor_id=mccusbtemp.parameters["VENDOR_ID"],
                 product_id=mccusbtemp.parameters["PRODUCT_ID"],
                 digital_port_direction="IN"):
    """
    Find all of the USBTemp devices on the USB chain
    :param vendor_id: Optional vendor identification number
    :param product_id: Optional product number
    :param digital_port_direction: Either "IN" or "OUT"
    :return:
    """
    return [USBTemp(device["serial_number"], digital_port_direction=digital_port_direction)
            for device in hid.enumerate(vendor_id, product_id)]
