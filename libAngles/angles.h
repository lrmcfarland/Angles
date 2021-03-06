// ================================================================
// Filename:    angles.h
//
// Description: This is a declaration of an angles class and template,
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
		   const double& a_sec = 0.0);

    explicit Angle(const std::string& a_deg, // The ambiguity is in the box.
		   const std::string& a_min = "0",
		   const std::string& a_sec = "0");

    virtual ~Angle() {};

    inline Angle(const Angle& a);
    inline Angle& operator=(const Angle& rhs);

    // ----- accessors -----
    void          value(const double& a_value) {m_value = a_value;}
    const double& value() const                {return m_value;}

    void          setValue(const double& a_value) {m_value = a_value;}
    double        getValue() const                {return m_value;} // for boost

    void          radians(const double& a_value) {value(rad2deg(a_value));}
    double        radians() const                {return deg2rad(value());}

    void           setRadians(const double& a_value) {value(rad2deg(a_value));}
    double         getRadians() const                {return deg2rad(value());} // for boost

    // ----- boolean operators -----

    inline bool operator== (const Angle& rhs) const;
    inline bool operator!= (const Angle& rhs) const;

    inline bool operator< (const Angle& rhs) const;
    inline bool operator<= (const Angle& rhs) const;

    inline bool operator> (const Angle& rhs) const;
    inline bool operator>= (const Angle& rhs) const;

    // ----- in-place operators -----

    virtual Angle& operator+=(const Angle& rhs);
    virtual Angle& operator-=(const Angle& rhs);

    virtual Angle& operator*=(const Angle& rhs);
    virtual Angle& operator/=(const Angle& rhs) throw (DivideByZeroError);


    // ----- other methods -----
    virtual void normalize();  // TODO normalized -> return a new copy?

  private:

    double m_value; // degrees for declination, latitude, longitude, seconds for right ascension

  };

  // ----- inline implementations of angle methods -----

  // copy constructor
  inline Angle::Angle(const Angle& a) {
    m_value = a.value();
  }

  // copy assignment
  inline Angle& Angle::operator=(const Angle& rhs) {
    if (this == &rhs) return *this;
    m_value = rhs.value();
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

  Angle operator+ (const Angle& lhs, const Angle& rhs);
  Angle operator- (const Angle& lhs, const Angle& rhs);
  Angle operator- (const Angle& rhs); // unitary minus

  Angle operator* (const Angle& lhs, const Angle& rhs);
  Angle operator/ (const Angle& lhs, const Angle& rhs) throw (DivideByZeroError);

  
  // ==============================
  // ===== LimitedRangeAngles =====
  // ==============================


  template<int A_MINIMUM, int A_MAXIMUM>  // only ints can be non-type arguments
    class LRA {

  public:

    // angle unit convertors
    static double deg2rad(const double& deg) {return deg*M_PI/180.0;}
    static double rad2deg(const double& rad) {return rad*180.0/M_PI;}


    explicit LRA(const double& a_deg = 0.0,
		 const double& a_min = 0.0,
		 const double& a_sec = 0.0) throw (RangeError);

    explicit LRA(const std::string& a_deg, // The ambiguity is in the box.
		 const std::string& a_min = "0.0",
		 const std::string& a_sec = "0.0") throw (RangeError);

    LRA(const LRA& a);

    LRA& operator=(const LRA& rhs);

    ~LRA() {};


    // ----- accessors -----
    void          value(const double& a_value) {m_value = a_value;}
    const double& value() const                {return m_value;}

    // TODO: validate version in manual throws invalid exceptions
    void          setValue(const double& a_value) throw (RangeError); // not for manual
    double        getValue() const             {return m_value;} // for boost

    void          radians(const double& a_value) {value(rad2deg(a_value));}
    double        radians() const                {return deg2rad(value());}

    // TODO: validate version in manual throws invalid exceptions
    void          setRadians(const double& a_value) throw (RangeError) {setValue(rad2deg(a_value));} // for not manual
    double        getRadians() const             {return deg2rad(value());} // for boost

    const double& minimum() const {return m_minimum;}
    double        getMinimum() const {return m_minimum;} // for boost

    const double& maximum() const {return m_maximum;}
    double        getMaximum() const {return m_maximum;} // for boost

    // ----- boolean operators -----

    bool operator== (const LRA& rhs) const;
    bool operator!= (const LRA& rhs) const;

    bool operator< (const LRA& rhs) const;
    bool operator<= (const LRA& rhs) const;

    bool operator> (const LRA& rhs) const;
    bool operator>= (const LRA& rhs) const;


    // ----- in-place operators -----

    LRA& operator+=(const LRA& rhs) throw (RangeError);
    LRA& operator-=(const LRA& rhs) throw (RangeError);

    LRA& operator*=(const LRA& rhs) throw (RangeError);
    LRA& operator/=(const LRA& rhs) throw (DivideByZeroError, RangeError);

    // ----- helpers -----
    void validRange(const double& a_value) const throw (RangeError);
    bool isValidRange(const double& a_value) const;

  private:

    double m_value; // degrees for declination, latitude, longitude, seconds for right ascension

    double m_minimum;
    double m_maximum;

  };


  // ================================
  // ===== typedef-ed instances =====
  // ================================

  typedef LRA<-360, 360> LimitedRangeAngle;
  typedef LRA<-90, 90>   Declination;
  typedef LRA<-90, 90>   Latitude;
  typedef LRA<-180, 180> Longitude;
  typedef LRA<0, 24>     RA; // Right Ascension

  // =============================
  // ===== output operator<< =====
  // =============================

  void value2DMSString(const double& a_value, std::stringstream& a_string);
  void value2HMSString(const double& a_value, std::stringstream& a_string);

  std::ostream& operator<< (std::ostream& os, const Angles::Angle& a);
  std::ostream& operator<< (std::ostream& os, const Angles::LimitedRangeAngle& a);
  std::ostream& operator<< (std::ostream& os, const Angles::Declination& a);
  std::ostream& operator<< (std::ostream& os, const Angles::Longitude& a);
  std::ostream& operator<< (std::ostream& os, const Angles::RA& a);

} // end namespace Angles

#include <angles.hpp>

