# Python wrappers

These are my Python wrapper examples and their unit tests. I have
found some interesting differences. For example it is not yet clear to
me how to make the rich comparison operators work in Boost like they
do manually or in [SWIG](swig.org) or wrap the exception handling
manually. This is still a work in progress and I am still
investigating how to make it happen.

### [Manual Extension](https://docs.python.org/2/extending/extending.html)

- **Makefile** creates the Python module and runs the test scripts.
- **gen_angles_module.py** removes the redundancy of creating wrappers for each template instantiation and creates angles.cpp with the python wrappers. This used by setup.py to create the angles module.
- **gen_test_angles.py** generates the unit test file test_angles.py
- **pylaunch.sh** sets up the Python environment and returns an command line interpreter.
- **setenv.sh** sets up the Python environment.
- **setup.py** builds the angles module.
- **test_angles.sh** sets up the Python environment and runs the unit tests.

The manual extension has several differenced from the Boost wrappers.
(This list is not definitive or complete. I am still working to resolve the differences.)

#### has

- rich comparison operators <, <=, ==, !=. >=, >
- a separate repr
- unitary minus
- angles.Error exceptions
- raises an exception when the value is set out of range for the limited range angles.

#### has not

- copy constructor
- copy assign
- properties, e.g. a_space.x() not a_space.x


#### Exceptions

This module has its own angles.Error exceptions. Boost uses
RuntimeError to wrap the C++ Exceptions.

#### Class vs. Template

There are two types of objects wrapped, the Angle class and
LimitedRangeAngle templates. Deep in the arithmetic operators, +, -,
*, /, I found an undocumented feature: The Angle class can construct
the result using the copy constructor, (e.g. + and -) or the copy
assign constructor (e.g. * and /), but the template versions can
not.

In the class version I can build the m_angle struct from the
class objects:

```
    result_angle->m_angle = ((Angle*)o1)->m_angle / ((Angle*)o2)->m_angle;
```

This causes range exceptions when I try it with the tempalte forms.
I work around the problemm by constructing from the values:

```
      Angles::LimitedRangeAngle the_quotient(((LimitedRangeAngle*)o1)->m_angle.value() /
					     ((LimitedRangeAngle*)o2)->m_angle.value());
```

I also found that the m_angle object's methods always return zero in the
python wrapper context:

```
static int LimitedRangeAngle_init(LimitedRangeAngle* self, PyObject* args, PyObject* kwds) {

  double degrees(0);
  double minutes(0);
  double seconds(0);

  static char* kwlist[] = {sDegreeStr, sMinuteStr, sSecondStr, NULL};

  if (! PyArg_ParseTupleAndKeywords(args, kwds, "|ddd", kwlist, &degrees, &minutes, &seconds))
    return -1;

  double a_value(Angles::degrees2seconds(degrees, minutes, seconds)/3600);

  // Angles::LimitedRangeAngle an_angle(a_value); // hi error works with this out

  std::cout << "not valid range " << self->m_angle.isValidRange(a_value)
   << " value " << a_value
   << " a value " << self->m_angle.value()
   << " max " << self->m_angle.maximum()
   << " min " << self->m_angle.minimum()
   << std::endl;

  if (self->m_angle.isValidRange(a_value) == true) {

    std::stringstream emsg;
    emsg << "not valid range " << a_value;

    PyErr_SetString(sAngleException, emsg.str().c_str());
    return -1;
  }

  self->m_angle.value(a_value);

  std::cout << "not valid range " << self->m_angle.isValidRange(a_value)
   << " value " << a_value
   << " a value " << self->m_angle.value()
   << " max " << self->m_angle.maximum()
   << " min " << self->m_angle.minimum()
   << std::endl;


  return 0;
}

```

produces

```
not valid range 0 value -129.282 a value 0 max 0 min 0
not valid range 0 value -129.282 a value -129.282 max 0 min 0
```

I am still working out why this is so.


### Boost

- **Makefile** creates the Python module and runs the test scripts.
- **gen_angles_module.py** removes the redundancy of creating wrappers for each template instantiation and creates angles.cpp with the python wrappers. This used by setup.py to create the angles module.
- **gen_test_angles.py** generates the unit test file test_angles.py
- **pylaunch.sh** sets up the Python environment and returns an command line interpreter.
- **setenv.sh** sets up the Python environment.
- **setup.py** builds the angles module.
- **test_angles.sh** sets up the Python environment and runs the unit tests.

The Boost wrappers have several differences from the manual extension.
(This list is not definitive or complete. I am still working to resolve the differences.)

#### has

- copy constructor
- copy assign
- properties, e.g. a_space.x() not a_space.x
- automatic exception handler for runtime errors

#### has not

- rich comparison operators <, <=, ==, !=. >=, >
- a separate repr (uses operator<<())
- unitary minus
- angles.Error exceptions (RuntimeErrors instead)


#### Exceptions

Unlike the current manual version, [Boost translates all C++ exceptions](http://www.boost.org/doc/libs/1_37_0/libs/python/doc/v2/exception_translator.html).

(As seen below, it also notes Declination and Latitude have the same
template. The manual version does not do this.)


```
>>> import angles
__main__:1: RuntimeWarning: to-Python converter for Angles::LRA<-90, 90> already registered; second conversion method ignored.
>>> a = angles.Longitude(360)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: maximum exceeded
>>>

>>> a = angles.Latitude(-33)
>>> b = angles.Latitude()

>>> a.value
-33.0
>>> b.value
0.0
>>> c = a / b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: division by zero is undefined
>>> ^D
```


### SWIG

TBD
