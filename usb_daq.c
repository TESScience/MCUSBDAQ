#include "usb_daq.h"
#include <stdio.h>
#include <structmember.h>

static PyMemberDef usb_daq_members[] = {
    {"vendor_id", T_OBJECT_EX, offsetof(usb_daq, vendor_id), 0,
     "Vendor identification number"},
    {"product_id", T_OBJECT_EX, offsetof(usb_daq, product_id), 0,
     "Product identification number"},
    {"manufacturer", T_OBJECT_EX, offsetof(usb_daq, manufacturer), 0,
     "Manufacturer name"},
    {"product", T_OBJECT_EX, offsetof(usb_daq, product), 0,
     "Product name"},
    {"serial", T_OBJECT_EX, offsetof(usb_daq, serial), 0,
     "Serial number"},
    {NULL}  /* Sentinel */
};

static void usb_daq_dealloc(usb_daq* self) {
    Py_XDECREF(self->manufacturer);
    Py_XDECREF(self->product);
    Py_XDECREF(self->serial);
    Py_XDECREF(self->product_id);
    Py_XDECREF(self->vendor_id);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject * usb_daq_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    usb_daq * self;
    self = (usb_daq *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->product = PyString_FromString("");
        if (self->product == NULL) {
          Py_DECREF(self);
          return NULL;
        }
        
        self->manufacturer = PyString_FromString("");
        if (self->manufacturer == NULL) {
          Py_DECREF(self);
          return NULL;
        }

        self->serial = PyString_FromString("");
        if (self->serial == NULL) {
          Py_DECREF(self);
          return NULL;
        }

        self->product_id = PyInt_FromLong(0);
        if (self->product_id == NULL) {
          Py_DECREF(self);
          return NULL;
        }

        self->vendor_id = PyInt_FromLong(0);
        if (self->vendor_id == NULL) {
          Py_DECREF(self);
          return NULL;
        }

        self->dev = 0;
    }
    return (PyObject *)self;
}

static struct usb_device * find_usb_device_by_serial(const char * serial_number_to_search_for) {
    struct usb_bus *bus;
    struct usb_device *dev;
  
    usb_init();
    usb_find_busses();
    usb_find_devices();
  
    for (bus = usb_get_busses(); bus != NULL; bus = bus->next)
      for (dev = bus->devices; dev != NULL; dev = dev->next) {
         if (dev->descriptor.iSerialNumber) {
           char this_serial_number[256] = {0x0};
           usb_dev_handle *udev = usb_open(dev);
           usb_get_string_simple(udev, dev->descriptor.iSerialNumber, this_serial_number, sizeof(this_serial_number)); 
           usb_close(udev);
           if (! strcmp(this_serial_number, serial_number_to_search_for) ) 
              return dev;
         }
       }
	
    return NULL;
}

static int
usb_daq_init(usb_daq *self, PyObject *args, PyObject *kwds)
{
    PyObject *serial=NULL, *tmp;
    usb_dev_handle *udev;

    static char *kwlist[] = {"serial", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &serial))
        return -1; 

    if (serial) {
        tmp = self->serial;
        Py_INCREF(serial);
        self->serial = serial;
        Py_XDECREF(tmp);
    } else return -1;

    if (! (self->dev = find_usb_device_by_serial(PyString_AsString(self->serial))))
        return -1;

    tmp = self->vendor_id;
    self->vendor_id = PyInt_FromLong(self->dev->descriptor.idVendor);
    Py_XDECREF(tmp);

    tmp = self->product_id;
    self->product_id = PyInt_FromLong(self->dev->descriptor.idProduct);
    Py_XDECREF(tmp);

    udev = usb_open(self->dev);

    if (udev) {
      if (self->dev->descriptor.iManufacturer) {
        char manufacturer[256] = {0x0};
        usb_get_string_simple(udev, self->dev->descriptor.iManufacturer, manufacturer, sizeof(manufacturer)); 
        tmp = self->manufacturer;
        self->manufacturer = PyString_FromString(manufacturer);
        Py_XDECREF(tmp);
      }
      if (self->dev->descriptor.iProduct) {
        char product[256] = {0x0};
        usb_get_string_simple(udev, self->dev->descriptor.iProduct, product, sizeof(product)); 
        tmp = self->product;
        self->product = PyString_FromString(product);
        Py_XDECREF(tmp);
      }
      usb_close(udev);
    } else
      return -1;

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
    // TODO: Add Methods
    0,                                                       /* tp_methods */
    usb_daq_members,                                         /* tp_members */
    0,                                                       /* tp_getset */
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
        // TODO: Throw exception if this fails
        usb_get_string_simple(udev, dev->descriptor.iSerialNumber, serial_number, sizeof(serial_number)); 
      }
      PyObject *argList = Py_BuildValue("(s)", serial_number);
      PyObject *obj = PyObject_CallObject((PyObject *) &usb_daq_PyType, argList);
      Py_DECREF(argList);
      usb_close(udev);
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

