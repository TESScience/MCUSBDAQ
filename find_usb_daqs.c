#include "find_usb_daqs.h"
#include <stdio.h>
#include <structmember.h>

// TODO: make Python datastructure that exposes
// - Vendor
// - Manufacturer
// - ProdID
// - Product
// - Rev
// - SerialNumber

static void usb_daq_dealloc(usb_daq* self) {
    self->ob_type->tp_free((PyObject*)self);
}

static PyMemberDef usb_daq_members[] = {
    {"vendor_id", T_INT, offsetof(usb_daq, vendor_id), 0,
     "Vendor Identification Number"},
    {"product", T_INT, offsetof(usb_daq, product_id), 0,
     "Product Identification Number"},
    {NULL}  /* Sentinel */
};

PyTypeObject usb_daq_PyType = {
    PyObject_HEAD_INIT(NULL)
    0,                                                       /* ob_size */
    "mcusbdaq.usb_daq",                                      /* tp_name */
    sizeof(usb_daq),                                         /* tp_basicsize */
    0,                                                       /* tp_itemsize */
    (destructor)usb_daq_dealloc,                             /* tp_dealloc */
    0,                                                       /* tp_print */
    0,                                                       /* tp_getattr */
    0,                                                       /* tp_setattr */
    0,                                                       /* tp_compare */
    0,                                                       /* tp_repr */
    0,                                                       /* tp_as_number */
    0,                                                       /* tp_as_sequence */
    0,                                                       /* tp_as_mapping */
    0,                                                       /* tp_hash */
    0,                                                       /* tp_call */
    0,                                                       /* tp_str */
    0,                                                       /* tp_getattro */
    0,                                                       /* tp_setattro */
    0,                                                       /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                /* tp_flags */
    "Measurement Computing data acquisition card object",    /* tp_doc */
    0,		                                             /* tp_traverse */
    0,		                                             /* tp_clear */
    0,		                                             /* tp_richcompare */
    0,		                                             /* tp_weaklistoffset */
    0,		                                             /* tp_iter */
    0,		                                             /* tp_iternext */
    // TODO: Add Methods
    0,                                                       /* tp_methods */
    usb_daq_members,                                         /* tp_members */
    0,                                                       /* tp_getset */
    0,                                                       /* tp_base */
    0,                                                       /* tp_dict */
    0,                                                       /* tp_descr_get */
    0,                                                       /* tp_descr_set */
    0,                                                       /* tp_dictoffset */
    // TODO: Write Init
    //(initproc)Noddy_init,                                    /* tp_init */
    0,                                                       /* tp_init */
    0,                                                       /* tp_alloc */
    // TODO: Write new
    //Noddy_new,                                               /* tp_new */
    0,                                                         /* tp_new */
};

static PyObject* usb_daq_obj_from_usb_device(struct usb_device * dev) {
    usb_dev_handle *udev = usb_open(dev);
    char serial_number[256] = {0x0};
    char product[256] = {0x0};
    char manufacturer[256] = {0x0};
    if (udev) {
      if (dev->descriptor.iSerialNumber) {
        // TODO: Throw exception if this fails
        usb_get_string_simple(udev, dev->descriptor.iSerialNumber, serial_number, sizeof(serial_number)); 
      }
      if (dev->descriptor.iProduct) {
        // TODO: Throw exception if this fails
        usb_get_string_simple(udev, dev->descriptor.iManufacturer, manufacturer, sizeof(manufacturer)); 
      }
      if (dev->descriptor.iProduct) {
        // TODO: Throw exception if this fails
        usb_get_string_simple(udev, dev->descriptor.iProduct, product, sizeof(product)); 
      }
      usb_close(udev);
    }

    // TODO: Create a usb_daq device and add it to a list of them
    printf("Found a Measurement Computing Device\n"
           "Product ID: %i\n"
           "Vendor ID: %i\n"
           "Product Name: %s\n"
           "Manufacturer Name: %s\n"
           "Serial Number: %s\n",
           dev->descriptor.idProduct,
           dev->descriptor.idVendor,
           product,
           manufacturer,
           serial_number
          );

    Py_RETURN_NONE;
}

PyObject* find_usb_daqs(PyObject* self, PyObject* args) {
    struct usb_bus *bus;
    struct usb_device *dev;
  
    usb_init();
    usb_find_busses();
    usb_find_devices();
  
    for (bus = usb_get_busses(); bus != NULL; bus = bus->next)
      for (dev = bus->devices; dev != NULL; dev = dev->next)
        if (dev->descriptor.idVendor == MCC_VID) {
          usb_daq_obj_from_usb_device(dev);
       }

    Py_RETURN_NONE;
}

