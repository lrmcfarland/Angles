// ==========================================================================
// Filename:    boost_angle_module.cpp
//
// Description: Contains the python wrappers for the
//              Sexagesimal::angle objects using boost and python.
//
// Author:      L.R. McFarland
// Created:     2014sep29
// ==========================================================================

#include <boost/python.hpp>

#include "angles.h"

using namespace boost::python;

// overload wrappers
void (Angles::Angle::*setValue)(const double&) = &Angles::Angle::value;
void (Angles::Angle::*setRadians)(const double&) = &Angles::Angle::radians;


BOOST_PYTHON_MODULE(angles) {

  class_<Angles::Angle>("Angle")

    .def("deg2rad", &Angles::Angle::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::Angle::rad2deg)
    .staticmethod("rad2deg")

    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))

    // constructors
    .def(init<>()) // default
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    .def(init<Angles::Angle>()) // copy

    .def(init<double>()) // degrees

    // accessors

    .def("getValue", &Angles::Angle::getValue)
    .def("setValue", setValue)
    .add_property("value", &Angles::Angle::getValue, setValue)

    .def("getRadians", &Angles::Angle::getRadians)
    .def("setRadians", setRadians)
    .add_property("radians", &Angles::Angle::getRadians, setRadians)

    // TODO rich compare

    // operators
    .def(self + Angles::Angle())
    .def(Angles::Angle() + self)

    .def(self - Angles::Angle())
    .def(Angles::Angle() - self)

    .def(self * double())
    .def(double() * self)

    .def(self / double())
    .def(double() / self)

    .def("normalize", &Angles::Angle::normalize)

    ; // end of Angle class_



  class_<Angles::LimitedRangeAngle, bases<Angles::Angle> >("LimitedRangeAngle")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::LimitedRangeAngle>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds
    .def(init<double, double, double, double>()) // degrees, minutes, seconds, minimum
    .def(init<double, double, double, double, double>()) // degrees, minutes, seconds, minimum, maximum

    // accessors
    .def("minimum", &Angles::LimitedRangeAngle::getMinimum)
    .add_property("minimum", &Angles::LimitedRangeAngle::getMinimum)

    .def("maximum", &Angles::LimitedRangeAngle::getMaximum)
    .add_property("maximum", &Angles::LimitedRangeAngle::getMaximum)

    ; // end of LimitedRangeAngle class_



  class_<Angles::Declination, bases<Angles::LimitedRangeAngle> >("Declination")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::Declination>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds
    .def(init<double, double, double, double>()) // degrees, minutes, seconds, minimum
    .def(init<double, double, double, double, double>()) // degrees, minutes, seconds, minimum, maximum

    ; // end of Declination class_


  class_<Angles::Latitude, bases<Angles::LimitedRangeAngle> >("Latitude")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::Latitude>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds
    .def(init<double, double, double, double>()) // degrees, minutes, seconds, minimum
    .def(init<double, double, double, double, double>()) // degrees, minutes, seconds, minimum, maximum

    ; // end of Latitude class_


  class_<Angles::Longitude, bases<Angles::LimitedRangeAngle> >("Longitude")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::Longitude>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds
    .def(init<double, double, double, double>()) // degrees, minutes, seconds, minimum
    .def(init<double, double, double, double, double>()) // degrees, minutes, seconds, minimum, maximum

    ; // end of Longitude class_


  class_<Angles::RA, bases<Angles::LimitedRangeAngle> >("RA")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::RA>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds
    .def(init<double, double, double, double>()) // degrees, minutes, seconds, minimum
    .def(init<double, double, double, double, double>()) // degrees, minutes, seconds, minimum, maximum

    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))

    ; // end of RA class_



};
