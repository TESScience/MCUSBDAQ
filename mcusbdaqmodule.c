#include <Python.h>
#include "find_usb_daqs.h"

static PyObject*
say_hello(PyObject* self, PyObject* args)
{
    const char* name;

    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;

    printf("Hello %s!\n", name);

    Py_RETURN_NONE;
}

static PyMethodDef MCUSBDAQMethods[] =
{
     {"say_hello", say_hello, METH_VARARGS, "Greet somebody."},
     {"find_usb_daqs", find_usb_daqs, METH_VARARGS, "Find the USB Measurement Computing data acquisition cards present."},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initmcusbdaq(void)
{
     (void) Py_InitModule("mcusbdaq", MCUSBDAQMethods);
}
