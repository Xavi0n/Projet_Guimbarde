#define PY_SSIZE_T_CLEAN
#include "huskylens_api.h"
#include <Python.h>
#include <stdio.h>

// This function initializes Python, calls Python function, and fills the objects array.
// Returns the number of objects parsed, or -1 on error.
// max_objects: max number of objects to read (avoid overflow)
// objs: array of HuskylensObject to fill
int get_huskylens_objects(HuskylensObject *objs, int max_objects) {
    // Check for NULL pointer
    if (objs == NULL) {
        return -1;
    }

    PyObject *pName, *pModule, *pFunc;
    PyObject *pValue, *pDict;
    Py_ssize_t list_size, i;
    int count = 0;

    // Initialize Python interpreter
    Py_Initialize();

    // Add the directory containing the Python script to sys.path
    PyRun_SimpleString("import sys; sys.path.insert(0, '/home/debian/Projet_Guimbarde/py files')");

    // Import huskylens module
    pName = PyUnicode_DecodeFSDefault("HuskyLens_ReadAndParse");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (!pModule) {
        PyErr_Print();
        fprintf(stderr, "Failed to load huskylens module\n");
        Py_Finalize();
        return -1;
    }

    // Get the function get_parsed_huskylens_objects
    pFunc = PyObject_GetAttrString(pModule, "get_parsed_huskylens_objects");
    if (!pFunc || !PyCallable_Check(pFunc)) {
        if (PyErr_Occurred()) PyErr_Print();
        fprintf(stderr, "Cannot find function get_parsed_huskylens_objects\n");
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
        Py_Finalize();
        return -1;
    }

    // Call the function with no arguments
    pValue = PyObject_CallObject(pFunc, NULL);
    if (!pValue) {
        PyErr_Print();
        fprintf(stderr, "Call to get_parsed_huskylens_objects failed\n");
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

            objs[count].id = PyLong_AsLong(id_obj);
            objs[count].x = PyLong_AsLong(x_obj);
            objs[count].y = PyLong_AsLong(y_obj);
            objs[count].width = PyLong_AsLong(w_obj);
            objs[count].height = PyLong_AsLong(h_obj);

            count++;
        }
    }

    // Cleanup
    Py_DECREF(pValue);
    Py_XDECREF(pFunc);
    Py_DECREF(pModule);

    // Finalize Python interpreter
    Py_Finalize();

    return count;
}
