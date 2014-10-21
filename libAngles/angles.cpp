// ==================================================================
// Filename:    sexagesimal.cpp
// Description: Implements the sexagesimal class
//              This file is part of lrm's Orbits software library.
//
// Author:      L.R. McFarland, lrm@starbug.com
// Created:     2014 June 19
// Language:    C++
//
//  Angles is free software: you can redistribute it and/or modify it
//  under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  Angles is distributed in the hope that it will be useful, but
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with Orbits.  If not, see <http://www.gnu.org/licenses/>.
// ==================================================================

#include <angles.h>
#include <utils.h>

// =================
// ===== Angle =====
// =================

// ----- constructors -----

Angles::Angle::Angle(const double& a_deg_or_hr,
		     const double& a_min,
		     const double& a_sec,
		     const double& a_minimum,
		     const double& a_maximum)
  : m_minimum(a_minimum), m_maximum(a_maximum) {
  value(degrees2seconds(a_deg_or_hr, a_min, a_sec)/3600.0);
}

Angles::Angle::Angle(const std::string& a_deg_or_hr,
		     const std::string& a_min,
		     const std::string& a_sec,
		     const double& a_minimum,
		     const double& a_maximum)
  : m_minimum(a_minimum), m_maximum(a_maximum) {
  value(Angle(Angles::stod(a_deg_or_hr),
	      Angles::stod(a_min),
	      Angles::stod(a_sec)).value());
  // TODO bad string exception with C++11 stod
  // TODO delegating constructors in C++11
}

// ----- operators -----

Angles::Angle& Angles::Angle::operator+=(const Angle& rhs) {
  m_value += rhs.value();
  return *this;
}

Angles::Angle& Angles::Angle::operator-=(const Angle& rhs) {
  m_value -= rhs.value();
  return *this;
}

Angles::Angle& Angles::Angle::operator*=(const Angle& rhs) {
  m_value *= rhs.value();
  return *this;
}

Angles::Angle& Angles::Angle::operator/=(const Angle& rhs) throw (DivideByZeroError, RangeError) {
  // LimitedRangeAngle can also raise RangeError
  if (rhs.value() == 0)
    throw DivideByZeroError();
  m_value /= rhs.value();
  return *this;
}

Angles::Angle Angles::operator+(const Angles::Angle& lhs, const Angles::Angle& rhs) {
  return Angles::Angle(lhs.value() + rhs.value());
}

Angles::Angle Angles::operator-(const Angles::Angle& lhs, const Angles::Angle& rhs) {
  return Angles::Angle(lhs.value() - rhs.value());
}

Angles::Angle Angles::operator-(const Angles::Angle& rhs) {
  return Angles::Angle(-rhs.value());
}

Angles::Angle Angles::operator*(const Angles::Angle& lhs, const Angles::Angle& rhs) {
  return Angles::Angle(lhs.value() * rhs.value());
}

Angles::Angle Angles::operator/(const Angles::Angle& lhs, const Angles::Angle& rhs)
  throw (DivideByZeroError) {
  if (rhs.value() == 0)
    throw DivideByZeroError();
  return Angles::Angle(lhs.value() / rhs.value());
}


// other methods

// TODO RA?
// TODO this is not right
// >>> rad2deg(math.asin(math.sin(deg2rad(45))))
// 45.0
// >>> rad2deg(math.asin(math.sin(deg2rad(45+360))))
// -44.999999999999936
// >>> rad2deg(math.asin(math.sin(deg2rad(45-360))))
// -45.00000000000001
// >>> rad2deg(math.asin(math.sin(deg2rad(45+360*2))))
// 44.99999999999992
// >>> rad2deg(math.asin(math.sin(deg2rad(45+360*3))))
// -45.00000000000001
// >>> rad2deg(math.asin(math.sin(deg2rad(45+360*4))))
// 44.99999999999999
// TODO fix this Angle(45 * 10).normalize() != 180
// >>> rad2deg(math.acos(math.cos(deg2rad(45+360*4))))
// 45.00000000000001
// >>> rad2deg(math.acos(math.cos(deg2rad(45+360*5))))
// 314.99999999999983

void Angles::Angle::normalize() {
  // bring back into 0-360 range
  while (m_value > 360)
    m_value -= 360;
}


// =============================
// ===== LimitedRangeAngle =====
// =============================

// ----- constructor from string for building from xml ----

Angles::LimitedRangeAngle::LimitedRangeAngle(const double& a_deg_or_hr,
					     const double& a_min,
					     const double& a_sec,
					     const double& a_minimum,
					     const double& a_maximum) throw(RangeError)
  : Angle(a_deg_or_hr, a_min, a_sec, a_minimum, a_maximum) {

  if (value() < minimum())
      throw RangeError("minimum exceeded");

  if (value() > maximum())
      throw RangeError("maximum exceeded");

  value(value());
}

