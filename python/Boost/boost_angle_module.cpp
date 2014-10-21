// ==========================================================================
// Filename:    boost_angle_module.cpp
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
void (Angles::Angle::*setAngleValue)(const double&) = &Angles::Angle::value;
void (Angles::Angle::*setAngleRadians)(const double&) = &Angles::Angle::radians;

void (Angles::LimitedRangeAngle::*setLimitedRangeAngleValue)(const double&) = &Angles::LimitedRangeAngle::value;
void (Angles::LimitedRangeAngle::*setLimitedRangeAngleRadians)(const double&) = &Angles::LimitedRangeAngle::radians;

void (Angles::Declination::*setDeclinationValue)(const double&) = &Angles::Declination::value;
void (Angles::Declination::*setDeclinationRadians)(const double&) = &Angles::Declination::radians;

void (Angles::Latitude::*setLatitudeValue)(const double&) = &Angles::Latitude::value;
void (Angles::Latitude::*setLatitudeRadians)(const double&) = &Angles::Latitude::radians;

void (Angles::Longitude::*setLongitudeValue)(const double&) = &Angles::Longitude::value;
void (Angles::Longitude::*setLongitudeRadians)(const double&) = &Angles::Longitude::radians;

void (Angles::RA::*setRAValue)(const double&) = &Angles::RA::value;
void (Angles::RA::*setRARadians)(const double&) = &Angles::RA::radians;



