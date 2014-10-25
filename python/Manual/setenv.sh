#!/usr/bin/env bash
#
# Shell wrapper to set up python environment
#
# TODO: add linux support
#

# --------------------------------
# ----- Cartesian space root -----
# --------------------------------

if [ -n "$ANGLES_ROOT" ]; then
    echo "# ANGLES_ROOT is" $ANGLES_ROOT
else
    ANGLES_ROOT=../..
    echo "# ANGLES_ROOT not set. Using" $ANGLES_ROOT
fi

# ----------------------------
# ----- set library path -----
# ----------------------------

ANGLES_LIBRARY_PATH=${ANGLES_ROOT}/libAngles
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:${ANGLES_LIBRARY_PATH}

# ---------------------------
# ----- set python path -----
# ---------------------------

ANGLES_SO=`find  ${ANGLES_ROOT}/python/Manual -name angles.so`

if [ -n "$ANGLES_SO" ]; then
    echo "# space.so:" $ANGLES_SO
    export PYTHONPATH=${PYTHONPATH}:$(dirname ${ANGLES_SO})
else
    echo "space.so not found"
    exit 1
fi

# -----------------------
# ----- echo result -----
# -----------------------

echo '# DYLD_LIBRARY_PATH' ${DYLD_LIBRARY_PATH}
echo '# PYTHONPATH' ${PYTHONPATH}
echo  # linefeed

# EoF
