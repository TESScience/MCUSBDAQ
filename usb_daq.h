#pragma once
#include <usb.h>
#include <Python.h>
#define MCC_VID (0x09db)

typedef struct {
    PyObject_HEAD
    PyObject * vendor_id, * product_id, * manufacturer, * product, * serial;
    struct usb_device * dev;
} usb_daq;

PyTypeObject usb_daq_PyType;

PyObject* find_usb_daqs(PyObject* self, PyObject* args);
