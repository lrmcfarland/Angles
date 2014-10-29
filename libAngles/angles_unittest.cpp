// ================================================================
// Filename:    angles_unittest.cpp
// Description: This is the gtest unittest of the angles library.
//
// Author:      L.R. McFarland, lrm@starbug.com
// Created:     2014 Jun 19
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

#include <angles.h>
#include <utils.h>

#include <sstream>

#include <gtest/gtest.h>

namespace {


  // -----------------
  // ----- Angle -----
  // -----------------

  // ----- static methods -----

  TEST(Angle, Degree2Radians) {
    double a = Angles::Angle::deg2rad(45);
    EXPECT_DOUBLE_EQ(0.78539816339744828, a);
  }

  TEST(Angle, Radian2Degrees) {
    double a = Angles::Angle::rad2deg(0.78539816339744828);
    EXPECT_DOUBLE_EQ(45, a);
  }

  // constructors (and implicitly radians() accessor)

  TEST(Angle, CopyConstructor) {
    Angles::Angle a;
    a.value(1);
    Angles::Angle b(a);
    EXPECT_TRUE(a == b);
  }

  TEST(Angle, CopyAssign) {
    Angles::Angle a;
    a.value(1);
    Angles::Angle b = a;
    EXPECT_TRUE(a == b);
  }

  TEST(Angle, DefaultConstructor) {
    Angles::Angle a;
    EXPECT_EQ(0, a.radians());
  }


  TEST(Angle, ConstructorDeg) {
    Angles::Angle a(-45);
    EXPECT_EQ(Angles::Angle::deg2rad(-45), a.radians());
  }

  TEST(Angle, ConstructorDegFromStr) {
    Angles::Angle a("-45");
    EXPECT_EQ(Angles::Angle::deg2rad(-45), a.radians());
  }

  TEST(Angle, ConstructorDegMin) {
    Angles::Angle a(0, -60);
    EXPECT_EQ(Angles::Angle::deg2rad(-1), a.radians());
  }

  TEST(Angle, ConstructorDegMinFromStr) {
    Angles::Angle a("0", "-60");
    EXPECT_EQ(Angles::Angle::deg2rad(-1), a.radians());
  }

  TEST(Angle, ConstructorDegMinSec) {
    Angles::Angle a(0, 0, -1);
    EXPECT_DOUBLE_EQ(Angles::Angle::deg2rad(-1/3600.0), a.radians());
  }

  TEST(Angle, ConstructorDegMinSecFromStr) {
    Angles::Angle a("0", "0", "-6.1");
    EXPECT_DOUBLE_EQ(Angles::Angle::deg2rad(-6.1/3600.0), a.radians());
  }

  // TODO correct behavior?
  TEST(Angle, MixedSignX) {
    Angles::Angle a(-1, 2);
    Angles::Angle b(1, -2);
    EXPECT_FALSE(a.value() == b.value());
  }

  TEST(Angle, MixedSign1) {
    Angles::Angle a(-1, 2);
    Angles::Angle b(-1, -2);
    EXPECT_DOUBLE_EQ(a.value(), b.value());
  }

  TEST(Angle, MixedSign2) {
    Angles::Angle a(-1, 2, 3);
    Angles::Angle b(-1, -2, -3);
    EXPECT_DOUBLE_EQ(a.value(), b.value());
  }

  TEST(Angle, MixedSign3) {
    Angles::Angle a(1, 2, 3);
    Angles::Angle b(1, -2, -3);
    EXPECT_DOUBLE_EQ(a.value(), b.value());
  }

  // accessors

  TEST(Angle, Accessors) {
    Angles::Angle a(-45);
    EXPECT_EQ(-45, a.value());
    EXPECT_EQ(-45, a.getValue());
    EXPECT_EQ(Angles::Angle::deg2rad(-45), a.radians());
    EXPECT_EQ(Angles::Angle::deg2rad(-45), a.getRadians());
  }

  // ----- booleans -----

  TEST(Angle, Equivalence1) {
    Angles::Angle a;
    Angles::Angle b;
    a.value(1);
    b.value(1);
    EXPECT_TRUE(a == b);
  }

