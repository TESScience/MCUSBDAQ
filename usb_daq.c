#ifndef USB_DAQ_C
#define USB_DAQ_C
#include "usb_daq.h"
#include <stdio.h>
#include <structmember.h>
#include <stdint.h>

static void inline cleanup_usb_dev_handle(usb_dev_handle *udev)
{
  if (udev) {
    usb_clear_halt(udev, USB_ENDPOINT_IN|1);
    usb_clear_halt(udev, USB_ENDPOINT_OUT|1);
    usb_release_interface(udev, 0);
    usb_close(udev);
  }
}

// In order to enable "hot-swapping" of USB devices, 
// we will in general only keep track of the serial number of the data acquisition card.
// The USB device is then looked up every time we need to query the specified device
static struct usb_device * find_usb_device_by_serial(const char * serial_number_to_search_for) {
    struct usb_bus *bus;
    struct usb_device *dev;
  
    usb_init();
    usb_find_busses();
    usb_find_devices();
  
    for (bus = usb_get_busses(); bus != NULL; bus = bus->next)
      for (dev = bus->devices; dev != NULL; dev = dev->next) {
         if (dev->descriptor.iSerialNumber) {
           char device_serial_number[256] = {0x0};
           usb_dev_handle *udev = usb_open(dev);
           usb_get_string_simple(udev, dev->descriptor.iSerialNumber, device_serial_number, sizeof(device_serial_number)); 
           cleanup_usb_dev_handle(udev);
           if (! strcmp(device_serial_number, serial_number_to_search_for)) 
              return dev;
         }
       }
    return NULL;
}

// Cargo Culted from MCC's pmd.c ; see ftp://lx10.tx.ncsu.edu/pub/Linux/drivers/USB/
int SendOutputReport(usb_dev_handle * dev_handle, const uint8_t reportID, const uint8_t * vals, int num_vals, int delay)
{
  int ret;

  if (reportID == 0) { // use interrupt endpoint 1
    ret = usb_interrupt_write(dev_handle, USB_ENDPOINT_OUT | 1, (char *) vals, num_vals, delay);
    if (ret != num_vals) { // try one more time:
      ret = usb_interrupt_write(dev_handle, USB_ENDPOINT_OUT | 1, (char *) vals, num_vals, delay);
    }
  } else { // use the control endpoint (Some FS devices use this)
    ret = usb_control_msg(dev_handle,
                          (USB_TYPE_CLASS| USB_RECIP_INTERFACE),
                          SET_REPORT,
                          (OUTPUT_REPORT | reportID),
                          0,
                          (char *) vals,
                          num_vals,
                          delay);
  }
  return ret;
}

static PyObject * usb_daq_blink(const usb_daq *self, PyObject *args, PyObject *kwds)
{
  struct usb_device * dev = find_usb_device_by_serial(PyString_AsString(self->serial));
  int count;
  static char *kwlist[] = {"count", NULL};
   
  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, &count)) {
      // TODO: Raise exception
      return NULL; 
  }

  if (! count ) {
      // TODO: Raise exception
      return NULL; 
  }


  if (! dev ) {
     // TODO: Raise exception
     return NULL;
  } else {
     usb_dev_handle * dev_handle = usb_open(dev);
     const uint8_t blink_code = BLINK_LED;
     int ret = usb_interrupt_write(dev_handle, USB_ENDPOINT_OUT | 1, (char *) &blink_code, sizeof(blink_code), FS_DELAY);
     fprintf(stderr, "Got return value: %i from blinking\n", ret);
     cleanup_usb_dev_handle(dev_handle);
  }
  Py_RETURN_NONE;
}

static PyMethodDef usb_daq_methods[] = {
    {"blink", (PyCFunction)usb_daq_blink, (METH_VARARGS | METH_KEYWORDS),
     "Blink the USB DAQ's LED"},
    {NULL}  /* Sentinel */
};

// Getter for the vendor_id (an int) of a usb_daq object
static PyObject * usb_daq_get_vendor_id(const usb_daq *self, const void *closure) {
    const struct usb_device * dev = find_usb_device_by_serial(PyString_AsString(self->serial));
    if (! dev ) {
       // TODO: raise exception
       return NULL;
    } else return PyInt_FromLong(dev->descriptor.idVendor);
}

// Getter for the product_id (an int) of a usb_daq object
static PyObject * usb_daq_get_product_id(const usb_daq *self, const void *closure) {
    const struct usb_device * dev = find_usb_device_by_serial(PyString_AsString(self->serial));
    if (! dev ) {
       // TODO: raise exception
       return NULL;
    } else return PyInt_FromLong(dev->descriptor.idProduct);
}

