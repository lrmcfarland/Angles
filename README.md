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
[SWIG](http://www.swig.org) and [Cython](http://cython.org) are next.

Sets of unit tests verify the C++ library and Python modules work
as expected.

## Build

Each directory has its own Makefile with 'build', 'test', and 'clean'
targets, e.g.

```
$ pwd
/Users/.../Angles/libAngles
$ make clean
$ make test
```

libAngles must be built first. There is a build.sh script that runs
the Makefiles in all the directories in the necessary order and takes
these targets as command line arguments.

```
$ pwd
/Users/.../Angles/
$ ./build.sh clean
$ ./build.sh test
```

Each directory also has a suite of unit tests. libAngles uses
[gtest](https://code.google.com/p/googletest/). The Python
modules use Python native unittest.

To build the Boost wrappers you will, of course, need to install
[Boost](http://www.boost.org).

### [googletest](https://code.google.com/p/googletest/)

The C++ library uses [googletest](https://code.google.com/p/googletest/) to
run the unit tests. I have downloaded and built it in /usr/local by
following the instructions in the README

```
[root@lrmz-iMac gtest-1.7.0]# export GTEST_DIR=/usr/local/gtest-1.7.0
[root@lrmz-iMac gtest-1.7.0]# g++ -isystem ${GTEST_DIR}/include -I${GTEST_DIR} -pthread -c ${GTEST_DIR}/src/gtest-all.cc

[root@lrmz-iMac gtest-1.7.0]# ar -rv libgtest.a gtest-all.o
ar: creating archive libgtest.a
a - gtest-all.o
```

libAngles/Makefile sets its GTEST_DIR to /usr/local/gtest-1.7.0 and picks
up libgtest.a from there.


### [Boost](http://www.boost.org)

I have been wanting to use [homebrew](http://brew.sh) to install
boost, but some reason, I find it does not yet install
libboost_python.a by default or even with the --with-python or
--build-from-source options. So I built and installed it from source.

```
cd boost_1_56_0

./bootstrap.sh
./b2
sudo ./b2 install
```

The files are now in /usr/local/include and /usr/local/lib/libboost_*
and python/Boost/setup.py sets BOOST_ROOT to point there.
brew doctor will notice and complain about this.


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
Caught RangeError: maximum exceeded
```

### Python

Use the pylaunch.sh script to set the environment varialbes.

```
$ pwd
/Users/.../Angles/python/Manual
$ ./pylaunch.sh

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

- TBD

### Boost

- rich comparison operators
- deep copy *RuntimeError: Pickling of "angles.Angle" instances is not enabled (http://www.boost.org/libs/python/doc/v2/pickle.html*



