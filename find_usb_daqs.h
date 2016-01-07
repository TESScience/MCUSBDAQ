#ifndef FIND_USB_DAQS_H
#define FIND_USB_DAQS_H
#include <usb.h>
#include <Python.h>
#define MCC_VID (0x09db)

typedef struct {
    PyObject_HEAD
    uint16_t vendor_id, product_id;
} usb_daq;

PyTypeObject usb_daq_PyType;

PyObject* find_usb_daqs(PyObject* self, PyObject* args);

#endif /* FIND_USB_DAQS_H */