  TEST(Angle, Equivalence2) {
    Angles::Angle a;
    Angles::Angle b;
    a.value(1);
    b.value(-1);
    EXPECT_FALSE(a == b);
  }

  TEST(Angle, NotEquivalence1) {
    Angles::Angle a(1);
    Angles::Angle b(1);
    EXPECT_FALSE(a != b);
  }

  TEST(Angle, NotEquivalence2) {
    Angles::Angle a(1);
    Angles::Angle b(-1);
    EXPECT_TRUE(a != b);
  }

  TEST(Angle, LessThan1) {
    Angles::Angle a(10);
    Angles::Angle b(20);
    EXPECT_TRUE(a < b);
  }

  TEST(Angle, LessThan2) {
    Angles::Angle a(10);
    Angles::Angle b(20);
    EXPECT_FALSE(b < a);
  }

  TEST(Angle, LessThanOrEqualTo1) {
    Angles::Angle a(25.1);
    Angles::Angle b(25.1);
    EXPECT_TRUE(a <= b);
  }

  TEST(Angle, LessThanOrEqualTo2) {
    Angles::Angle a(10.5);
    Angles::Angle b(10.6);
    EXPECT_FALSE(b <= a);
  }

  TEST(Angle, GreaterThan1) {
    Angles::Angle a(20);
    Angles::Angle b(10);
    EXPECT_TRUE(a > b);
  }

  TEST(Angle, GreaterThan2) {
    Angles::Angle a(20);
    Angles::Angle b(10);
    EXPECT_FALSE(b > a);
  }

  TEST(Angle, GreaterThanOrEqualTo1) {
    Angles::Angle a(25.1);
    Angles::Angle b(25.1);
    EXPECT_TRUE(a >= b);
  }

  TEST(Angle, GreaterThanOrEqualTo2) {
    Angles::Angle a(10.6);
    Angles::Angle b(10.5);
    EXPECT_FALSE(b >= a);
  }

  // operators

  // add
  TEST(Angle, InplaceAddAngle) {
    Angles::Angle a(45);
    Angles::Angle b(45);
    a += b;
    EXPECT_DOUBLE_EQ(90, a.value());
  }

  TEST(Angle, InplaceAddAngleNeg) {
    Angles::Angle a(45);
    Angles::Angle b(-45);
    a += b;
    EXPECT_DOUBLE_EQ(0, a.value());
  }

  TEST(Angle, AnglePlusAnglePos) {
    Angles::Angle a(44.5);
    Angles::Angle b(44.5);
    Angles::Angle c;
    c = a + b;
    EXPECT_DOUBLE_EQ(89, c.value());
  }

  TEST(Angle, AnglePlusAngleNeg) {
    Angles::Angle a(45);
    Angles::Angle b(-45);
    Angles::Angle c;
    c = a + b;
    EXPECT_DOUBLE_EQ(0, c.value());
  }

  // subtract
  TEST(Angle, InplaceSubtractAnglePos) {
    Angles::Angle a(45);
    Angles::Angle b(40);
    a -= b;
    EXPECT_DOUBLE_EQ(5, a.value());
  }

  TEST(Angle, InplaceSubtractAngleNeg) {
    Angles::Angle a(45);
    Angles::Angle b(-45);
    a -= b;
    EXPECT_DOUBLE_EQ(90, a.value());
  }

  TEST(Angle, AngleMinusAnglePos) {
    Angles::Angle a(45);
    Angles::Angle b(45);
    Angles::Angle c;
    c = a - b;
    EXPECT_DOUBLE_EQ(0, c.value());
  }

  TEST(Angle, AngleMinusAngleNeg) {
    Angles::Angle a(45);
    Angles::Angle b(-45);
    Angles::Angle c;
    c = a - b;
    EXPECT_DOUBLE_EQ(90, c.value());
  }

  // unitary minus
  TEST(Angle, UnitaryMinus) {
    Angles::Angle a;
    Angles::Angle b(-45);
    a = -b;
    EXPECT_DOUBLE_EQ(45, a.value());
  }

  // multiply

