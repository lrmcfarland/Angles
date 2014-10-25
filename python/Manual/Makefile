# ===============================================================
# Filename:    Makefile
# Description: makefile to run build, test commands
# Author:      L.R. McFarland
# Created:     2014 oct 10
# ===============================================================

OSXFLAGS = env ARCHFLAGS="-arch x86_64"
RM       = rm -rf

all: build

build: gen_angles_module.py angles.cpp setup.py
	./gen_angles_module.py
	${OSXFLAGS} python setup.py build

angles.cpp: gen_angles_module.py
	./gen_angles_module.py

test: build test_angles.py
	./test_angles.sh -v

test_angles.py: gen_test_angles.py
	./gen_test_angles.py

clean:
	-$(RM) angles.cpp
	-$(RM) test_angles.py
	-$(RM) build

clobber: clean
	-$(RM) *~
