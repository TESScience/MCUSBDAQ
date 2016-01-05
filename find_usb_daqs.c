#include "find_usb_daqs.h"
#include <stdio.h>

// TODO: make Python datastructure that exposes
// - Vendor
// - Manufacturer
// - ProdID
// - Product
// - Rev
// - SerialNumber

void findMCUSBDAQs() {
    struct usb_bus *bus;
    struct usb_device *dev;
    struct usb_bus *busses;
  
    usb_init();
    usb_find_busses();
    usb_find_devices();
    busses = usb_get_busses();
  
    for (bus = busses; bus; bus = bus->next)
      for (dev = bus->devices; dev; dev = dev->next)
        if (dev->descriptor.idVendor == MCC_VID)
          printf("Found a Measurement Computing Device\n");
}
