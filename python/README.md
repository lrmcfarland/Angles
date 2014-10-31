# Python wrappers

These are my Python wrapper examples and their unit tests. I have
found some interesting differences. For example it is not yet clear to
me how to make the rich comparison operators work in Boost like they
do manually or in [SWIG](swig.org) or wrap the exception handling
manually. This is still a work in progress and I am still
investigating how to make it happen.


## Manual Python Bindings

### has

- rich comparison operators <, <=, ==, !=. >=, >
- a separate repr
- unitary minus
- angles.Error exceptions
- raises an exception when the value is set out of range for the limited range angles.

### has not

- copy constructor
- copy assign
- properties, e.g. a_space.x() not a_space.x


## Boost

### has

- copy constructor
- copy assign
- properties, e.g. a_space.x() not a_space.x
- automatic exception handler for runtime errors

### has not

- rich comparison operators <, <=, ==, !=. >=, >
- a separate repr (uses operator<<())
- unitary minus
- angles.Error exceptions (RuntimeErrors instead)




## SWIG

TBD
