// ================================================================
// Filename:    angle.h
//
// Description: This is an implementation of angles, e.g. declination,
//              right ascension, latitude and longitude as a full
//              featured c++ object. For use in astronomy equatorial
//              coordinate system applications.
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


// Notes: I had originaly had angles */ doubles, doubles */ angles and
// could overload the operators directly, but when I tired to make
// templates of this, I got a compile "error: overloaded 'operator*'
// must have at least one parameter of class or enumeration type"
// I decided it was apples and oranges anyway and removed it.
//
// Angles "specialized" to ignore range, but Angles *
// LimitedRangeAngle returns an Angle even if it is out of range.
//
// Angles has min/max but does not use them. LimitedRangeAngles
// assumes the template sets them the same for all instances.




#pragma once

#include <cmath>
#include <sstream>
#include <stdexcept>

#include <utils.h>


 
namespace Angles {

  // =================
  // ===== Angle =====
  // =================

  class Angle {
    // base class for latitude, longitude, declination and right ascension

  public:
    // angle unit convertors
    static double deg2rad(const double& deg) {return deg*M_PI/180.0;}
    static double rad2deg(const double& rad) {return rad*180.0/M_PI;}

    // ----- ctor and dtor -----

    explicit Angle(const double& a_deg = 0.0,
		   const double& a_min = 0.0,
		   const double& a_sec = 0.0,
		   const double& a_minimum = 0.0,
		   const double& a_maximum = 360);

    explicit Angle(const std::string& a_deg, // The ambiguity is in the box.
		   const std::string& a_min = "0",
		   const std::string& a_sec = "0",
		   const double& a_minimum = 0.0,
		   const double& a_maximum = 360);

    virtual ~Angle() {};

    inline Angle(const Angle& a);
    inline Angle& operator=(const Angle& rhs);

    // ----- accessor -----
    void          value(const double& a_value) {m_value = a_value;}
    const double& value() const                {return m_value;}
    double        getValue() const             {return m_value;} // for boost

    virtual void   radians(const double& a_value) {value(rad2deg(a_value));}
    virtual double radians() const                {return deg2rad(value());}
    double         getRadians() const             {return deg2rad(value());} // for boost

    // not enforced by Angle, but is here to simplify wrapper
    // generation for LimitedRangeAngles
    const double& minimum() const {return m_minimum;}
    double        getMinimum() const {return m_minimum;} // for boost

    const double& maximum() const {return m_maximum;}
    double        getMaximum() const {return m_maximum;} // for boost

    // ----- bool operators -----

    inline bool operator== (const Angle& rhs) const;
    inline bool operator!= (const Angle& rhs) const;

    inline bool operator< (const Angle& rhs) const;
    inline bool operator<= (const Angle& rhs) const;

    inline bool operator> (const Angle& rhs) const;
    inline bool operator>= (const Angle& rhs) const;

    // ----- inplace operators -----

    virtual Angle& operator+=(const Angle& rhs);
    virtual Angle& operator-=(const Angle& rhs);

    virtual Angle& operator*=(const Angle& rhs);
    virtual Angle& operator/=(const Angle& rhs) throw (DivideByZeroError, RangeError);
    // LimitedRangeAngles can thow RangeError if dividing by a
    // fraction, so the base class can not narrow the error types.

    // ----- other methods -----
    virtual void normalize();  // TODO normalized -> return a new copy?

  private:

    double m_value; // degrees for declination, latitude, longitude, seconds for right ascension

    // not used here but simplifies python/Manual wrapper generation.
    double m_minimum;
    double m_maximum;

  };

  // ----- inline implementations of angle methods -----

  // copy constructor
  inline Angle::Angle(const Angle& a) {
    m_value = a.value();
    m_minimum = a.minimum();
    m_maximum = a.maximum();
  }

  // copy assignment
  inline Angle& Angle::operator=(const Angle& rhs) {
    if (this == &rhs) return *this;
    m_value = rhs.value();
    m_minimum = rhs.minimum();
    m_maximum = rhs.maximum();
    return *this;
  }

  // ----- bool operators -----

  inline bool Angle::operator== (const Angle& rhs) const {
    return m_value == rhs.value();
  }