  TEST(Angle, InplaceMultiply) {
    Angles::Angle a(45);
    Angles::Angle b(2);
    a *= b;
    EXPECT_DOUBLE_EQ(90, a.value());
  }

  TEST(Angle, MultiplyAngleByAngle) {
    Angles::Angle a(45);
    Angles::Angle b(2);
    Angles::Angle c;
    c = a * b;
    EXPECT_DOUBLE_EQ(90, c.value());
  }

  // divide

  TEST(Angle, InplaceDivide) {
    Angles::Angle a(90);
    Angles::Angle b(2);
    a /= b;
    EXPECT_DOUBLE_EQ(45, a.value());
  }

  TEST(Angle, InplaceDivideByZeroError) {
    Angles::Angle a(45);
    Angles::Angle b(0);
    EXPECT_THROW(a /= b, Angles::DivideByZeroError);
  }

  TEST(Angle, InplaceDivideByZeroErrorMsg) {
    try {
      Angles::Angle a(15);
      Angles::Angle b;
      a /= b;
    } catch (Angles::DivideByZeroError& err) {
      EXPECT_STREQ(err.what(), "division by zero is undefined");
    }
  }

  TEST(Angle, DivideAngleByAngle) {
    Angles::Angle a(90);
    Angles::Angle b(2);
    Angles::Angle c;
    c = a / b;
    EXPECT_DOUBLE_EQ(45, c.value());
  }


  // operator<<

  TEST(Angle, operatorStdOut) {
    Angles::Angle a(44, 32, 15.4);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("44* 32' 15.4\"", out.str().c_str());
  }


  // 360 and beyond

  TEST(Angle, Stdout360) {
    Angles::Angle a(360);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("360* 0' 0\"", out.str().c_str());
  }

  TEST(Angle, Stdout361) {
    Angles::Angle a(361);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("361* 0' 0\"", out.str().c_str());
  }

  TEST(Angle, RoundingIssuesBeyond360) {
    // had rounding issues when storing value in radians.
    Angles::Angle a(45+360);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("405* 0' 0\"", out.str().c_str());
  }

  // TODO fix this Angle(45 * 10).normalize() != 180
  TEST(Angle, Normalize) {
    Angles::Angle a(45 + 360);
    a.normalize();
    EXPECT_NEAR(45, a.value(), 1e-15);
  }


  // -----------------------------
  // ----- LimitedRangeAngle -----
  // -----------------------------

  // ----- static methods -----

  TEST(LimitedRangeAngle, Degree2Radians) {
    double a = Angles::LimitedRangeAngle::deg2rad(45);
    EXPECT_DOUBLE_EQ(0.78539816339744828, a);
  }

  TEST(LimitedRangeAngle, Radian2Degrees) {
    double a = Angles::LimitedRangeAngle::rad2deg(0.78539816339744828);
    EXPECT_DOUBLE_EQ(45, a);
  }

  // ----- constructors -----

  TEST(LimitedRangeAngle, CopyConstructor) {
    Angles::LimitedRangeAngle a(30);
    Angles::LimitedRangeAngle b(a);
    EXPECT_EQ(a.value(), b.value());
  }
  
  TEST(LimitedRangeAngle, CopyAssign) {
    Angles::LimitedRangeAngle a(-35);
    Angles::LimitedRangeAngle b;
    b = a;
    EXPECT_EQ(a.value(), b.value());
  }

  TEST(LimitedRangeAngle, DefaultConstructor) {
    Angles::LimitedRangeAngle a;
    EXPECT_EQ(0, a.value());
  }

