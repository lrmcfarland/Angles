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
    ANGLE_ROOT=..
    echo "# ANGLE_ROOT not set. Using" $ANGLE_ROOT
fi

# ----------------------
# ----- Gtest root -----
# ----------------------

if [ -n "$GTEST_DIR" ]; then
    echo "# GTEST_DIR is" $ANGLE_ROOT
else
    GTEST_DIR=/usr/local/gtest-1.7.0
    echo "# GTEST_DIR not set. Using" $GTEST_DIR
fi


# ----------------------------
# ----- set library path -----
# ----------------------------

ANGLE_LIBRARY_PATH=${ANGLE_ROOT}/libAngles
GTEST_LIBRARY_PATH=${GTEST_DIR}/lib/.libs

export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:${ANGLE_LIBRARY_PATH}:${GTEST_LIBRARY_PATH}

# -----------------------
# ----- echo result -----
# -----------------------

echo '# DYLD_LIBRARY_PATH' ${DYLD_LIBRARY_PATH}
echo  # linefeed

# EoF
