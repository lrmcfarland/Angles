// ================================================================
// Filename:    angles.hpp
//
// Description: This implements the angles template,
//              e.g. declination, right ascension, latitude and
//              longitude as a full featured c++ object. For use in
//              astronomy equatorial coordinate system applications.
//
// Author:      L.R. McFarland, lrm@starbug.com
// Created:     2014 Jun 21
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
// ================================================================

#pragma once

namespace Angles {

  // constructor from doubles
  template<int A_MINIMUM, int A_MAXIMUM>  // only ints can be non-type arguments
    LRA<A_MINIMUM, A_MAXIMUM>::LRA(const double& a_deg,
				   const double& a_min,
				   const double& a_sec) throw (RangeError)
    : m_minimum(A_MINIMUM), m_maximum(A_MAXIMUM)
  {
    double temp(degrees2seconds(a_deg, a_min, a_sec)/3600.0);
    setValue(temp);
  };

  // constructor from strings
  template<int A_MINIMUM, int A_MAXIMUM>  // only ints can be non-type arguments
    LRA<A_MINIMUM, A_MAXIMUM>::LRA(const std::string& a_deg,
				   const std::string& a_min,
				   const std::string& a_sec) throw (RangeError)
    : m_minimum(A_MINIMUM), m_maximum(A_MAXIMUM)
  {

    // TODO bad string exception with C++11 stod
    // TODO delegating constructors in C++11

    double temp(degrees2seconds(Angles::stod(a_deg),
				Angles::stod(a_min),
				Angles::stod(a_sec))/3600.0);
    setValue(temp);
  };

  // copy constructor
  template<int A_MINIMUM, int A_MAXIMUM>
    LRA<A_MINIMUM, A_MAXIMUM>::LRA(const LRA& a) {
    m_value = a.value();
    m_minimum = a.minimum();
    m_maximum = a.maximum();
  }

  // copy assign
  template<int A_MINIMUM, int A_MAXIMUM>
    LRA<A_MINIMUM, A_MAXIMUM>& LRA<A_MINIMUM, A_MAXIMUM>::operator=(const LRA& rhs) {
    if (this == &rhs) return *this;
    m_value = rhs.value();
    m_minimum = rhs.minimum();
    m_maximum = rhs.maximum();
    return *this;
  }

  // booleans

  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::operator== (const LRA& rhs) const {
    return m_value == rhs.value();
  }

  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::operator!= (const LRA& rhs) const {
    return !operator==(rhs);
  }

  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::operator< (const LRA& rhs) const {
    return m_value < rhs.value();
  }

  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::operator<= (const LRA& rhs) const {
    return m_value <= rhs.value();
  }

  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::operator> (const LRA& rhs) const {
    return m_value > rhs.value();
  }

  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::operator>= (const LRA& rhs) const {
    return m_value >= rhs.value();
  }


  // in-place arithmetic operator method templates

  // value
  template<int A_MINIMUM, int A_MAXIMUM>
    void LRA<A_MINIMUM, A_MAXIMUM>::setValue(const double& a_value) throw (RangeError) {
    validRange(a_value);
    m_value = a_value;
  }

  // validRange
  template<int A_MINIMUM, int A_MAXIMUM>
    void LRA<A_MINIMUM, A_MAXIMUM>::validRange(const double& a_value) const throw (RangeError) {
    if (a_value < minimum())
      throw RangeError("minimum exceeded");
    if (a_value > maximum())
      throw RangeError("maximum exceeded");
  }

  // isValidRange
  // less informative range check for manual python exception issues.
  template<int A_MINIMUM, int A_MAXIMUM>
    bool LRA<A_MINIMUM, A_MAXIMUM>::isValidRange(const double& a_value) const {
    if (a_value < minimum())
      return false;
    if (a_value > maximum())
      return false;
    return true;
  }

  // add
  template<int A_MINIMUM, int A_MAXIMUM>
    LRA<A_MINIMUM, A_MAXIMUM>& LRA<A_MINIMUM, A_MAXIMUM>::operator+=(const LRA& rhs)
    throw (RangeError) {
    double temp(value() + rhs.value());
    validRange(temp);
    value(temp);
    return *this;
  }

  // subtract
  template<int A_MINIMUM, int A_MAXIMUM>
    LRA<A_MINIMUM, A_MAXIMUM>& LRA<A_MINIMUM, A_MAXIMUM>::operator-=(const LRA& rhs)
    throw (RangeError) {
    double temp(value() - rhs.value());
    validRange(temp);
    value(temp);
    return *this;
  }


  // multiply
  template<int A_MINIMUM, int A_MAXIMUM>
    LRA<A_MINIMUM, A_MAXIMUM>& LRA<A_MINIMUM, A_MAXIMUM>::operator*=(const LRA& rhs)
    throw (RangeError) {
    double temp(value() * rhs.value());
    validRange(temp);
    value(temp);
    return *this;
  }


  // divide
  template<int A_MINIMUM, int A_MAXIMUM>
    LRA<A_MINIMUM, A_MAXIMUM>& LRA<A_MINIMUM, A_MAXIMUM>::operator/=(const LRA& rhs)
    throw (DivideByZeroError, RangeError) {
    if (rhs.value() == 0)
      throw DivideByZeroError();
    double temp(value() / rhs.value());
    validRange(temp);
    value(temp);
    return *this;
  }

 // arithmetic operator function templates

  // add
  template <typename T>
    T operator+(const T& lhs, const T& rhs) throw (RangeError) {
    double temp(lhs.value() + rhs.value());
    lhs.validRange(temp);
    return T(temp);
  }

  // subtract
  template <typename T>
    T operator-(const T& lhs, const T& rhs) throw (RangeError) {
    double temp(lhs.value() - rhs.value());
    lhs.validRange(temp);
    return T(temp);
  }

  // unitary minus
  template <typename T>
    T operator-(const T& rhs) throw(RangeError) {
    double temp(-rhs.value());
    rhs.validRange(temp);
    return T(temp);
  }

  // multiply
  template <typename T>
    T operator*(const T& lhs, const T& rhs) throw (RangeError) {
    double temp(lhs.value() * rhs.value());
    lhs.validRange(temp);
    return T(temp);
  }

  // divide
  template <typename T>
    T operator/(const T& lhs, const T& rhs) throw (DivideByZeroError, RangeError) {
    if (rhs.value() == 0)
      throw DivideByZeroError();
    double temp(lhs.value() / rhs.value());
    lhs.validRange(temp);
    return T(temp);
  }


  // =============================
  // ===== output operator<< =====
  // =============================

  std::ostream& operator<< (std::ostream& os, const Angles::Angle& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::LimitedRangeAngle& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::Declination& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::Longitude& a) {
    std::stringstream out;
    Angles::value2DMSString(a.value(), out);
    return os << out.str();
  }

  std::ostream& operator<< (std::ostream& os, const Angles::RA& a) {
    std::stringstream out;
    Angles::value2HMSString(a.value(), out);
    return os << out.str();
  }

}
