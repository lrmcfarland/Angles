#!/usr/bin/env python


module_header = """// THIS IS A GENERATED FILE. EDITS WILL BE OVERWRITTEN.

// ==========================================================================
// Filename:    angles.cpp
//
// Description: Contains the python wrappers for the Angles objects
//              using boost and python. Lots of cut and paste in this
//              implementation since it uses templates and not
//              inheritance.
//
//
// Author:      L.R. McFarland
// Created:     2014sep29
// ==========================================================================

#include <boost/python.hpp>

#include "angles.h"

using namespace boost::python;

// overload wrappers
"""

wrapper_template = """
void (Angles::%(TypeName)s::*set%(TypeName)sValue)(const double&) = &Angles::%(TypeName)s::value;
void (Angles::%(TypeName)s::*set%(TypeName)sRadians)(const double&) = &Angles::%(TypeName)s::radians;
"""

module_init = """
BOOST_PYTHON_MODULE(angles) {
"""

angle_class_template = """

  class_<Angles::Angle>("Angle")

    .def("deg2rad", &Angles::Angle::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::Angle::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    .def(init<Angles::Angle>()) // copy

    // accessors

    .def("getValue", &Angles::Angle::getValue)
    .def("setValue", setAngleValue)
    .add_property("value", &Angles::Angle::getValue, setAngleValue)

    .def("getRadians", &Angles::Angle::getRadians)
    .def("setRadians", setAngleRadians)
    .add_property("radians", &Angles::Angle::getRadians, setAngleRadians)

    // TODO rich compare

    // operators
    .def(self + Angles::Angle())
    .def(Angles::Angle() + self)

    .def(self - Angles::Angle())
    .def(Angles::Angle() - self)

    .def(self * Angles::Angle())
    .def(Angles::Angle() * self)

    .def(self / Angles::Angle())
    .def(Angles::Angle() / self)

    .def("normalize", &Angles::Angle::normalize)

    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))

    ; // end of Angle class_
"""

angle_template_template = """

  class_<Angles::%(TypeName)s>("%(TypeName)s")

    .def("deg2rad", &Angles::%(TypeName)s::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::%(TypeName)s::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::%(TypeName)s>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    // accessors

    .def("getValue", &Angles::%(TypeName)s::getValue)
    .def("setValue", set%(TypeName)sValue)
    .add_property("value", &Angles::%(TypeName)s::getValue, set%(TypeName)sValue)

    .def("getRadians", &Angles::%(TypeName)s::getRadians)
    .def("setRadians", set%(TypeName)sRadians)
    .add_property("radians", &Angles::%(TypeName)s::getRadians, set%(TypeName)sRadians)

    .def("minimum", &Angles::%(TypeName)s::getMinimum)
    .add_property("minimum", &Angles::%(TypeName)s::getMinimum)

    .def("maximum", &Angles::%(TypeName)s::getMaximum)
    .add_property("maximum", &Angles::%(TypeName)s::getMaximum)

    // TODO rich compare

    // operators
    .def(self + Angles::%(TypeName)s())
    .def(Angles::%(TypeName)s() + self)

    .def(self - Angles::%(TypeName)s())
    .def(Angles::%(TypeName)s() - self)

    .def(self * Angles::%(TypeName)s())
    .def(Angles::%(TypeName)s() * self)

    .def(self / Angles::%(TypeName)s())
    .def(Angles::%(TypeName)s() / self)


    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))


    ; // end of %(TypeName)s class_
"""

module_close = """
};
"""

# ================
# ===== main =====
# ================

if __name__ == '__main__':

    angle_classes = list()
    angle_classes.append({'TypeName': 'Angle'})

    angle_templates = list()
    angle_templates.append({'TypeName': 'LimitedRangeAngle'})
    angle_templates.append({'TypeName': 'Declination'})
    angle_templates.append({'TypeName': 'Latitude'})
    angle_templates.append({'TypeName': 'Longitude'})
    angle_templates.append({'TypeName': 'RA'})


    flnm = 'angles.cpp'
    afp = open(flnm, 'w')

    afp.write(module_header)

    for angle_class in angle_classes:
        afp.write(wrapper_template % angle_class)

    for angle_template in angle_templates:
        afp.write(wrapper_template % angle_template)

    afp.write(module_init)

    for angle_class in angle_classes:
        afp.write(angle_class_template % angle_class)

    for angle_template in angle_templates:
        afp.write(angle_template_template % angle_template)

    afp.write(module_close) # final brace

    afp.close()

