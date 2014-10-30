#!/usr/bin/env bash
#
# Shell wrapper to set up library path for sim
#
# TODO: add linux support
#

if [ -z "$ANGLES_ROOT" ]; then
    ANGLES_ROOT=..
    echo "# ANGLES_ROOT not set. Using" $ANGLES_ROOT
else
    echo "# ANGLES_ROOT is" $ANGLES_ROOT
fi

ANGLES_LIBRARY_PATH=${ANGLES_ROOT}/libAngles

# if OSX
DYLD_LIBRARY_PATH=${ANGLES_LIBRARY_PATH} ${ANGLES_ROOT}/libAngles/example1 "$@"

# EoF
