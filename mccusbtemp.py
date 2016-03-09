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

VENDOR_ID   = 0x09db
PRODUCT_ID  = 0x008d

DIO_DIR_IN  = 0x01
DIO_DIR_OUT = 0x00

# Commands and HID Report ID for USB TEMP
#
# Digital I/O commands
#
DCONFIG     = 0x01     # Configure digital port
DCONFIG_BIT = 0x02     # Configure individual digital port bits
DIN         = 0x03     # Read digital port
DOUT        = 0x04     # Write digital port
DBIT_IN     = 0x05     # Read digital port bit
DBIT_OUT    = 0x06     # Write digital port bit

#
# Temperature input commands
#
TIN         = 0x18     # Read input channel
TIN_SCAN    = 0x19     # Read multiple input channels

# Memory Commands
MEM_READ    = 0x30     # Read Memory
MEM_WRITE   = 0x31     # Write Memory

# Miscellaneous Commands
BLINK_LED          = 0x40  # Causes LED to blink
RESET              = 0x41  # Reset USB interface
GET_STATUS         = 0x44  # Get device status
SET_ITEM           = 0x49  # Set a configuration item
GET_ITEM           = 0x4A  # Get a configuration item
CALIBRATE          = 0x4B  # Perform a channel calibration
GET_BURNOUT_STATUS = 0x4C  # Get thermocouple burnout detection status

# Code Update Commands
PREPARE_DOWNLOAD   = 0x50  # Prepare for program memory download
WRITE_CODE         = 0x51  # Write program memory
WRITE_SERIAL       = 0x53  # Write a new serial number to device
READ_CODE          = 0x55  # Read program memory

# Command parameters
#
# Channel parameter
CH0  = 0x0   # Channel 0
CH1  = 0x1   # Channel 1
CH2  = 0x2   # Channel 2
CH3  = 0x3   # Channel 3
CH4  = 0x4   # Channel 4
CH5  = 0x5   # Channel 5
CH6  = 0x6   # Channel 6
CH7  = 0x7   # Channel 7
CJC0 = 0x80  # Cold Junction Compensator 0
CJC1 = 0x81  # Cold Junction Compensator 1

# Units parameter
TEMPERATURE = 0x00  #
RAW         = 0x01  #

# Configuration Items
ADC_0 = 0x0  # Setting for ADC 0
ADC_1 = 0x1  # Setting for ADC 1
ADC_2 = 0x2  # Setting for ADC 2
ADC_3 = 0x3  # Setting for ADC 3

# Configuration Sub Items
SENSOR_TYPE     = 0x00  # Sensor type  Read Only
CONNECTION_TYPE = 0x01  # Connection type - RTD & Thermistor
FILTER_RATE     = 0x02  # Filter update rate
EXCITATION      = 0x03  # Currect excitation
VREF            = 0x04  # Measured Vref value
I_value_0       = 0x05  # Measured I value @ 10uA
I_value_1       = 0x06  # Measured I value @ 210uA
I_value_2       = 0x07  # Measured I value @ 10uA (3 wire connection)
V_value_0       = 0x08  # Measured V value @ 10uA
V_value_1       = 0x09  # Measured V value @ 210uA
V_value_2       = 0x0a  # Measured V value @ 210uA (3 wire connection)
CH_0_TC         = 0x10  # Thermocouple type for channel 0
CH_1_TC         = 0x11  # Thermocouple type for channel 1
CH_0_GAIN       = 0x12  # Channel 0 gain value
CH_1_GAIN       = 0x13  # Channel 1 gain value
CH_0_COEF_0     = 0x14  # Coefficient 0
CH_1_COEF_0     = 0x15  # Coefficient 0
CH_0_COEF_1     = 0x16  # Coefficient 1
CH_1_COEF_1     = 0x17  # Coefficient 1
CH_0_COEF_2     = 0x18  # Coefficient 2
CH_1_COEF_2     = 0x19  # Coefficient 2
CH_0_COEF_3     = 0x1a  # Coefficient 3
CH_1_COEF_3     = 0x1b  # Coefficient 3

# Possible Values
RTD           = 0x0
THERMISTOR    = 0x1
THERMOCOUPLE  = 0x2
SEMICONDUCTOR = 0x3
DISABLED      = 0x4

# Sensor configuration
TWO_WIRE_ONE_SENSOR = 0x0
TWO_WIRE_TWO_SENSOR = 0x1
THREE_WIRE          = 0x2
FOUR_WIRE           = 0x3

# Current excitation values */
EXCITATION_OFF = 0x0  #
MU_A_10        = 0x1  # 10 micro Amps
MU_A_210       = 0x2  # 210 micro Amps

# For connection types Semiconductor
SINGLE_ENDED = 0x00
DIFFERENTIAL = 0x01

FREQ_500_HZ   = 0x1
FREQ_250_HZ   = 0x2
FREQ_125_HZ   = 0x3
FREQ_62_5_HZ  = 0x4
FREQ_50_HZ    = 0x5
FREQ_39_2_HZ  = 0x6
FREQ_33_3_HZ  = 0x7
FREQ_19_6_HZ  = 0x8
FREQ_16_7_HZ  = 0x9
# FREQ_16_7_HZ  = 0xa
FREQ_12_5_HZ  = 0xb
FREQ_10_HZ    = 0xc
FREQ_8_33_HZ  = 0xd
FREQ_6_25_HZ  = 0xe
FREQ_4_17_HZ  = 0xf

# Thermocouple types
TYPE_J = 0x0
TYPE_K = 0x1
TYPE_T = 0x2
TYPE_E = 0x3
TYPE_R = 0x4
TYPE_S = 0x5
TYPE_B = 0x6
TYPE_N = 0x7

GAIN_1X   = 0x0
GAIN_2X   = 0x1
GAIN_4X   = 0x2
GAIN_8X   = 0x3
GAIN_16X  = 0x4
GAIN_32X  = 0x5
GAIN_64X  = 0x6
GAIN_128X = 0x7
