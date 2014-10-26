# Python wrappers

These are my Python wrapper examples and their unit tests. I have
found some interesting differences. For example it is not yet clear to
me how to make the rich comparison operators work in Boost like they
do manually or in [SWIG](swig.org) or wrap the exception handling
manually. This is still a work in progress and I am still
investigating how to make it happen. Any advice or hints would be
welcome.

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

#### has not

- copy constructor
- copy assign
- properties, e.g. a_space.x() not a_space.x
- automatic exception handler for runtime errors

#### Exceptions

TODO the C++ exceptions are not caught by the python interpreter and
will "blow the stack" when encountered.

#### Class vs. Template

There are two types of objects wrapped, the Angle class and
LimitedRangeAngle templates. Deep in the arithmetic operators, +, -,
*, /, I found an undocumented feature: The Angle class can construct
the result using the copy constructor, (e.g. + and -) or the copy
assign constructor (e.g. * and /), but the template versions can
not. (It was just whimsy that drove my choice of these construction
techniques for these operators and lead to this finding.) This
produces out of range errors, probably from using the addresses and
not the values of the objects. This is not the case for the Boost
version. The copy constructor test also fails. I have not yet figured
out why this is so, but the work around is to use the values. For
example where Angle::operator+() wraps:

```
  Angles::%(TypeName)s the_sum(((%(TypeName)s*)o1)->m_angle + ((%(TypeName)s*)o2)->m_angle);
```

and builds the new angle from the copy constructor, the
LimitedRangeAngle template uses the value constructor:

```
  Angles::%(TypeName)s the_sum(((%(TypeName)s*)o1)->m_angle.value() + ((%(TypeName)s*)o2)->m_angle.value());
```

The template also has maximum and minimums and RangeError behaviors
so this is not the only difference and two templates are still needed.


### Boost

- **Makefile** creates the Python module and runs the test scripts.
- **gen_angles_module.py** removes the redundancy of creating wrappers for each template instantiation and creates angles.cpp with the python wrappers. This used by setup.py to create the angles module.
- **gen_test_angles.py** generates the unit test file test_angles.py
- **pylaunch.sh** sets up the Python environment and returns an command line interpreter.
- **setenv.sh** sets up the Python environment.
- **setup.py** builds the angles module.
- **test_angles.sh** sets up the Python environment and runs the unit tests.

The Boost wrappers has several differenced from the manual extension.
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


#### Exceptions

Boost automagiclly wraps the C++ exceptions and does not "blow the
stack".  (As see below, it does note Declination and Latitude have the same
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