BOOST_PYTHON_MODULE(angles) {

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



  class_<Angles::LimitedRangeAngle>("LimitedRangeAngle")

    .def("deg2rad", &Angles::LimitedRangeAngle::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::LimitedRangeAngle::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::LimitedRangeAngle>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    // accessors

    .def("getValue", &Angles::LimitedRangeAngle::getValue)
    .def("setValue", setLimitedRangeAngleValue)
    .add_property("value", &Angles::LimitedRangeAngle::getValue, setLimitedRangeAngleValue)

    .def("getRadians", &Angles::LimitedRangeAngle::getRadians)
    .def("setRadians", setLimitedRangeAngleRadians)
    .add_property("radians", &Angles::LimitedRangeAngle::getRadians, setLimitedRangeAngleRadians)

    .def("minimum", &Angles::LimitedRangeAngle::getMinimum)
    .add_property("minimum", &Angles::LimitedRangeAngle::getMinimum)

    .def("maximum", &Angles::LimitedRangeAngle::getMaximum)
    .add_property("maximum", &Angles::LimitedRangeAngle::getMaximum)

    // TODO rich compare

    // operators
    .def(self + Angles::LimitedRangeAngle())
    .def(Angles::LimitedRangeAngle() + self)

    .def(self - Angles::LimitedRangeAngle())
    .def(Angles::LimitedRangeAngle() - self)

    .def(self * Angles::LimitedRangeAngle())
    .def(Angles::LimitedRangeAngle() * self)

    .def(self / Angles::LimitedRangeAngle())
    .def(Angles::LimitedRangeAngle() / self)


    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))


    ; // end of LimitedRangeAngle class_




  class_<Angles::Declination>("Declination")

    .def("deg2rad", &Angles::Declination::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::Declination::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::Declination>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    // accessors

    .def("getValue", &Angles::Declination::getValue)
    .def("setValue", setDeclinationValue)
    .add_property("value", &Angles::Declination::getValue, setDeclinationValue)

    .def("getRadians", &Angles::Declination::getRadians)
    .def("setRadians", setDeclinationRadians)
    .add_property("radians", &Angles::Declination::getRadians, setDeclinationRadians)

    .def("minimum", &Angles::Declination::getMinimum)
    .add_property("minimum", &Angles::Declination::getMinimum)

    .def("maximum", &Angles::Declination::getMaximum)
    .add_property("maximum", &Angles::Declination::getMaximum)

    // TODO rich compare

    // operators
    .def(self + Angles::Declination())
    .def(Angles::Declination() + self)

    .def(self - Angles::Declination())
    .def(Angles::Declination() - self)

    .def(self * Angles::Declination())
    .def(Angles::Declination() * self)

    .def(self / Angles::Declination())
    .def(Angles::Declination() / self)


    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))


    ; // end of Declination class_


  // Latitude and Declination are the same templates only typedef-ed
  // differently.


  class_<Angles::Latitude>("Latitude")

    .def("deg2rad", &Angles::Latitude::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::Latitude::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::Latitude>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    // accessors

    .def("getValue", &Angles::Latitude::getValue)
    .def("setValue", setLatitudeValue)
    .add_property("value", &Angles::Latitude::getValue, setLatitudeValue)

    .def("getRadians", &Angles::Latitude::getRadians)
    .def("setRadians", setLatitudeRadians)
    .add_property("radians", &Angles::Latitude::getRadians, setLatitudeRadians)

    .def("minimum", &Angles::Latitude::getMinimum)
    .add_property("minimum", &Angles::Latitude::getMinimum)

    .def("maximum", &Angles::Latitude::getMaximum)
    .add_property("maximum", &Angles::Latitude::getMaximum)

    // TODO rich compare

    // operators
    .def(self + Angles::Latitude())
    .def(Angles::Latitude() + self)

    .def(self - Angles::Latitude())
    .def(Angles::Latitude() - self)

    .def(self * Angles::Latitude())
    .def(Angles::Latitude() * self)

    .def(self / Angles::Latitude())
    .def(Angles::Latitude() / self)


    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))


    ; // end of Latitude class_


  class_<Angles::Longitude>("Longitude")

    .def("deg2rad", &Angles::Longitude::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::Longitude::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::Longitude>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    // accessors

    .def("getValue", &Angles::Longitude::getValue)
    .def("setValue", setLongitudeValue)
    .add_property("value", &Angles::Longitude::getValue, setLongitudeValue)

    .def("getRadians", &Angles::Longitude::getRadians)
    .def("setRadians", setLongitudeRadians)
    .add_property("radians", &Angles::Longitude::getRadians, setLongitudeRadians)

    .def("minimum", &Angles::Longitude::getMinimum)
    .add_property("minimum", &Angles::Longitude::getMinimum)

    .def("maximum", &Angles::Longitude::getMaximum)
    .add_property("maximum", &Angles::Longitude::getMaximum)

    // TODO rich compare

    // operators
    .def(self + Angles::Longitude())
    .def(Angles::Longitude() + self)

    .def(self - Angles::Longitude())
    .def(Angles::Longitude() - self)

    .def(self * Angles::Longitude())
    .def(Angles::Longitude() * self)

    .def(self / Angles::Longitude())
    .def(Angles::Longitude() / self)


    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))


    ; // end of Longitude class_


  class_<Angles::RA>("RA")

    .def("deg2rad", &Angles::RA::deg2rad)
    .staticmethod("deg2rad")

    .def("rad2deg", &Angles::RA::rad2deg)
    .staticmethod("rad2deg")

    // constructors
    .def(init<>()) // default
    .def(init<Angles::RA>()) // copy

    .def(init<double>()) // degrees
    .def(init<double, double>()) // degrees, minutes
    .def(init<double, double, double>()) // degrees, minutes, seconds

    // accessors

    .def("getValue", &Angles::RA::getValue)
    .def("setValue", setRAValue)
    .add_property("value", &Angles::RA::getValue, setRAValue)

    .def("getRadians", &Angles::RA::getRadians)
    .def("setRadians", setRARadians)
    .add_property("radians", &Angles::RA::getRadians, setRARadians)

    .def("minimum", &Angles::RA::getMinimum)
    .add_property("minimum", &Angles::RA::getMinimum)

    .def("maximum", &Angles::RA::getMaximum)
    .add_property("maximum", &Angles::RA::getMaximum)

    // TODO rich compare

    // operators
    .def(self + Angles::RA())
    .def(Angles::RA() + self)

    .def(self - Angles::RA())
    .def(Angles::RA() - self)

    .def(self * Angles::RA())
    .def(Angles::RA() * self)

    .def(self / Angles::RA())
    .def(Angles::RA() / self)


    // operator<<(), str not repr
    .def(self_ns::str(self_ns::self))


    ; // end of RA class_



};
