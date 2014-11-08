// ==================================================================
// Filename:    angles.cpp
//
// Description: This implements the angles class.
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
		     const double& a_sec) {
  value(degrees2seconds(a_deg_or_hr, a_min, a_sec)/3600.0);
}

Angles::Angle::Angle(const std::string& a_deg_or_hr,
		     const std::string& a_min,
		     const std::string& a_sec) {
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

Angles::Angle& Angles::Angle::operator/=(const Angle& rhs) throw (DivideByZeroError) {
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





// operator<<

void Angles::value2DMSString(const double& a_value, std::stringstream& a_string) {

  bool isNegative(false);

  if (a_value < 0)
    isNegative = true;

  double degrees = fabs(a_value);
  double minutes = 60 * (degrees - floor(degrees));
  double seconds = 60 * (minutes - floor(minutes));

  if (isNegative)
    degrees = -1 * floor(degrees);
  else
    degrees = floor(degrees);

  a_string << degrees << "* " << floor(minutes) << "\' " << seconds << "\"";

}

void Angles::value2HMSString(const double& a_value, std::stringstream& a_string) {

  bool isNegative(false);

  if (a_value < 0)
    isNegative = true;

  double degrees = fabs(a_value);
  double minutes = 60 * (degrees - floor(degrees));
  double seconds = 60 * (minutes - floor(minutes));

  if (isNegative)
    degrees = -1 * floor(degrees);
  else
    degrees = floor(degrees);

  a_string << degrees << ":" << floor(minutes) << ":" << seconds; // TODO use this form for others?

}
