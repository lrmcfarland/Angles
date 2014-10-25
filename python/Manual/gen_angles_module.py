#!/usr/bin/env python

"""Generates angles.cpp for python wrappers.

This file contanis the templates for generating angles.cpp for the
different types of angles defined in libAngles.

There are two types of objects wrapped, the Angle class and
LimitedRangeAngle templates. Deep in the arithmetic operators, +, -,
*, /, I found an undocumented feature: The Angle class can construct
the result using the copy constructor, (e.g. + and -) or the copy
assign constructor (e.g. * and /), but the template versions can
not. (It was just whimsy that drove my choice of these construction
techniques for these operators.) This produces out of range errors,
probably from using the addresses and not the values of the
objects. This is not the case for the Boost version. The copy
constructor test also fails. I have not yet figured out why this is
so, but the work around is to use the values. For example where
Angle::operator+() wraps:

  Angles::%(TypeName)s the_sum(((%(TypeName)s*)o1)->m_angle + ((%(TypeName)s*)o2)->m_angle);

and builds the new angle from the copy constructor, the
LimitedRangeAngle template uses the value constructor:

  Angles::%(TypeName)s the_sum(((%(TypeName)s*)o1)->m_angle.value() + ((%(TypeName)s*)o2)->m_angle.value());

The template also has maximum and minimums and RangeError behaviors
so this is not the only difference and two templates are still needed.

TODO: I still need to handle Angles::Error exceptions.

"""



module_header = """// THIS IS A GENERATED FILE. EDITS WILL BE OVERWRITTEN.

// ==========================================================
// Filename:    angles.cpp
//
// Description: Contains the python wrappers for Angles objects.
//              This file is generated automatically.
//
// See also:    http://docs.python.org/extending/newtypes.html
//              http://docs.python.org/c-api/complex.html
//              https://docs.python.org/2/reference/datamodel.html
//
// Author:      L.R. McFarland
// Created:     2014 Oct 08
// ==========================================================

#include <Python.h> // must be first
#include <structmember.h> // part of python

#include <sstream>

#include <angles.h>

// ===================
// ===== statics =====
// ===================

static PyObject* sAngleException; // exception holder

// char* kwlist[] init strings
static char sDegreeStr[] = "degees";
static char sMinuteStr[] = "minutes";
static char sSecondStr[] = "seconds";
static char sMinimumStr[] = "minimum";
static char sMaximumStr[] = "maximum";

static char sValueStr[] = "value";
static char sRadiansStr[] = "radians";


// TODO: make precision configuralble on build, not hardcoded.
static const unsigned int sPrintPrecision(12); // matches defaut %s precision for unit test


""" # end header




