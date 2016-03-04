#include <Python.h>
#include "usb_daq.h"
#include "usb_daq.c"

static PyMethodDef MCUSBDAQMethods[] =
{
     {"find_usb_daqs", find_usb_daqs, METH_VARARGS, "Find the USB Measurement Computing data acquisition cards present."},
     {NULL, NULL, 0, NULL}
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initmcusbdaq(void)
{
     PyObject* m;

     if (PyType_Ready(&usb_daq_PyType) < 0)
         return;

     m = Py_InitModule3("mcusbdaq", MCUSBDAQMethods, "A module for handing Measurement Computer data acquisition cards");

     if (m == NULL)
         return;


     Py_INCREF(&usb_daq_PyType);
     PyModule_AddObject(m, "usb_daq", (PyObject *)&usb_daq_PyType);
}