Angles::LimitedRangeAngle::LimitedRangeAngle(const std::string& a_deg_or_hr,
					     const std::string& a_min,
					     const std::string& a_sec,
					     const double& a_minimum,
					     const double& a_maximum) throw(RangeError)
  : Angle(a_deg_or_hr, a_min, a_sec, a_minimum, a_maximum) {
  value(LimitedRangeAngle(Angles::stod(a_deg_or_hr),
			  Angles::stod(a_min),
			  Angles::stod(a_sec),
			  a_minimum,
			  a_maximum).value());
  // TODO bad string exception with C++11 stod
  // TODO delegating constructors in C++11
}


// ----- inplace operators -----

Angles::LimitedRangeAngle& Angles::LimitedRangeAngle::operator+=(const LimitedRangeAngle& rhs)
  throw (RangeError) {

  if (minimum() != rhs.minimum())
    throw RangeError("range minimums are not equal");

  if (maximum() != rhs.maximum())
    throw RangeError("range maximums are not equal");

  double temp(value() + rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

Angles::LimitedRangeAngle& Angles::LimitedRangeAngle::operator-=(const LimitedRangeAngle& rhs)
  throw (RangeError) {

  if (minimum() != rhs.minimum())
    throw RangeError("range minimums are not equal");

  if (maximum() != rhs.maximum())
    throw RangeError("range maximums are not equal");

  double temp(value() - rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

Angles::LimitedRangeAngle& Angles::LimitedRangeAngle::operator*=(const Angles::LimitedRangeAngle& rhs)
  throw (RangeError) {

  double temp(value() * rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

Angles::LimitedRangeAngle& Angles::LimitedRangeAngle::operator/=(const Angles::LimitedRangeAngle& rhs)
  throw (DivideByZeroError, RangeError) {

  if (rhs.value() == 0)
    throw DivideByZeroError();

  double temp(value() / rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

// =======================
// ===== Declination =====
// =======================


// ----- constructor from string for building from xml ----

Angles::Declination::Declination(const double& a_deg,
				 const double& a_min,
				 const double& a_sec,
				 const double& a_minimum,
				 const double& a_maximum) throw(RangeError)
  : LimitedRangeAngle(a_deg, a_min, a_sec, a_minimum, a_maximum) {
  // TODO delegating constructors in C++11
}

Angles::Declination::Declination(const std::string& a_deg,
				 const std::string& a_min,
				 const std::string& a_sec,
				 const double& a_minimum,
				 const double& a_maximum) throw(RangeError)
  : LimitedRangeAngle(a_deg, a_min, a_sec, a_minimum, a_maximum) {
  // TODO delegating constructors in C++11
}


// ----- inplace operators -----

Angles::Declination& Angles::Declination::operator+=(const Declination& rhs)
  throw (RangeError) {

  if (minimum() != rhs.minimum())
    throw RangeError("range minimums are not equal");

  if (maximum() != rhs.maximum())
    throw RangeError("range maximums are not equal");

  double temp(value() + rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

Angles::Declination& Angles::Declination::operator-=(const Declination& rhs)
  throw (RangeError) {

  if (minimum() != rhs.minimum())
    throw RangeError("range minimums are not equal");

  if (maximum() != rhs.maximum())
    throw RangeError("range maximums are not equal");

  double temp(value() - rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

Angles::Declination& Angles::Declination::operator*=(const Angles::Declination& rhs)
  throw (RangeError) {

  double temp(value() * rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}

Angles::Declination& Angles::Declination::operator/=(const Angles::Declination& rhs)
  throw (DivideByZeroError, RangeError) {

  if (rhs.value() == 0)
    throw DivideByZeroError();

  double temp(value() / rhs.value());

  if (temp < minimum())
    throw RangeError("minimum exceeded");

  if (temp > maximum())
    throw RangeError("maximum exceeded");

  value(temp);

  return *this;
}


// =====================
// ===== Longitude =====
// =====================


// ----- constructor from string for building from xml ----

Angles::Longitude::Longitude(const double& a_deg,
			     const double& a_min,
			     const double& a_sec,
			     const double& a_minimum,
			     const double& a_maximum) throw(RangeError)
  : LimitedRangeAngle(a_deg, a_min, a_sec, a_minimum, a_maximum) {
  // TODO delegating constructors in C++11
}

Angles::Longitude::Longitude(const std::string& a_deg,
			     const std::string& a_min,
			     const std::string& a_sec,
			     const double& a_minimum,
			     const double& a_maximum) throw(RangeError)
  : LimitedRangeAngle(a_deg, a_min, a_sec, a_minimum, a_maximum) {
  // TODO delegating constructors in C++11
}

// ===========================
// ===== Right Ascension =====
// ===========================


// ----- constructor from string for building from xml ----

Angles::RA::RA(const double& a_hour,
	       const double& a_min,
	       const double& a_sec,
	       const double& a_minimum,
	       const double& a_maximum) throw(RangeError)
  : LimitedRangeAngle(a_hour, a_min, a_sec, a_minimum, a_maximum) {

  // TODO delegating constructors in C++11

}

Angles::RA::RA(const std::string& a_hour,
	       const std::string& a_min,
	       const std::string& a_sec,
	       const double& a_minimum,
	       const double& a_maximum) throw(RangeError)
  : LimitedRangeAngle(a_hour, a_min, a_sec, a_minimum, a_maximum) {

  // TODO delegating constructors in C++11

}


