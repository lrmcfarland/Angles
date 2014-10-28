#!/usr/bin/env bash
#
# Shell wrapper to set up OS X python environment
#
# TODO: add linux support
#

# -----------------------
# ----- Angles root -----
# -----------------------

if [ -n "$ANGLE_ROOT" ]; then
    echo "# ANGLE_ROOT is" $ANGLE_ROOT
else
    ANGLE_ROOT=../..
    echo "# ANGLE_ROOT not set. Using" $ANGLE_ROOT
fi

# ----------------------------
# ----- set library path -----
# ----------------------------

ANGLE_LIBRARY_PATH=${ANGLE_ROOT}/libAngles
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:${ANGLE_LIBRARY_PATH}

# ---------------------------
# ----- set python path -----
# ---------------------------

ANGLES_SO=`find ${ANGLE_ROOT}/python/Boost -name angles.so`

if [ -n "$ANGLES_SO" ]; then
    echo "# angles.so:" $ANGLE_SO
    export PYTHONPATH=${PYTHONPATH}:$(dirname ${ANGLES_SO})
else
    echo "angles.so not found"
    exit 1
fi

# -----------------------
# ----- echo result -----
# -----------------------

echo '# DYLD_LIBRARY_PATH' ${DYLD_LIBRARY_PATH}
echo '# PYTHONPATH' ${PYTHONPATH}
echo  # linefeed

# EoF
