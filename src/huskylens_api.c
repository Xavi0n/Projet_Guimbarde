#define PY_SSIZE_T_CLEAN
#include "huskylens_api.h"
#include <Python.h>
#include <stdio.h>

// Assumes huskylib.py has a function get_objects() returning list of dicts with keys:
// "id", "x", "y", "width", "height"

int get_huskylens_objects(HuskylensObject *objs, int max_objects) {
    if (objs == NULL) {
        return -1;
    }

    PyObject *pName = NULL, *pModule = NULL, *pFunc = NULL;
    PyObject *pValue = NULL, *pDict = NULL;
    Py_ssize_t list_size, i;
    int count = 0;

    Py_Initialize();

    // Add your Python script directory to sys.path
    PyRun_SimpleString("import sys; sys.path.insert(0, '/home/debian/Projet_Guimbarde/py files')");

    // Import huskylib module
    pName = PyUnicode_DecodeFSDefault("huskylib");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (!pModule) {
        PyErr_Print();
        fprintf(stderr, "Failed to load huskylib module\n");
        Py_Finalize();
        return -1;
    }

    // Get the function get_objects
    pFunc = PyObject_GetAttrString(pModule, "get_objects");
    if (!pFunc || !PyCallable_Check(pFunc)) {
        if (PyErr_Occurred()) PyErr_Print();
        fprintf(stderr, "Cannot find function get_objects\n");
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
        Py_Finalize();
        return -1;
    }

    // Call get_objects() with no arguments
    pValue = PyObject_CallObject(pFunc, NULL);
    if (!pValue) {
        PyErr_Print();
        fprintf(stderr, "Call to get_objects failed\n");
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
        Py_Finalize();
        return -1;
    }

    if (!PyList_Check(pValue)) {
        fprintf(stderr, "Return value is not a list\n");
        Py_DECREF(pValue);
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
        Py_Finalize();
        return -1;
    }

    list_size = PyList_Size(pValue);
    for (i = 0; i < list_size && count < max_objects; i++) {
        pDict = PyList_GetItem(pValue, i);  // Borrowed reference
        if (PyDict_Check(pDict)) {
            PyObject *id_obj = PyDict_GetItemString(pDict, "id");
            PyObject *x_obj = PyDict_GetItemString(pDict, "x");
            PyObject *y_obj = PyDict_GetItemString(pDict, "y");
            PyObject *w_obj = PyDict_GetItemString(pDict, "width");
            PyObject *h_obj = PyDict_GetItemString(pDict, "height");

            objs[count].id = (int)PyLong_AsLong(id_obj);
            objs[count].x = (int)PyLong_AsLong(x_obj);
            objs[count].y = (int)PyLong_AsLong(y_obj);
            objs[count].width = (int)PyLong_AsLong(w_obj);
            objs[count].height = (int)PyLong_AsLong(h_obj);

            count++;
        }
    }

    Py_DECREF(pValue);
    Py_XDECREF(pFunc);
    Py_DECREF(pModule);

    Py_Finalize();

    return count;
}