// Getter for the manufacturer (string) of a usb_daq object
static PyObject * usb_daq_get_manufacturer(const usb_daq *self, const void *closure) {
    struct usb_device * dev = find_usb_device_by_serial(PyString_AsString(self->serial));
    if (! dev ) {
       // TODO: raise exception
       return NULL;
    } else {
       usb_dev_handle * udev = usb_open(dev);
       char manufacturer[256] = {0x0};
       usb_get_string_simple(udev, dev->descriptor.iManufacturer, manufacturer, sizeof(manufacturer)); 
       return PyString_FromString(manufacturer);
    }
}

// Getter for the product (string) of a usb_daq object
static PyObject * usb_daq_get_product(const usb_daq *self, const void *closure) {
    struct usb_device * dev = find_usb_device_by_serial(PyString_AsString(self->serial));
    if (! dev ) {
       // TODO: raise exception
       return NULL;
    } else {
       usb_dev_handle * udev = usb_open(dev);
       char product[256] = {0x0};
       usb_get_string_simple(udev, dev->descriptor.iProduct, product, sizeof(product)); 
       return PyString_FromString(product);
    }
}

// TODO: Setting these attributes should raise an exception
static PyGetSetDef usb_daq_getseters[] = {
    {"vendor_id", (getter)usb_daq_get_vendor_id, NULL /* No setter */,
     "Vendor identification number",
     NULL},
    {"product_id", (getter)usb_daq_get_product_id, NULL /* No setter */,
     "Product identification number",
     NULL},
    {"manufacturer", (getter)usb_daq_get_manufacturer, NULL /* No setter */,
     "Manufacturer name",
     NULL},
    {"product", (getter)usb_daq_get_product, NULL /* No setter */,
     "Product name",
     NULL},
    {NULL}  /* Sentinel */
};


static PyMemberDef usb_daq_members[] = {
    {"serial", T_OBJECT_EX, offsetof(usb_daq, serial), 0, "Serial number"},
    {NULL}  /* Sentinel */
};

static void usb_daq_dealloc(usb_daq* self) {
    Py_XDECREF(self->serial);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject * usb_daq_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    usb_daq * self;
    self = (usb_daq *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->serial = PyString_FromString("");
        if (self->serial == NULL) {
          Py_DECREF(self);
          return NULL;
        }
    }
    return (PyObject *)self;
}


static int
usb_daq_init(usb_daq *self, PyObject *args, PyObject *kwds)
{
    PyObject *serial=NULL, *tmp;

    static char *kwlist[] = {"serial", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &serial))
        return -1; 

    if (serial) {
        tmp = self->serial;
        Py_INCREF(serial);
        self->serial = serial;
        Py_XDECREF(tmp);
    } else return -1;

    return 0;
}

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
    usb_daq_methods,                                         /* tp_methods */
    usb_daq_members,                                         /* tp_members */
    usb_daq_getseters,                                       /* tp_getset */
    0,                                                       /* tp_base */
    0,                                                       /* tp_dict */
    0,                                                       /* tp_descr_get */
    0,                                                       /* tp_descr_set */
    0,                                                       /* tp_dictoffset */
    (initproc)usb_daq_init,                                  /* tp_init */
    0,                                                       /* tp_alloc */
    usb_daq_new,                                             /* tp_new */
};

static PyObject* usb_daq_obj_from_usb_device(struct usb_device * dev) {
    usb_dev_handle *udev = usb_open(dev);
    if (udev) {
      char serial_number[256] = {0x0};
      if (dev->descriptor.iSerialNumber) {
        // TODO: Raise exception if this fails
        usb_get_string_simple(udev, dev->descriptor.iSerialNumber, serial_number, sizeof(serial_number)); 
      }
      PyObject *argList = Py_BuildValue("(s)", serial_number);
      PyObject *obj = PyObject_CallObject((PyObject *) &usb_daq_PyType, argList);
      Py_DECREF(argList);
      cleanup_usb_dev_handle(udev);
      return obj;
    }
    Py_RETURN_NONE;
}


PyObject* find_usb_daqs(PyObject* self, PyObject* args) {
    struct usb_bus *bus;
    struct usb_device *dev;
    PyObject * results = PyList_New(0);
  
    usb_init();
    usb_find_busses();
    usb_find_devices();
  
    for (bus = usb_get_busses(); bus != NULL; bus = bus->next)
      for (dev = bus->devices; dev != NULL; dev = dev->next)
        if (dev->descriptor.idVendor == MCC_VID) {
          PyList_Append(results, usb_daq_obj_from_usb_device(dev));
        }

    return results;
}
#endif /* USB_DAQ_C */
