# Angles

## Features

This repo demonstrates how to take C++ templates into a Python module.
I have a C++ angle class for use in astronomy applications. I start
with constructors to create angles from degrees, minutes and seconds
(doubles or strings). To make full featured objects I add the
copy and assign constructors and overload the basic arithmetic
and boolean operators, e.g. +, +=, -, -=, >, <= et al.

I have a C++ template to build sets of limited range angle
objects like [declination](http://en.wikipedia.org/wiki/Declination)
and [right
ascension](http://en.wikipedia.org/wiki/Right_ascension). Objects
built from this template will raise an exception if their range is
exceed, either in the constructor or by a math operation like
addition.

I wrap these in Python by both [manually
extending](https://docs.python.org/2/extending/extending.html) angles
and using [Boost](http://www.boost.org) wrappers.
[SWIG](http://www.swig.org) is next.

Sets of unit tests verify the C++ library and Python modules work
as expected.

## Build

Each directory has its own Makefile with 'build', 'test', and 'clean'
targets.  libAngles must be built first. There is a build.sh script
that runs the Makefiles in all the directories in the necessary order
and takes these targets as command line arguments. There may be some
missing make dependencies between the directories, but it is always
safe to build clean then build test. The module is still small enough
that this doesn't take much time.

Each directory also has a suite of unit tests. libAngles uses
[gtest](https://code.google.com/p/googletest/). The Python
modules use Python native unittest.

To build the Boost wrappers you will, of course, need to install
[Boost](http://www.boost.org).

### OSX

I built this on my iMac using the g++ compiler that comes with
[Xcode](https://developer.apple.com/xcode/), but there is nothing special
that should cause a problem for other compilers.

### Linux

TODO

## Use

### C++

See [libAngles/example1.cpp](libAngles/example1.cpp).

```
// ============================================================
// Filename:    example1.cpp
//
// Description: Example of using libAngles
//
// Authors:     L.R. McFarland
// Created:     2014oct25
// ============================================================

#include <iostream>
#include <math.h>

#include <angles.h>

int main () {

  Angles::Angle a1(44, 59, 60);
  Angles::Angle a2("44", "59", "60");

  std::cout << "a1 = " << a1 << std::endl;
  std::cout << "a2 = " << a2 << std::endl;

  a1 += a2;

  std::cout << "sin(a1 + a2) = " << sin(a1.radians()) << std::endl;

  try {
    Angles::Latitude a3(200);
  } catch (Angles::RangeError err) {
    std::cout << "Error: " << err.what() << std::endl;
  }

  return 0;
}
```

This has its own make target "example1"

```
$ make example1
g++ -g -W -Wall -fPIC -I.   -c -o example1.o example1.cpp
g++ example1.o -o example1 -L. -lAngles

$ ./example1.sh
# ANGLES_ROOT not set. Using ../
a1 = 45* 0' 0"
a2 = 45* 0' 0"
sin(a1 + a2) = 1
Error: maximum exceeded
```

### Python

```
>>> import angles
>>> a = angles.Angle(45)
>>> b = a
>>> c = a + b
>>> c.value
90.0
>>> c.radians
1.5707963267948966
>>> 

```


## TODO

### Manual

- Angle specific exception handling

### Boost

- rich comparison operators
- deep copy *RuntimeError: Pickling of "angles.Angle" instances is not enabled (http://www.boost.org/libs/python/doc/v2/pickle.html*



