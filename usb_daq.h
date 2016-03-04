#pragma once
#include <usb.h>
#include <Python.h>

#define MCC_VID (0x09db)
#define HOST_TO_DEVICE (0x0 << 7)
#define VENDOR_TYPE (0x2 << 5)
#define DEVICE_RECIPIENT (0x0)
// TODO: this code number changes depending on the device
#define BLINK_LED (0x40)

// Measurement Computing Constants
#define FS_DELAY 10000

/* USB Request */
enum {
  GET_REPORT             = 1,
  GET_IDLE               = 2,
  GET_PROTOCOL           = 3,
  SET_REPORT             = 9,
  SET_IDLE               = 0x0A,
  SET_PROTOCOL           = 0x0B
};

#define  INPUT_REPORT      (1 << 8)
#define  OUTPUT_REPORT     (2 << 8)
#define  FEATURE_REPORT    (3 << 8)

typedef struct {
    PyObject_HEAD
    PyObject * serial;
} usb_daq;

PyTypeObject usb_daq_PyType;

PyObject* find_usb_daqs(PyObject* self, PyObject* args);