angle_class_template = """

// -----------------
// ----- %(TypeName)s -----
// -----------------

// ------------------------
// ----- constructors -----
// ------------------------


// %(TypeName)s object definition.
typedef struct {
  PyObject_HEAD
  Angles::%(TypeName)s m_angle;
} %(TypeName)s;


// Forward declarations for as_number methods. Wraps Type definition.
static void new_%(TypeName)sType(%(TypeName)s** an_angle);
static int is_%(TypeName)sType(PyObject* an_angle);


static PyObject* %(TypeName)s_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  %(TypeName)s* self(NULL);
  self = (%(TypeName)s*)type->tp_alloc(type, 0);
  return (PyObject*)self;
}


static int %(TypeName)s_init(%(TypeName)s* self, PyObject* args, PyObject* kwds) {

  double degrees(0);
  double minutes(0);
  double seconds(0);

  static char* kwlist[] = {sDegreeStr, sMinuteStr, sSecondStr, NULL};

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|ddd", kwlist, &degrees, &minutes, &seconds))
    return -1;

  // value initialized to 0 by new.
  self->m_angle.value(Angles::degrees2seconds(degrees, minutes, seconds)/3600);

  return 0;
}


static void %(TypeName)s_dealloc(%(TypeName)s* self) {
  self->ob_type->tp_free((PyObject*)self);
}


// -----------------
// ----- print -----
// -----------------

PyObject* %(TypeName)s_str(PyObject* self) {
  std::stringstream result;
  result.precision(sPrintPrecision);
  result << ((%(TypeName)s*)self)->m_angle;
  return PyString_FromString(result.str().c_str());
}

// TODO a different repr? for constructor?
PyObject* %(TypeName)s_repr(PyObject* self) {
  std::stringstream result;
  result.precision(sPrintPrecision);
  result << ((%(TypeName)s*)self)->m_angle;
  return PyString_FromString(result.str().c_str());
}


// -------------------------------
// ----- getters and setters -----
// -------------------------------

// ----- value -----

static PyObject* %(TypeName)s_getValue(%(TypeName)s* self, void* closure) {
  return PyFloat_FromDouble(self->m_angle.value());
}

static int %(TypeName)s_setValue(%(TypeName)s* self, PyObject* value, void* closure) {

  if (value == NULL) {
    PyErr_SetString(sAngleException, "Cannot delete value");
    return 0;
  }

  if (!PyFloat_Check(value) && !PyInt_Check(value)) {
    PyErr_SetString(sAngleException, "value must be a float");
    return 0;
  }

  self->m_angle.value(PyFloat_AsDouble(value));

  return 0;
}

// ----- radians -----

static PyObject* %(TypeName)s_getRadians(%(TypeName)s* self, void* closure) {
  return PyFloat_FromDouble(self->m_angle.radians());
}

static int %(TypeName)s_setRadians(%(TypeName)s* self, PyObject* radians, void* closure) {

  if (radians == NULL) {
    PyErr_SetString(sAngleException, "Cannot delete radians");
    return 0;
  }

  if (!PyFloat_Check(radians) && !PyInt_Check(radians)) {
    PyErr_SetString(sAngleException, "radians must be a float");
    return 0;
  }

  self->m_angle.radians(PyFloat_AsDouble(radians));

  return 0;
}

// --------------------------
// ----- number methods -----
// --------------------------


static PyObject* %(TypeName)s_nb_add(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);

  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "add failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_sum(((%(TypeName)s*)o1)->m_angle + ((%(TypeName)s*)o2)->m_angle);

  // copy because m_angle constructor has already run.
  result_angle->m_angle = the_sum;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_subtract(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);

  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "subtract failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_difference(((%(TypeName)s*)o1)->m_angle - ((%(TypeName)s*)o2)->m_angle);

  // copy because m_angle constructor has already run.
  result_angle->m_angle = the_difference;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_negative(PyObject* o1) {
  // Unitary minus

  if (!is_%(TypeName)sType(o1)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);

  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "negative failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_inverse = -((%(TypeName)s*)o1)->m_angle;

  // copy because m_angle constructor has already run.
  result_angle->m_angle = the_inverse;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_multiply(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);
  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "multiply failed to create angle");
    return NULL;
  }

  result_angle->m_angle = ((%(TypeName)s*)o1)->m_angle * ((%(TypeName)s*)o2)->m_angle;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_divide(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);
  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "multiply failed to create angle");
    return NULL;
  }

  result_angle->m_angle = ((%(TypeName)s*)o1)->m_angle / ((%(TypeName)s*)o2)->m_angle;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_tp_richcompare(PyObject* o1, PyObject* o2, int op) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }


  // TODO >, >=, <, <=

  if (op == Py_LT) {

    if (((%(TypeName)s*)o1)->m_angle < ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_LE) {

    if (((%(TypeName)s*)o1)->m_angle <= ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_EQ) {

    if (((%(TypeName)s*)o1)->m_angle == ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_NE) {

    if (((%(TypeName)s*)o1)->m_angle != ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_GT) {

    if (((%(TypeName)s*)o1)->m_angle > ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_GE) {

    if (((%(TypeName)s*)o1)->m_angle >= ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else {

    PyErr_SetString(PyExc_TypeError, "richcompare op not supported");
    return NULL;

  }

}

// ---------------------------
// ----- inplace methods -----
// ---------------------------

static PyObject* %(TypeName)s_nb_inplace_add(PyObject* o1, PyObject* o2) {
  // TODO can this be implement directly using space::operator+=()?
  // problem with refence going out of scope, segfault.
  return %(TypeName)s_nb_add(o1, o2);
}

static PyObject* %(TypeName)s_nb_inplace_subtract(PyObject* o1, PyObject* o2) {
  // TOOD implement directly?
  return %(TypeName)s_nb_subtract(o1, o2);
}

static PyObject* %(TypeName)s_nb_inplace_multiply(PyObject* o1, PyObject* o2) {
  // TOOD implement directly?
  return %(TypeName)s_nb_multiply(o1, o2);
}

static PyObject* %(TypeName)s_nb_inplace_divide(PyObject* o1, PyObject* o2) {
  // TOOD implement directly?
  return %(TypeName)s_nb_divide(o1, o2);
}

// --------------------------
// ----- Python structs -----
// --------------------------

static PyMethodDef %(TypeName)s_methods[] = {
    {NULL}  /* Sentinel */
};


static PyMemberDef %(TypeName)s_members[] = {
    {NULL}  /* Sentinel */
};

static PyGetSetDef %(TypeName)s_getseters[] = {
    {sValueStr, (getter)%(TypeName)s_getValue, (setter)%(TypeName)s_setValue, sValueStr, NULL},
    {sRadiansStr, (getter)%(TypeName)s_getRadians, (setter)%(TypeName)s_setRadians, sRadiansStr, NULL},
    {NULL}  /* Sentinel */
};


// see http://docs.python.org/c-api/typeobj.html
static PyNumberMethods %(TypeName)s_as_number = {
  (binaryfunc) %(TypeName)s_nb_add,
  (binaryfunc) %(TypeName)s_nb_subtract,
  (binaryfunc) %(TypeName)s_nb_multiply,
  (binaryfunc) %(TypeName)s_nb_divide,
  (binaryfunc) 0,  // nb_remainder
  (binaryfunc) 0,  // nb_divmod
  (ternaryfunc) 0, // nb_power
  (unaryfunc) %(TypeName)s_nb_negative,
  (unaryfunc) 0,   // nb_positive
  (unaryfunc) 0,   // nb_absolute
  (inquiry) 0,     // nb_nonzero. Used by PyObject_IsTrue.
  (unaryfunc) 0,   // nb_invert
  (binaryfunc) 0,  // nb_lshift
  (binaryfunc) 0,  // nb_rshift
  (binaryfunc) 0,  // nb_and
  (binaryfunc) 0,  // nb_xor
  (binaryfunc) 0,  // nb_or
  (coercion) 0,    // Used by the coerce() function
  (unaryfunc) 0,   // nb_int
  (unaryfunc) 0,   // nb_long
  (unaryfunc) 0,   // nb_float
  (unaryfunc) 0,   // nb_oct
  (unaryfunc) 0,   // nb_hex

  // added in release 2.0

  (binaryfunc) %(TypeName)s_nb_inplace_add,
  (binaryfunc) %(TypeName)s_nb_inplace_subtract,
  (binaryfunc) %(TypeName)s_nb_inplace_multiply,
  (binaryfunc) %(TypeName)s_nb_inplace_divide,
  (binaryfunc) 0,  // nb_inplace_remainder
  (ternaryfunc) 0, // nb_inplace_power
  (binaryfunc) 0,  // nb_inplace_lshift
  (binaryfunc) 0,  // nb_inplace_rshift
  (binaryfunc) 0,  // nb_inplace_and
  (binaryfunc) 0,  // nb_inplace_xor
  (binaryfunc) 0,  // nb_inplace_or

  // added in release 2.2
  (binaryfunc) 0,  // nb_floor_divide
  (binaryfunc) 0,  // nb_true_divide
  (binaryfunc) 0,  // nb_inplace_floor_divide
  (binaryfunc) 0,  // nb_inplace_true_divide

};


PyTypeObject %(TypeName)sType = {
  PyObject_HEAD_INIT(NULL)
  0,                                        /* ob_size */
  "angle",                                  /* tp_name */
  sizeof(%(TypeName)s),                     /* tp_basicsize */
  0,                                        /* tp_itemsize */
  (destructor) %(TypeName)s_dealloc,        /* tp_dealloc */
  0,                                        /* tp_print */
  0,                                        /* tp_getattr */
  0,                                        /* tp_setattr */
  0,                                        /* tp_compare */
  %(TypeName)s_repr,                        /* tp_repr */
  &%(TypeName)s_as_number,                  /* tp_as_number */
  0,                                        /* tp_as_sequence */
  0,                                        /* tp_as_mapping */
  0,                                        /* tp_hash */
  0,                                        /* tp_call */
  %(TypeName)s_str,                         /* tp_str */
  0,                                        /* tp_getattro */
  0,                                        /* tp_setattro */
  0,                                        /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_CHECKTYPES, /* tp_flags */
  "%(TypeName)s objects",                   /* tp_doc */
  0,                                        /* tp_traverse */
  0,                                        /* tp_clear */
  %(TypeName)s_tp_richcompare,              /* tp_richcompare */
  0,                                        /* tp_weaklistoffset */
  0,                                        /* tp_iter */
  0,                                        /* tp_iternext */
  %(TypeName)s_methods,                     /* tp_methods */
  %(TypeName)s_members,                     /* tp_members */
  %(TypeName)s_getseters,                   /* tp_getset */
  0,                                        /* tp_base */
  0,                                        /* tp_dict */
  0,                                        /* tp_descr_get */
  0,                                        /* tp_descr_set */
  0,                                        /* tp_dictoffset */
  (initproc)%(TypeName)s_init,              /* tp_init */
  0,                                        /* tp_alloc */
  %(TypeName)s_new,                         /* tp_new */
};


// Create new objects with PyObject_New() for binary operators that
// return a new instance of %(TypeName)s, like add.
static void new_%(TypeName)sType(%(TypeName)s** an_angle) {
  *an_angle = PyObject_New(%(TypeName)s, &%(TypeName)sType);
}

static int is_%(TypeName)sType(PyObject* an_angle) {
  //wrapper for type check
  return PyObject_TypeCheck(an_angle, &%(TypeName)sType);
}

""" # end angle_class_template









