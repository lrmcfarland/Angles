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

  TEST(Angle, Degree2Radians) {
    double a = Angles::Angle::deg2rad(45);
    EXPECT_DOUBLE_EQ(0.78539816339744828, a);
  }

  TEST(Angle, Radian2Degrees) {
    double a = Angles::Angle::rad2deg(0.78539816339744828);
    EXPECT_DOUBLE_EQ(45, a);
  }

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

  // constructors (and implicitly radians() accessor)

  TEST(Angle, ConstructorDefault) {
    Angles::Angle a;
    EXPECT_EQ(0, a.radians());
  }

  // positive angles in limited range tests
  TEST(Angle, ConstructorDeg) {
    Angles::Angle a(-45);
    EXPECT_EQ(Angles::Angle::deg2rad(-45), a.radians());
  }

  TEST(Angle, ConstructorDegStr) {
    Angles::Angle a("-45");
    EXPECT_EQ(Angles::Angle::deg2rad(-45), a.radians());
  }

  TEST(Angle, ConstructorDegMin) {
    Angles::Angle a(0, -60);
    EXPECT_EQ(Angles::Angle::deg2rad(-1), a.radians());
  }

  TEST(Angle, ConstructorDegMinStr) {
    Angles::Angle a("0", "-60");
    EXPECT_EQ(Angles::Angle::deg2rad(-1), a.radians());
  }

  TEST(Angle, ConstructorDegMinSec) {
    Angles::Angle a(0, 0, -1);
    EXPECT_DOUBLE_EQ(Angles::Angle::deg2rad(-1/3600.0), a.radians());
  }

  TEST(Angle, ConstructorDegMinSecStr) {
    Angles::Angle a("0", "0", "-6.1");
    EXPECT_DOUBLE_EQ(Angles::Angle::deg2rad(-6.1/3600.0), a.radians());
  }


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

  TEST(Angle, UnitaryMinus) {
    Angles::Angle a;
    Angles::Angle b(-45);
    a = -b;
    EXPECT_DOUBLE_EQ(45, a.value());
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

  // multiply

  TEST(Angle, InplaceMultiplyDouble) {
    Angles::Angle a(45);
    double b(2);
    a *= b;
    EXPECT_DOUBLE_EQ(90, a.value());
  }

  TEST(Angle, MultiplyAngleByDouble) {
    Angles::Angle a(45);
    double b(2);
    Angles::Angle c;
    c = a * b;
    EXPECT_DOUBLE_EQ(90, c.value());
  }

  TEST(Angle, MultiplyDoubleByAngle) {
    Angles::Angle a(45);
    double b(2);
    Angles::Angle c;
    c = b * a;
    EXPECT_DOUBLE_EQ(90, c.value());
  }


  // divide
  TEST(Angle, InplaceDivideDouble) {
    Angles::Angle a(90);
    double b(2);
    a /= b;
    EXPECT_DOUBLE_EQ(45, a.value());
  }

  TEST(Angle, InplaceDivideByZeroError) {
    Angles::Angle a(45);
    EXPECT_THROW(a /= 0, Angles::Error);
  }

  TEST(Angle, InplaceDivideByZeroErrorStr) {
    try {
      Angles::Angle a(15); a /= 0;
    } catch (Angles::Error& err) {
      EXPECT_STREQ(err.what(), "division by zero is undefined");
    }
  }

  TEST(Angle, DivideAngleByDouble) {
    Angles::Angle a(90);
    double b(2);
    Angles::Angle c;
    c = a / b;
    EXPECT_DOUBLE_EQ(45, c.value());
  }

  TEST(Angle, DivideDoubleByAngle) {
    Angles::Angle a(2);
    double b(90);
    Angles::Angle c;
    c = b / a;
    EXPECT_DOUBLE_EQ(45, c.value());
  }

  TEST(Angle, DivideDoubleByZeroAngleError) {
    Angles::Angle a;
    double b(90);
    EXPECT_THROW(b/a, Angles::Error);
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

  TEST(LimitedRangeAngle, OutputOperator1) {
    Angles::LimitedRangeAngle a(23, 26, 12.1);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("23* 26' 12.1\"", out.str().c_str());
  }

  // constructors (and implicitly radians() accessor)

  TEST(LimitedRangeAngle, ConstructorDefault) {
    Angles::LimitedRangeAngle a;
    EXPECT_EQ(0, a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDeg) {
    Angles::LimitedRangeAngle a(45);
    EXPECT_EQ(Angles::Angle::deg2rad(45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegStr) {
    Angles::LimitedRangeAngle a("45");
    EXPECT_EQ(Angles::Angle::deg2rad(45), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMin) {
    Angles::LimitedRangeAngle a(0, 60);
    EXPECT_EQ(Angles::Angle::deg2rad(1), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMinStr) {
    Angles::LimitedRangeAngle a("0", "60");
    EXPECT_EQ(Angles::Angle::deg2rad(1), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMinSec) {
    Angles::LimitedRangeAngle a(0, 0, 1);
    EXPECT_DOUBLE_EQ(Angles::Angle::deg2rad(1/3600.0), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorDegMinSecStr) {
    Angles::LimitedRangeAngle a("0", "0", "6.1");
    EXPECT_DOUBLE_EQ(Angles::Angle::deg2rad(6.1/3600.0), a.radians());
  }

  TEST(LimitedRangeAngle, ConstructorCopy) {
    Angles::LimitedRangeAngle a(1, 2, 3);
    Angles::LimitedRangeAngle b(a);
    EXPECT_EQ(a, b);
  }

  TEST(LimitedRangeAngle, ConstructorAssign) {
    Angles::LimitedRangeAngle a(1, 2, 3);
    Angles::LimitedRangeAngle b;
    b = a;
    EXPECT_EQ(a, b);
  }

  TEST(LimitedRangeAngle, OperatorEQ_1) {
    Angles::LimitedRangeAngle a(1, 2, 3);
    Angles::LimitedRangeAngle b(a);
    EXPECT_TRUE(a == b);
  }

  TEST(LimitedRangeAngle, OperatorEQ_2) {
    Angles::LimitedRangeAngle a(1, 2, 3);
    Angles::LimitedRangeAngle b(4, 5, 6);
    EXPECT_TRUE(a != b);
  }

  TEST(LimitedRangeAngle, OperatorNE_1) {
    Angles::LimitedRangeAngle a(1, 2, 3);
    Angles::LimitedRangeAngle b(a);
    EXPECT_FALSE(a != b);
  }

  TEST(LimitedRangeAngle, OperatorNE_2) {
    Angles::LimitedRangeAngle a(1, 2, 3);
    Angles::LimitedRangeAngle b(4, 2, 3);
    EXPECT_TRUE(a != b);
  }


  TEST(LimitedRangeAngle, OutOfRangeError0) {
    EXPECT_NO_THROW(Angles::LimitedRangeAngle(0));
  }

  TEST(LimitedRangeAngle, OutOfRangeError1) {
    EXPECT_THROW(Angles::LimitedRangeAngle("-45"), Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeError2) {
    EXPECT_THROW(Angles::LimitedRangeAngle(361), Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeError3) {
    EXPECT_NO_THROW(Angles::LimitedRangeAngle("360"));
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorAdd) {
    Angles::LimitedRangeAngle a(345);
    Angles::LimitedRangeAngle b(345);
    EXPECT_THROW(a + b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorInplaceAdd) {
    Angles::LimitedRangeAngle a(345);
    Angles::LimitedRangeAngle b(345);
    EXPECT_THROW(a += b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorSubtract) {
    Angles::LimitedRangeAngle a(0);
    Angles::LimitedRangeAngle b(345);
    EXPECT_THROW(a - b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorInplaceSubtract) {
    Angles::LimitedRangeAngle a(0);
    Angles::LimitedRangeAngle b(345);
    EXPECT_THROW(a -= b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorMultiply) {
    Angles::LimitedRangeAngle a(90);
    EXPECT_THROW(5*a, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorDivide1) {
    Angles::LimitedRangeAngle a(90);
    EXPECT_THROW(a/0.0, Angles::Error);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorDivide2) {
    // expects LimitedRangeAngle constructor to declare it throws a RangeError
    Angles::LimitedRangeAngle a(90);
    EXPECT_THROW(a/0.01, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, OutOfRangeErrorDivide3) {
    Angles::LimitedRangeAngle a(90);
    EXPECT_THROW(a /= 0.01, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, MismatchRangeError1) {
    Angles::LimitedRangeAngle a(90, 0, 0, 0, 360);
    Angles::LimitedRangeAngle b(90, 0, 0, -90, 90);
    EXPECT_THROW(a + b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, MismatchRangeError2) {
    Angles::LimitedRangeAngle a(90, 0, 0, 0, 360);
    Angles::LimitedRangeAngle b(90, 0, 0, -90, 90);
    EXPECT_THROW(a += b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, MismatchRangeError3) {
    Angles::LimitedRangeAngle a(90, 0, 0, 0, 360);
    Angles::LimitedRangeAngle b(90, 0, 0, -90, 90);
    EXPECT_THROW(a - b, Angles::RangeError);
  }

  TEST(LimitedRangeAngle, MismatchRangeError4) {
    Angles::LimitedRangeAngle a(90, 0, 0, 0, 360);
    Angles::LimitedRangeAngle b(90, 0, 0, -90, 90);
    EXPECT_THROW(a -= b, Angles::RangeError);
  }

  // -----------------------
  // ----- Declination -----
  // -----------------------

  TEST(Declination, OutputOperator1) {
    Angles::Declination a(-23, 26, 12.1);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("-23* 26' 12.1\"", out.str().c_str());
  }

  // constructors (and implicitly radians() accessor)

  TEST(Declination, ConstructorDefault) {
    Angles::Declination a;
    EXPECT_EQ(0, a.radians());
  }

  TEST(Declination, ConstructorDeg) {
    Angles::Declination a(45);
    EXPECT_EQ(Angles::Angle::deg2rad(45), a.radians());
  }

  TEST(Declination, ConstructorDegStr) {
    Angles::Declination a("45");
    EXPECT_EQ(Angles::Angle::deg2rad(45), a.radians());
  }


  TEST(Declination, OutOfRangeError0) {
    EXPECT_NO_THROW(Angles::Declination(-30));
  }

  TEST(Declination, OutOfRangeError1) {
    EXPECT_THROW(Angles::Declination("-100"), Angles::RangeError);
  }

  TEST(Declination, OutOfRangeError2) {
    EXPECT_THROW(Angles::Declination(90, 1), Angles::RangeError);
  }

  TEST(Declination, OutOfRangeError3) {
    EXPECT_THROW(Angles::Declination("90", "1"), Angles::RangeError);
  }

  TEST(Declination, OutOfRangeError4) {
    EXPECT_THROW(Angles::Declination("-90", "1"), Angles::RangeError);
  }

  TEST(Declination, OutOfRangeErrorAdd) {
    Angles::Declination a(50);
    Angles::Declination b(45);
    EXPECT_THROW(a + b, Angles::RangeError);
  }

  TEST(Declination, OutOfRangeErrorInplaceAdd) {
    Angles::Declination a(50);
    Angles::Declination b(45);
    EXPECT_THROW(a += b, Angles::RangeError);
  }

  TEST(Declination, OutOfRangeErrorSubtract) {
    Angles::Declination a(-90);
    Angles::Declination b(1);
    EXPECT_THROW(a - b, Angles::RangeError);
  }

  TEST(Declination, OutOfRangeErrorInplaceSubtract) {
    Angles::Declination a(-90);
    Angles::Declination b(1);
    EXPECT_THROW(a -= b, Angles::RangeError);
  }


  TEST(Declination, OutOfRangeErrorMultiply) {
    Angles::Declination a(45);
    double b(5);
    EXPECT_THROW(a * b, Angles::RangeError);
  }

  TEST(Declination, OutOfRangeErrorInplaceMultiply) {
    Angles::Declination a(45);
    double b(5);
    EXPECT_THROW(a *= b, Angles::RangeError);
  }


  TEST(Declination, OutOfRangeErrorDivide1) {
    Angles::Declination a(90);
    EXPECT_THROW(a/0.0, Angles::Error);
  }

  TEST(Declination, OutOfRangeErrorDivide2) {
    // expects Declination constructor to declare it throws a RangeError
    Angles::Declination a(90);
    EXPECT_THROW(a/0.01, Angles::RangeError);
  }

  TEST(Declination, OutOfRangeErrorDivide3) {
    Angles::Declination a(90);
    EXPECT_THROW(a /= 0.01, Angles::RangeError);
  }

  // --------------------
  // ----- Latitude -----
  // --------------------

  TEST(Latitude, OutputOperator1) {
    Angles::Latitude a(23, 26, 12.1);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("23* 26' 12.1\"", out.str().c_str());
  }

  // constructors (and implicitly radians() accessor)

  TEST(Latitude, ConstructorDefault) {
    Angles::Latitude a;
    EXPECT_EQ(0, a.radians());
  }


  // ---------------------
  // ----- Longitude -----
  // ---------------------

  TEST(Longitude, OutputOperator1) {
    Angles::Longitude a(23, 26, 12.1);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("23* 26' 12.1\"", out.str().c_str());
  }

  // constructors (and implicitly radians() accessor)

  TEST(Longitude, ConstructorDefault) {
    Angles::Longitude a;
    EXPECT_EQ(0, a.radians());
  }


  TEST(Longitude, OutOfRangeError1) {
    EXPECT_THROW(Angles::Longitude("-190"), Angles::RangeError);
  }

  TEST(Longitude, OutOfRangeError2) {
    EXPECT_THROW(Angles::Longitude(190, 1), Angles::RangeError);
  }


  // ---------------------------
  // ----- Right Ascension -----
  // ---------------------------

  TEST(RightAscension, OutputOperator1) {
    Angles::RA a(23, 26, 12.1);
    std::stringstream out;
    out << a;
    EXPECT_STREQ("23 hr 26' 12.1\"", out.str().c_str());
  }

  TEST(RightAscension, OutOfRangeError1) {
    EXPECT_THROW(Angles::RA("-10"), Angles::RangeError);
  }

  TEST(RightAscension, OutOfRangeError2) {
    EXPECT_THROW(Angles::RA(24, 0, 0.1), Angles::RangeError);
  }


  // add
  TEST(RightAscension, InplaceAddAngle) {
    Angles::RA a(11, 59);
    Angles::RA b("0", "0", "60");
    a += b;
    EXPECT_DOUBLE_EQ(12, a.value());
  }

  TEST(RightAscension, OutOfRangeErrorInplaceAdd) {
    Angles::RA a(24, 0, 0);
    Angles::RA b(0, 0, 0.01);
    EXPECT_THROW(a += b, Angles::RangeError);
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



} // end anonymous namespace



// ==================
// ===== main() =====
// ==================

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