  TEST(LimitedRangeAngle, ConstructorDeg) {
    Angles::LimitedRangeAngle a(45);
    EXPECT_EQ(45, a.value());
    EXPECT_EQ(Angles::LimitedRangeAngle::deg2rad(45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegFromString) {
    Angles::LimitedRangeAngle a("-45.0");
    EXPECT_EQ(-45, a.value());
    EXPECT_EQ(Angles::LimitedRangeAngle::deg2rad(-45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMin) {
    Angles::LimitedRangeAngle a(44, 60);
    EXPECT_EQ(45, a.value());
    EXPECT_EQ(Angles::LimitedRangeAngle::deg2rad(45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMinFromString) {
    Angles::LimitedRangeAngle a("-44.0", "60");
    EXPECT_EQ(-45, a.value());
    EXPECT_EQ(Angles::LimitedRangeAngle::deg2rad(-45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMinSec) {
    Angles::LimitedRangeAngle a(44, 59, 60);
    EXPECT_EQ(45, a.value());
    EXPECT_EQ(Angles::LimitedRangeAngle::deg2rad(45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMinSecFromString) {
    Angles::LimitedRangeAngle a("-44.0", "59", "60");
    EXPECT_EQ(-45, a.value());
    EXPECT_EQ(Angles::LimitedRangeAngle::deg2rad(-45), a.radians());
  }

  // range errors

  TEST(LimitedRangeAngle, OutOfRangeError_360) {
    EXPECT_NO_THROW(Angles::LimitedRangeAngle(-360));
  }

  TEST(LimitedRangeAngle, OutOfRangeError360) {
    EXPECT_NO_THROW(Angles::LimitedRangeAngle(360));
  }

  TEST(LimitedRangeAngle, OutOfRangeError_361) {
    EXPECT_THROW(Angles::LimitedRangeAngle(-361), Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeError361) {
    EXPECT_THROW(Angles::LimitedRangeAngle(361), Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeError_360Str) {
    EXPECT_NO_THROW(Angles::LimitedRangeAngle("-360"));
  }

  TEST(LimitedRangeAngle, OutOfRangeError360Str) {
    EXPECT_NO_THROW(Angles::LimitedRangeAngle("360"));
  }

  TEST(LimitedRangeAngle, OutOfRangeError_361Str) {
    EXPECT_THROW(Angles::LimitedRangeAngle("-361"), Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeError361Str) {
    EXPECT_THROW(Angles::LimitedRangeAngle("361"), Angles::RangeError);
  }


  // accessors

  TEST(LimitedRangeAngle, min_accessors) {
    Angles::LimitedRangeAngle a;
    EXPECT_EQ(-360, a.minimum());
    EXPECT_EQ(-360, a.getMinimum());
  }

  TEST(LimitedRangeAngle, max_accessors) {
    Angles::LimitedRangeAngle a;
    EXPECT_EQ(360, a.maximum());
    EXPECT_EQ(360, a.getMaximum());
  }

  TEST(LimitedRangeAngle, value_accessors) {
    Angles::LimitedRangeAngle a;

    a.value(45);
    EXPECT_EQ(45, a.value());

    a.setValue(-30);
    EXPECT_EQ(-30, a.getValue());
  }

  TEST(LimitedRangeAngle, radians_accessors) {
    Angles::LimitedRangeAngle a;

    a.radians(1.4);
    EXPECT_EQ(1.4, a.radians());

    a.setRadians(-1.2);
    EXPECT_DOUBLE_EQ(-1.2, a.getRadians());

  }

  TEST(LimitedRangeAngle, value_ccessor_error) {
    Angles::LimitedRangeAngle a;
    EXPECT_THROW(a.setValue(361), Angles::RangeError);
  }

  TEST(LimitedRangeAngle, radians_accessor_error) {
    Angles::LimitedRangeAngle a;
    EXPECT_THROW(a.setRadians(361), Angles::RangeError);
  }


  // ----- booleans -----


  TEST(LimitedRangeAngle, Equivalence1) {
    Angles::LimitedRangeAngle a;
    Angles::LimitedRangeAngle b;
    a.value(1);
    b.value(1);
    EXPECT_TRUE(a == b);
  }

  TEST(LimitedRangeAngle, Equivalence2) {
    Angles::LimitedRangeAngle a;
    Angles::LimitedRangeAngle b;
    a.value(1);
    b.value(-1);
    EXPECT_FALSE(a == b);
  }

  TEST(LimitedRangeAngle, NotEquivalence1) {
    Angles::LimitedRangeAngle a(1);
    Angles::LimitedRangeAngle b(1);
    EXPECT_FALSE(a != b);
  }

  TEST(LimitedRangeAngle, NotEquivalence2) {
    Angles::LimitedRangeAngle a(1);
    Angles::LimitedRangeAngle b(-1);
    EXPECT_TRUE(a != b);
  }

  TEST(LimitedRangeAngle, LessThan1) {
    Angles::LimitedRangeAngle a(10);
    Angles::LimitedRangeAngle b(20);
    EXPECT_TRUE(a < b);
  }

  TEST(LimitedRangeAngle, LessThan2) {
    Angles::LimitedRangeAngle a(10);
    Angles::LimitedRangeAngle b(20);
    EXPECT_FALSE(b < a);
  }

  TEST(LimitedRangeAngle, LessThanOrEqualTo1) {
    Angles::LimitedRangeAngle a(25.1);
    Angles::LimitedRangeAngle b(25.1);
    EXPECT_TRUE(a <= b);
  }

  TEST(LimitedRangeAngle, LessThanOrEqualTo2) {
    Angles::LimitedRangeAngle a(10.5);
    Angles::LimitedRangeAngle b(10.6);
    EXPECT_FALSE(b <= a);
  }

  TEST(LimitedRangeAngle, GreaterThan1) {
    Angles::LimitedRangeAngle a(20);
    Angles::LimitedRangeAngle b(10);
    EXPECT_TRUE(a > b);
  }

  TEST(LimitedRangeAngle, GreaterThan2) {
    Angles::LimitedRangeAngle a(20);
    Angles::LimitedRangeAngle b(10);
    EXPECT_FALSE(b > a);
  }

  TEST(LimitedRangeAngle, GreaterThanOrEqualTo1) {
    Angles::LimitedRangeAngle a(25.1);
    Angles::LimitedRangeAngle b(25.1);
    EXPECT_TRUE(a >= b);
  }

  TEST(LimitedRangeAngle, GreaterThanOrEqualTo2) {
    Angles::LimitedRangeAngle a(10.6);
    Angles::LimitedRangeAngle b(10.5);
    EXPECT_FALSE(b >= a);
  }

  // arithmetic operators

  // add
  TEST(LimitedRangeAngle, InplaceAddAngle) {
    Angles::LimitedRangeAngle a(45);
    Angles::LimitedRangeAngle b(45);
    a += b;
    EXPECT_DOUBLE_EQ(90, a.value());
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorInplaceAdd) {
    Angles::LimitedRangeAngle a(350);
    Angles::LimitedRangeAngle b(45);
    EXPECT_THROW(a += b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, AnglePlusAngle) {
    Angles::LimitedRangeAngle a(44.5);
    Angles::LimitedRangeAngle b(44.5);
    Angles::LimitedRangeAngle c;
    c = a + b;
    EXPECT_DOUBLE_EQ(89, c.value());
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorAdd) {
    Angles::LimitedRangeAngle a(350);
    Angles::LimitedRangeAngle b(45);
    EXPECT_THROW(a + b, Angles::RangeError);
  }

  // subtract

  TEST(LimitedRangeAngle, InplaceSubtractAngle) {
    Angles::LimitedRangeAngle a(45);
    Angles::LimitedRangeAngle b(10);
    a -= b;
    EXPECT_DOUBLE_EQ(35, a.value());
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorInplaceSubtract) {
    Angles::LimitedRangeAngle a(-360);
    Angles::LimitedRangeAngle b(1);
    EXPECT_THROW(a -= b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, AngleMinusAngle) {
    Angles::LimitedRangeAngle a(45);
    Angles::LimitedRangeAngle b(45);
    Angles::LimitedRangeAngle c;
    c = a - b;
    EXPECT_DOUBLE_EQ(0, c.value());
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorSubtract) {
    Angles::LimitedRangeAngle a(-360);
    Angles::LimitedRangeAngle b(1);
    EXPECT_THROW(a - b, Angles::RangeError);
  }

  // unitary minus

  TEST(LimitedRangeAngle, UnitaryMinus) {
    Angles::LimitedRangeAngle a;
    Angles::LimitedRangeAngle b(-45);
    a = -b;
    EXPECT_DOUBLE_EQ(45, a.value());
  }

  // multiply

  TEST(LimitedRangeAngle, OutOfRangeErrorMultiply) {
    Angles::LimitedRangeAngle a(45);
    Angles::LimitedRangeAngle b(9);
    EXPECT_THROW(a * b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorInplaceMultiply) {
    Angles::LimitedRangeAngle a(45);
    Angles::LimitedRangeAngle b(9);
    EXPECT_THROW(a *= b, Angles::RangeError);
  }

  // divide

  TEST(LimitedRangeAngle, InplaceDivide) {
    Angles::LimitedRangeAngle a(90);
    Angles::LimitedRangeAngle b(2);
    a /= b;
    EXPECT_DOUBLE_EQ(45, a.value());
  }

  TEST(LimitedRangeAngle, InplaceDivideByZeroError) {
    Angles::LimitedRangeAngle a(90);
    Angles::LimitedRangeAngle b(0);
    EXPECT_THROW(a /= b, Angles::DivideByZeroError);
  }

  TEST(LimitedRangeAngle, DivideAngleByAngle) {
    Angles::LimitedRangeAngle a(90);
    Angles::LimitedRangeAngle b(2);
    Angles::LimitedRangeAngle c;
    c = a / b;
    EXPECT_DOUBLE_EQ(45, c.value());
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorDivide1) {
    Angles::LimitedRangeAngle a(90);
    Angles::LimitedRangeAngle b(0);
    EXPECT_THROW(a/b, Angles::DivideByZeroError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorDivide2) {
    Angles::LimitedRangeAngle a(90);
    Angles::LimitedRangeAngle b(0.01);
    EXPECT_THROW(a/b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorDivide3) {
    Angles::LimitedRangeAngle a(90);
    Angles::LimitedRangeAngle b(0.01);
    EXPECT_THROW(a /= b, Angles::RangeError);
  }


  // -----------------
  // ----- Utils -----
  // -----------------

  // utils degrees2seconds sign syntax errors
  TEST(Utils, Degree2SecondsError1) {
    EXPECT_TRUE(Angles::degrees2seconds(45, 60, 0) == Angles::degrees2seconds(45, -60, 0));
  }

  TEST(Utils, Degree2SecondsError2) {
    EXPECT_TRUE(Angles::degrees2seconds(45, 59, 60) == Angles::degrees2seconds(45, 59, -60));
  }

  TEST(Utils, Degree2SecondsError3) {
    EXPECT_TRUE(Angles::degrees2seconds(0, 59, 60) == Angles::degrees2seconds(0, 59, -60));
  }

  TEST(Utils, Degree2SecondsError4) {
    EXPECT_TRUE(Angles::degrees2seconds(0, -59, 60) == Angles::degrees2seconds(0, -59, -60));
  }

  TEST(Utils, Degree2SecondsError5) {
    EXPECT_TRUE(Angles::degrees2seconds(-45, 59, 60) == Angles::degrees2seconds(-45, -59, 60));
  }

  TEST(Utils, Degree2SecondsError6) {
    EXPECT_TRUE(Angles::degrees2seconds(-45, 59, 60) == Angles::degrees2seconds(-45, 59, -60));
  }

  TEST(Utils, Degree2SecondsError7) {
    EXPECT_TRUE(Angles::degrees2seconds(-45, 59, 60) == Angles::degrees2seconds(-45, -59, -60));
  }



  // opeartor<<()

  TEST(LimitedRangeAngle, operatorStdOut) {
    Angles::LimitedRangeAngle a(44, 32, 15.4);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("44* 32' 15.4\"", out.str().c_str());
  }

  TEST(Declination, operatorStdOut) {
    Angles::Declination a(44, 32, 15.4);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("44* 32' 15.4\"", out.str().c_str());
  }

  TEST(Latitude, operatorStdOut) {
    Angles::Latitude a(-53, 42, 23.6);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("-53* 42' 23.6\"", out.str().c_str());
  }

  TEST(Longitude, operatorStdOut) {
    Angles::Longitude a(100, 17, 45.8);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("100* 17' 45.8\"", out.str().c_str());
  }

  TEST(RA, operatorStdOut) {
    Angles::RA a(16, 30, 15);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("16:30:15", out.str().c_str());
  }



} // end anonymous namespace



// ==================
// ===== main() =====
// ==================

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