  inline bool Angle::operator!= (const Angle& rhs) const {
    return !operator==(rhs);
  }

  inline bool Angle::operator< (const Angle& rhs) const {
    return m_value < rhs.value();
  }

  inline bool Angle::operator<= (const Angle& rhs) const {
    return m_value <= rhs.value();
  }

  inline bool Angle::operator> (const Angle& rhs) const {
    return m_value > rhs.value();
  }

  inline bool Angle::operator>= (const Angle& rhs) const {
    return m_value >= rhs.value();
  }

  // ---------------------------
  // ----- Angle operators -----
  // ---------------------------

  // Angle "specilizations" that do not check range.

  Angle operator+ (const Angle& lhs, const Angle& rhs);
  Angle operator- (const Angle& lhs, const Angle& rhs);
  Angle operator- (const Angle& rhs); // unitary minus

  Angle operator* (const Angle& lhs, const Angle& rhs);
  Angle operator/ (const Angle& lhs, const Angle& rhs) throw (DivideByZeroError);



  // =============================
  // ===== LimitedRangeAngle =====
  // =============================


 // limited range operator templates

  // add
  template <typename T>
    T operator+(const T& lhs, const T& rhs) throw (RangeError) {

    double temp(lhs.value() + rhs.value());

    // ASSUMES: template class has the same minimum and maximum for all instances.
    // TODO: construct angles from class template that enforces this.

    if (temp < lhs.minimum())
      throw RangeError("minimum exceeded");

    if (temp > lhs.maximum())
      throw RangeError("maximum exceeded");

    return T(temp);
  }


  // subtract
  template <typename T>
    T operator-(const T& lhs, const T& rhs) throw (RangeError) {

    double temp(lhs.value() - rhs.value());

    // ASSUMES: template class has the same minimum and maximum for all instances.
    // TODO: construct angles from class template that enforces this.

    if (temp < lhs.minimum())
      throw RangeError("minimum exceeded");

    if (temp > lhs.maximum())
      throw RangeError("maximum exceeded");

    return T(temp);
  }


  // unitary minus
  template <typename T>
    T operator-(const T& rhs) throw(RangeError) {

    double temp(-rhs.value());

    if (temp < rhs.minimum())
      throw RangeError("minimum exceeded");

    if (temp > rhs.maximum())
      throw RangeError("maximum exceeded");

    return T(temp);
  }


  // multiply
  template <typename T>
    T operator*(const T& lhs, const T& rhs) throw (RangeError) {

    double temp(lhs.value() * rhs.value());

    // ASSUMES: template class has the same minimum and maximum for all instances.
    // TODO: construct angles from class template that enforces this.

    if (temp < lhs.minimum())
      throw RangeError("minimum exceeded");

    if (temp > lhs.maximum())
      throw RangeError("maximum exceeded");

    return T(temp);
  }


  // divide
  template <typename T>
    T operator/(const T& lhs, const T& rhs) throw (RangeError) {

    double temp(lhs.value() / rhs.value());

    // ASSUMES: template class has the same minimum and maximum for all instances.
    // TODO: construct angles from class template that enforces this.

    if (temp < lhs.minimum())
      throw RangeError("minimum exceeded");

    if (temp > lhs.maximum())
      throw RangeError("maximum exceeded");

    return T(temp);
  }



  // TODO template this, but with min/max parameters at the template level



  class LimitedRangeAngle : public Angle {
    // enforces range limits on angles, e.g. longitude -180 to 180,
    // declination and latitude -90 to 90

  public:

    // ----- ctor and dtor -----

    explicit LimitedRangeAngle(const double& a_deg = 0.0,
			       const double& a_min = 0.0,
			       const double& a_sec = 0.0,
			       const double& a_minimum = 0.0,
			       const double& a_maximum = 360) throw (RangeError);

    explicit LimitedRangeAngle(const std::string& a_deg, // The ambiguity is in the box.
			       const std::string& a_min = "0",
			       const std::string& a_sec = "0",
			       const double& a_minimum = 0.0,
			       const double& a_maximum = 360) throw (RangeError);

    virtual ~LimitedRangeAngle() {};

