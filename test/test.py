#!/usr/bin/env python

import mcusbdaq

print "Imported mcusbdaq successfully!"

for d in mcusbdaq.find_usb_daqs():
	print "-----------------------"
	print "Serial Number:", d.serial
	print "Product ID:", d.product_id
	print "Vendor ID:", d.vendor_id
	print "Manufacturer:", d.manufacturer
	print "Product Name:", d.product
	d.blink(5)
