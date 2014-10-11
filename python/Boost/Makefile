# ===============================================================
# Filename:    Makefile
# Description: Makefile to run build, test commands
# Author:      L.R. McFarland
# Created:     2014sep29
# ===============================================================

OSXFLAGS = env ARCHFLAGS="-arch x86_64"

all: build

build: setup.py boost_angle_module.cpp
	${OSXFLAGS} python setup.py build

test: build test_angles.py
	./test_angles.sh -v

clean:
	rm -rf build

clobber:
	rm -rf build
	rm *~