# -----------------------------------
# ----- angle template template -----
# -----------------------------------

# adds minimum/maximum range features


angle_template_template = """

// -----------------
// ----- %(TypeName)s -----
// -----------------

// ------------------------
// ----- constructors -----
// ------------------------


// %(TypeName)s object definition.
typedef struct {
  PyObject_HEAD
  Angles::%(TypeName)s m_angle;
} %(TypeName)s;


// Forward declarations for as_number methods. Wraps Type definition.
static void new_%(TypeName)sType(%(TypeName)s** an_angle);
static int is_%(TypeName)sType(PyObject* an_angle);


static PyObject* %(TypeName)s_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  %(TypeName)s* self(NULL);
  self = (%(TypeName)s*)type->tp_alloc(type, 0);
  return (PyObject*)self;
}


static int %(TypeName)s_init(%(TypeName)s* self, PyObject* args, PyObject* kwds) {

  double degrees(0);
  double minutes(0);
  double seconds(0);

  static char* kwlist[] = {sDegreeStr, sMinuteStr, sSecondStr, NULL};

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|ddd", kwlist, &degrees, &minutes, &seconds))
    return -1;



  // TODO check minimum/maximum this bypasses constructor!!!

  // use constructor to raise exception if not valie
  Angles::%(TypeName)s the_difference(Angles::degrees2seconds(degrees, minutes, seconds)/3600);

  // TODO use validate instead? raise exception if not valid?

  // value initialized to 0 by new.
  self->m_angle.value(Angles::degrees2seconds(degrees, minutes, seconds)/3600);

  return 0;
}


static void %(TypeName)s_dealloc(%(TypeName)s* self) {
  self->ob_type->tp_free((PyObject*)self);
}


// -----------------
// ----- print -----
// -----------------

PyObject* %(TypeName)s_str(PyObject* self) {
  std::stringstream result;
  result.precision(sPrintPrecision);
  result << ((%(TypeName)s*)self)->m_angle;
  return PyString_FromString(result.str().c_str());
}

// TODO a different repr? for constructor?
PyObject* %(TypeName)s_repr(PyObject* self) {
  std::stringstream result;
  result.precision(sPrintPrecision);
  result << ((%(TypeName)s*)self)->m_angle;
  return PyString_FromString(result.str().c_str());
}


// -------------------------------
// ----- getters and setters -----
// -------------------------------

// ----- value -----

static PyObject* %(TypeName)s_getValue(%(TypeName)s* self, void* closure) {
  return PyFloat_FromDouble(self->m_angle.value());
}

static int %(TypeName)s_setValue(%(TypeName)s* self, PyObject* value, void* closure) {

  if (value == NULL) {
    PyErr_SetString(sAngleException, "Cannot delete value");
    return 0;
  }

  if (!PyFloat_Check(value) && !PyInt_Check(value)) {
    PyErr_SetString(sAngleException, "value must be a float");
    return 0;
  }

  self->m_angle.value(PyFloat_AsDouble(value));

  return 0;
}

// ----- radians -----

static PyObject* %(TypeName)s_getRadians(%(TypeName)s* self, void* closure) {
  return PyFloat_FromDouble(self->m_angle.radians());
}

static int %(TypeName)s_setRadians(%(TypeName)s* self, PyObject* radians, void* closure) {

  if (radians == NULL) {
    PyErr_SetString(sAngleException, "Cannot delete radians");
    return 0;
  }

  if (!PyFloat_Check(radians) && !PyInt_Check(radians)) {
    PyErr_SetString(sAngleException, "radians must be a float");
    return 0;
  }

  self->m_angle.radians(PyFloat_AsDouble(radians));

  return 0;
}

// ----- minimum -----

static PyObject* %(TypeName)s_getMinimum(%(TypeName)s* self, void* closure) {
  return PyFloat_FromDouble(self->m_angle.minimum());
}

// ----- maximum -----

static PyObject* %(TypeName)s_getMaximum(%(TypeName)s* self, void* closure) {
  return PyFloat_FromDouble(self->m_angle.maximum());
}

// --------------------------
// ----- number methods -----
// --------------------------


static PyObject* %(TypeName)s_nb_add(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);

  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "add failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_sum(((%(TypeName)s*)o1)->m_angle.value() + ((%(TypeName)s*)o2)->m_angle.value());

  // copy because m_angle constructor has already run.
  result_angle->m_angle = the_sum;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_subtract(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);

  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "subtract failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_difference(((%(TypeName)s*)o1)->m_angle.value() - ((%(TypeName)s*)o2)->m_angle.value());

  // copy because m_angle constructor has already run.
  result_angle->m_angle = the_difference;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_negative(PyObject* o1) {
  // Unitary minus

  if (!is_%(TypeName)sType(o1)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);

  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "negative failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_inverse(-((%(TypeName)s*)o1)->m_angle.value());

  // copy because m_angle constructor has already run.
  result_angle->m_angle = the_inverse;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_multiply(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);
  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "multiply failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_product(((%(TypeName)s*)o1)->m_angle.value() * ((%(TypeName)s*)o2)->m_angle.value());

  result_angle->m_angle = the_product;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_nb_divide(PyObject* o1, PyObject* o2) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }

  %(TypeName)s* result_angle(NULL);
  new_%(TypeName)sType(&result_angle);

  if (result_angle == NULL) {
    PyErr_SetString(sAngleException, "multiply failed to create angle");
    return NULL;
  }

  Angles::%(TypeName)s the_quotient(((%(TypeName)s*)o1)->m_angle.value() / ((%(TypeName)s*)o2)->m_angle.value());

  result_angle->m_angle = the_quotient;

  return (PyObject*) result_angle;
}


static PyObject* %(TypeName)s_tp_richcompare(PyObject* o1, PyObject* o2, int op) {

  if (!is_%(TypeName)sType(o1) || !is_%(TypeName)sType(o2)) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
  }


  // TODO >, >=, <, <=

  if (op == Py_LT) {

    if (((%(TypeName)s*)o1)->m_angle < ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_LE) {

    if (((%(TypeName)s*)o1)->m_angle <= ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_EQ) {

    if (((%(TypeName)s*)o1)->m_angle == ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_NE) {

    if (((%(TypeName)s*)o1)->m_angle != ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_GT) {

    if (((%(TypeName)s*)o1)->m_angle > ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else if (op == Py_GE) {

    if (((%(TypeName)s*)o1)->m_angle >= ((%(TypeName)s*)o2)->m_angle)
      return Py_True;
    else
      return Py_False;

  } else {

    PyErr_SetString(PyExc_TypeError, "richcompare op not supported");
    return NULL;

  }

}

// ---------------------------
// ----- inplace methods -----
// ---------------------------

static PyObject* %(TypeName)s_nb_inplace_add(PyObject* o1, PyObject* o2) {
  // TODO can this be implement directly using space::operator+=()?
  // problem with refence going out of scope, segfault.
  return %(TypeName)s_nb_add(o1, o2);
}

static PyObject* %(TypeName)s_nb_inplace_subtract(PyObject* o1, PyObject* o2) {
  // TOOD implement directly?
  return %(TypeName)s_nb_subtract(o1, o2);
}

static PyObject* %(TypeName)s_nb_inplace_multiply(PyObject* o1, PyObject* o2) {
  // TOOD implement directly?
  return %(TypeName)s_nb_multiply(o1, o2);
}

static PyObject* %(TypeName)s_nb_inplace_divide(PyObject* o1, PyObject* o2) {
  // TOOD implement directly?
  return %(TypeName)s_nb_divide(o1, o2);
}

// --------------------------
// ----- Python structs -----
// --------------------------

static PyMethodDef %(TypeName)s_methods[] = {
    {sMinimumStr, (PyCFunction)%(TypeName)s_getMinimum, METH_NOARGS, NULL},
    {sMaximumStr, (PyCFunction)%(TypeName)s_getMaximum, METH_NOARGS, NULL},
    {NULL}  /* Sentinel */
};


static PyMemberDef %(TypeName)s_members[] = {
    {NULL}  /* Sentinel */
};

static PyGetSetDef %(TypeName)s_getseters[] = {
    {sValueStr, (getter)%(TypeName)s_getValue, (setter)%(TypeName)s_setValue, sValueStr, NULL},
    {sRadiansStr, (getter)%(TypeName)s_getRadians, (setter)%(TypeName)s_setRadians, sRadiansStr, NULL},
    {NULL}  /* Sentinel */
};


// see http://docs.python.org/c-api/typeobj.html
static PyNumberMethods %(TypeName)s_as_number = {
  (binaryfunc) %(TypeName)s_nb_add,
  (binaryfunc) %(TypeName)s_nb_subtract,
  (binaryfunc) %(TypeName)s_nb_multiply,
  (binaryfunc) %(TypeName)s_nb_divide,
  (binaryfunc) 0,  // nb_remainder
  (binaryfunc) 0,  // nb_divmod
  (ternaryfunc) 0, // nb_power
  (unaryfunc) %(TypeName)s_nb_negative,
  (unaryfunc) 0,   // nb_positive
  (unaryfunc) 0,   // nb_absolute
  (inquiry) 0,     // nb_nonzero. Used by PyObject_IsTrue.
  (unaryfunc) 0,   // nb_invert
  (binaryfunc) 0,  // nb_lshift
  (binaryfunc) 0,  // nb_rshift
  (binaryfunc) 0,  // nb_and
  (binaryfunc) 0,  // nb_xor
  (binaryfunc) 0,  // nb_or
  (coercion) 0,    // Used by the coerce() function
  (unaryfunc) 0,   // nb_int
  (unaryfunc) 0,   // nb_long
  (unaryfunc) 0,   // nb_float
  (unaryfunc) 0,   // nb_oct
  (unaryfunc) 0,   // nb_hex

  // added in release 2.0

  (binaryfunc) %(TypeName)s_nb_inplace_add,
  (binaryfunc) %(TypeName)s_nb_inplace_subtract,
  (binaryfunc) %(TypeName)s_nb_inplace_multiply,
  (binaryfunc) %(TypeName)s_nb_inplace_divide,
  (binaryfunc) 0,  // nb_inplace_remainder
  (ternaryfunc) 0, // nb_inplace_power
  (binaryfunc) 0,  // nb_inplace_lshift
  (binaryfunc) 0,  // nb_inplace_rshift
  (binaryfunc) 0,  // nb_inplace_and
  (binaryfunc) 0,  // nb_inplace_xor
  (binaryfunc) 0,  // nb_inplace_or

  // added in release 2.2
  (binaryfunc) 0,  // nb_floor_divide
  (binaryfunc) 0,  // nb_true_divide
  (binaryfunc) 0,  // nb_inplace_floor_divide
  (binaryfunc) 0,  // nb_inplace_true_divide

};


PyTypeObject %(TypeName)sType = {
  PyObject_HEAD_INIT(NULL)
  0,                                        /* ob_size */
  "angle",                                  /* tp_name */
  sizeof(%(TypeName)s),                     /* tp_basicsize */
  0,                                        /* tp_itemsize */
  (destructor) %(TypeName)s_dealloc,        /* tp_dealloc */
  0,                                        /* tp_print */
  0,                                        /* tp_getattr */
  0,                                        /* tp_setattr */
  0,                                        /* tp_compare */
  %(TypeName)s_repr,                        /* tp_repr */
  &%(TypeName)s_as_number,                  /* tp_as_number */
  0,                                        /* tp_as_sequence */
  0,                                        /* tp_as_mapping */
  0,                                        /* tp_hash */
  0,                                        /* tp_call */
  %(TypeName)s_str,                         /* tp_str */
  0,                                        /* tp_getattro */
  0,                                        /* tp_setattro */
  0,                                        /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_CHECKTYPES, /* tp_flags */
  "%(TypeName)s objects",                   /* tp_doc */
  0,                                        /* tp_traverse */
  0,                                        /* tp_clear */
  %(TypeName)s_tp_richcompare,              /* tp_richcompare */
  0,                                        /* tp_weaklistoffset */
  0,                                        /* tp_iter */
  0,                                        /* tp_iternext */
  %(TypeName)s_methods,                     /* tp_methods */
  %(TypeName)s_members,                     /* tp_members */
  %(TypeName)s_getseters,                   /* tp_getset */
  0,                                        /* tp_base */
  0,                                        /* tp_dict */
  0,                                        /* tp_descr_get */
  0,                                        /* tp_descr_set */
  0,                                        /* tp_dictoffset */
  (initproc)%(TypeName)s_init,              /* tp_init */
  0,                                        /* tp_alloc */
  %(TypeName)s_new,                         /* tp_new */
};


// Create new objects with PyObject_New() for binary operators that
// return a new instance of %(TypeName)s, like add.
static void new_%(TypeName)sType(%(TypeName)s** an_angle) {
  *an_angle = PyObject_New(%(TypeName)s, &%(TypeName)sType);
}

static int is_%(TypeName)sType(PyObject* an_angle) {
  //wrapper for type check
  return PyObject_TypeCheck(an_angle, &%(TypeName)sType);
}

""" # end angle_class_template