    // ----- inplace operators -----

    virtual LimitedRangeAngle& operator+=(const LimitedRangeAngle& rhs) throw (RangeError);
    virtual LimitedRangeAngle& operator-=(const LimitedRangeAngle& rhs) throw (RangeError);

    virtual LimitedRangeAngle& operator*=(const LimitedRangeAngle& rhs) throw (RangeError);
    virtual LimitedRangeAngle& operator/=(const LimitedRangeAngle& rhs) throw (DivideByZeroError, RangeError);

  };


  // =============================
  // ===== Declination Angle =====
  // =============================


  class Declination : public LimitedRangeAngle {

  public:

    // ----- ctor and dtor -----

    explicit Declination(const double& a_deg = 0.0,
			 const double& a_min = 0.0,
			 const double& a_sec = 0.0,
			 const double& a_minimum = -90.0,
			 const double& a_maximum =  90.0) throw (RangeError);

    explicit Declination(const std::string& a_deg, // The ambiguity is in the box.
			 const std::string& a_min = "0",
			 const std::string& a_sec = "0",
			 const double& a_minimum = -90.0,
			 const double& a_maximum =  90.0) throw (RangeError);

    virtual ~Declination() {};

    // ----- inplace operators -----

    virtual Declination& operator+=(const Declination& rhs) throw (RangeError);
    virtual Declination& operator-=(const Declination& rhs) throw (RangeError);

    virtual Declination& operator*=(const Declination& rhs) throw (RangeError);
    virtual Declination& operator/=(const Declination& rhs) throw (DivideByZeroError, RangeError);

  };

  // ====================
  // ===== Latitude =====
  // ====================

  typedef Declination Latitude;

  // =====================
  // ===== Longitude =====
  // =====================

  class Longitude : public LimitedRangeAngle {

  public:

    // ----- ctor and dtor -----

    explicit Longitude(const double& a_deg = 0.0,
		       const double& a_min = 0.0,
		       const double& a_sec = 0.0,
		       const double& a_minimum = -180.0,
		       const double& a_maximum =  180.0) throw (RangeError);

    explicit Longitude(const std::string& a_deg, // The ambiguity is in the box.
		       const std::string& a_min = "0",
		       const std::string& a_sec = "0",
		       const double& a_minimum = -180.0,
		       const double& a_maximum =  180.0) throw (RangeError);

    virtual ~Longitude() {};

  };

  // ===========================
  // ===== Right Ascension =====
  // ===========================

  class RA : public LimitedRangeAngle {

  public:

    // ----- ctor and dtor -----

    explicit RA(const double& a_hour = 0.0,
		const double& a_min = 0.0,
		const double& a_sec = 0.0,
		const double& a_minimum =  0.0,
		const double& a_maximum = 24.0) throw (RangeError);

    explicit RA(const std::string& a_hour, // The ambiguity is in the box.
		const std::string& a_min = "0",
		const std::string& a_sec = "0",
		const double& a_minimum =  0.0,
		const double& a_maximum = 24.0) throw (RangeError);

    virtual ~RA() {};

  };



// ================================
// ===== operator<< functions =====
// ================================

// operator<< for declination, latitude, longitude

// inline for boost templates

inline std::ostream& operator<< (std::ostream& os, const Angles::Angle& a) {

  bool isNegative(false);

  if (a.value() < 0)
    isNegative = true;

  double degrees = fabs(a.value());
  double minutes = 60 * (degrees - floor(degrees));
  double seconds = 60 * (minutes - floor(minutes));

  if (isNegative)
    degrees = -1 * floor(degrees);
  else
    degrees = floor(degrees);

  os << degrees << "* " << floor(minutes) << "\' " << seconds << "\"";

  return os;
}

// operator<< right ascension

inline std::ostream& operator<< (std::ostream& os, const Angles::RA& a) {
  // constructor ensures a is not negative.
  double hours = fabs(a.value());
  double minutes = 60 * (hours - floor(hours));
  double seconds = 60 * (minutes - floor(minutes));

  os << floor(hours) << " hr " << floor(minutes) << "\' " << seconds << "\"";

  return os;
}


} // end namespace Angles

