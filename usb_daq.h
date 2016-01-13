#pragma once
#include <usb.h>
#include <Python.h>

#define MCC_VID (0x09db)
#define HOST_TO_DEVICE (0x0 << 7)
#define VENDOR_TYPE (0x2 << 5)
#define DEVICE_RECIPIENT (0x0)
// TODO: this code number changes depending on the device
#define BLINK_LED (0x40)

// Why is this constant important?!?
#define HS_DELAY 2000

typedef struct {
    PyObject_HEAD
    PyObject * serial;
} usb_daq;

PyTypeObject usb_daq_PyType;

PyObject* find_usb_daqs(PyObject* self, PyObject* args);