module_init = """
// --------------------------
// ----- module methods -----
// --------------------------

// -------------------
// ----- deg2rad -----
// -------------------

PyDoc_STRVAR(angles_deg2rad__doc__, "converts degrees into radians");

static PyObject* deg2rad(PyObject* self, PyObject *args) {
  double radians(0);
  if (!PyArg_ParseTuple(args, "d", &radians))
    return NULL;
  double degrees = Angles::Angle::deg2rad(radians);
  return (PyObject*)  Py_BuildValue("d", degrees);
}


// -------------------
// ----- rad2deg -----
// -------------------

PyDoc_STRVAR(angles_rad2deg__doc__, "converts radians into degrees");

static PyObject* rad2deg(PyObject* self, PyObject *args) {
  double radians(0);
  if (!PyArg_ParseTuple(args, "d", &radians))
    return NULL;
  double degrees = Angles::Angle::rad2deg(radians);
  return (PyObject*)  Py_BuildValue("d", degrees);
}


// -----------------------
// ----- method list -----
// -----------------------

PyMethodDef angles_module_methods[] = {
  {"deg2rad", (PyCFunction) deg2rad, METH_VARARGS, angles_deg2rad__doc__},
  {"rad2deg", (PyCFunction) rad2deg, METH_VARARGS, angles_rad2deg__doc__},
  {NULL, NULL}  /* Sentinel */
};


// ------------------------------
// ----- init angles module -----
// ------------------------------

// PyMODINIT_FUNC declares extern "C" too.
PyMODINIT_FUNC initangles(void) {

  PyObject* m(Py_InitModule3("angles", angles_module_methods, "python wrappers for angle objects."));

  // error
  char eMsgStr[] = "angles.error";
  sAngleException = PyErr_NewException(eMsgStr, NULL, NULL);
  Py_INCREF(sAngleException);
  PyModule_AddObject(m, "Error", sAngleException);

"""

module_type_init = """

  %(TypeName)sType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&%(TypeName)sType) < 0)
    return;
  Py_INCREF(&%(TypeName)sType);
  PyModule_AddObject(m, "%(TypeName)s", (PyObject *)&%(TypeName)sType);

"""

# ================
# ===== main =====
# ================

if __name__ == '__main__':

    angle_classes = list()
    angle_classes.append({'TypeName': 'Angle'})

    angle_templates = list()
    angle_templates.append({'TypeName': 'LimitedRangeAngle'})
    angle_templates.append({'TypeName': 'Declination'})
    angle_templates.append({'TypeName': 'Latitude'})
    angle_templates.append({'TypeName': 'Longitude'})
    angle_templates.append({'TypeName': 'RA'})

    flnm = 'angles.cpp'
    afp = open(flnm, 'w')

    afp.write(module_header)


    for angle_class in angle_classes:
        afp.write(angle_class_template % angle_class)

    for angle_template in angle_templates:
        afp.write(angle_template_template % angle_template)


    afp.write(module_init)

    for angle_class in angle_classes:
        afp.write(module_type_init % angle_class)

    for angle_template in angle_templates:
        afp.write(module_type_init % angle_template)

    afp.write('\n}\n') # final brace


    afp.close()



