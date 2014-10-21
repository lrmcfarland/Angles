#!/usr/bin/env python

"""Unit tests for space objects."""

import copy
import math
import random
import time
import unittest

import angles

class TestAngle(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = -720
        self.upper_range = 720

        self.lower_minute_range = -60
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_range)
        self.rm1 = random.uniform(self.lower_minute_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_minute_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_range)
        self.rm2 = random.uniform(self.lower_minute_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_minute_range, self.upper_minute_range)

    # static methods

    def test_deg2rad_1(self):
        """Test deg2rad"""
        self.assertAlmostEqual(math.pi/2.0, angles.Angle.deg2rad(90), self.places)

    def test_deg2rad_2(self):
        """Test deg2rad negative angle"""
        self.assertAlmostEqual(-math.pi, angles.Angle.deg2rad(-180), self.places)

    def test_rad2deg_1(self):
        """Test rad2deg 1"""
        self.assertAlmostEqual(270, angles.Angle.rad2deg(3.0*math.pi/2.0), self.places)

    def test_rad2deg_2(self):
        """Test rad2deg negative angle"""
        self.assertAlmostEqual(-180, angles.Angle.rad2deg(-math.pi), self.places)

    # booleans

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_lt_angle1(self):
        """Test richcompare operator<()"""
        a = angles.Angle(10)
        b = angles.Angle(20)
        self.assertTrue(a < b)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_lt_angle2(self):
        """Test richcompare operator<()"""
        a = angles.Angle(10)
        b = angles.Angle(20)
        self.assertFalse(b < a)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_le_angle1(self):
        """Test richcompare operator<=()"""
        a = angles.Angle(10)
        b = angles.Angle(10)
        self.assertTrue(a <= b)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_le_angle2(self):
        """Test richcompare operator<=()"""
        a = angles.Angle(20)
        b = angles.Angle(20.6)
        self.assertFalse(b <= a)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_eq_angle1(self):
        """Test richcompare operator==()"""
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(1)
        self.assertTrue(an_angle == another_angle)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_eq_angle2(self):
        """Test richcompare operator==()"""
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(-1)
        self.assertFalse(an_angle == another_angle)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ne_angle1(self):
        """Test richcompare operator!=()"""
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(1)
        self.assertFalse(an_angle != another_angle)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ne_angle2(self):
        """Test richcompare operator==()"""
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(-1)
        self.assertTrue(an_angle != another_angle)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_gt_angle1(self):
        """Test richcompare operato>()"""
        a = angles.Angle(30)
        b = angles.Angle(20)
        self.assertTrue(a > b)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_gt_angle2(self):
        """Test richcompare operator>()"""
        a = angles.Angle(30)
        b = angles.Angle(20)
        self.assertFalse(b > a)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ge_angle1(self):
        """Test richcompare operator>=()"""
        a = angles.Angle(10)
        b = angles.Angle(10)
        self.assertTrue(a >= b)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ge_angle2(self):
        """Test richcompare operator>=()"""
        a = angles.Angle(20.9)
        b = angles.Angle(20.6)
        self.assertFalse(b >= a)

    # constructors

    def test_copy_constructor(self):
        """Test copy constructor"""
        an_angle = angles.Angle(self.rd1)
        another_angle = angles.Angle(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_copy_assign(self):
        """Test copy assign
        This is a Python reference copy not a deep copy."""
        an_angle = angles.Angle(self.rd1)
        another_angle = angles.Angle()
        another_angle = an_angle
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    @unittest.skip('Not available in boost')
    def test_deep_copy(self):
        """Test deep copy"""
        an_angle = angles.Angle(self.rd1)
        another_angle = copy.deepcopy(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.Angle()
        self.assertEqual(0, an_angle.value)


    def test_construct_degrees(self):
        """Test construct_degrees"""
        an_angle = angles.Angle(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)


    def test_construct_degrees_minutes(self):
        """Test construct degrees minutes"""
        an_angle = angles.Angle(-45.0, 30.0)
        self.assertEqual(-45.5, an_angle.value)


    def test_construct_degrees_minutes_seconds(self):
        """Test construct degrees minutes seconds"""
        an_angle = angles.Angle(-44, 59.0, 60)
        self.assertEqual(-45.0, an_angle.value)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.Angle(-self.rd1/2, self.rm1, self.rs1)
        b = angles.Angle(-self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.Angle(-self.rd1/2, self.rm1, self.rs1)
        b = angles.Angle(-self.rd1/2, self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.Angle(-self.rd1/2, self.rm1, self.rs1)
        b = angles.Angle(-self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    # accessors

    def test_accessors_1(self):
        """Test value accessors 1"""
        an_angle = angles.Angle()
        an_angle.value = 90
        self.assertEqual(90, an_angle.value)
        self.assertEqual(math.pi/2.0, an_angle.radians)

    def test_accessors_2(self):
        """Test radians accessor negative"""
        an_angle = angles.Angle()
        an_angle.radians = -math.pi/2.0
        self.assertEqual(-90, an_angle.value)
        self.assertEqual(-math.pi/2.0, an_angle.radians)

 
    # operators

    # add

    def test_inplace_add(self):
        """Test angle += angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a1 += a2
        self.assertAlmostEqual(self.rd1 + self.rd1, a1.value, self.places)

    def test_angle_plus_angle(self):
        """Test angle + angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a3 = angles.Angle()
        a3 = a1 + a2
        self.assertAlmostEqual(self.rd1 + self.rd1, a3.value, self.places)


    # subtract

    def test_inplace_subtract(self):
        """Test angle -= angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a1 -= a2
        self.assertAlmostEqual(self.rd1 - self.rd1, a1.value, self.places)

    def test_angle_minus_angle(self):
        """Test angle - angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a3 = angles.Angle()
        a3 = a1 - a2
        self.assertAlmostEqual(self.rd1 - self.rd1, a3.value, self.places)


    @unittest.skip('TODO boost unitary minus?')
    def test_unitary_minus(self):
        """Test angle = -angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(-self.rd1)
        a1 = -a2
        self.assertAlmostEqual(a2.value, a1.value, self.places)


    # multiply

    def test_inplace_multiply(self):
        """Test angle *= angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a1 *= a2
        self.assertAlmostEqual(self.rd1 * self.rd2, a1.value, self.places)


    def test_angle_times_angle(self):
        """Test angle * angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a3 = a1 * a2
        self.assertAlmostEqual(self.rd1 * self.rd2, a3.value, self.places)


    # divide

    def test_angle_inplace_divide_angle(self):
        """Test angle /= angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a1 /= a2
        self.assertAlmostEqual(self.rd1 / self.rd2, a1.value, self.places)


    def test_angle_divide_angle(self):
        """Test angle / angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a3 = a1 / a2
        self.assertAlmostEqual(self.rd1 / self.rd2, a3.value, self.places)


    def test_angle_divide_zero(self):
        """Test angle / 0"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(0)
        self.assertRaises(RuntimeError, lambda a, b: a / b, a1, a2)


    @unittest.skip('TODO fix normalize')
    def test_angle_normalize(self):
        """Test angle * double"""
        a1 = angles.Angle(450)
        a2 = angles.Angle()
        a2 = a1 * 10
        a2.normalize()
        self.assertEqual(45, a2.value)


   # strings

    def test_str(self):
        """Test str"""
        an_angle = angles.Angle()
        a_str = '''0* 0' 0"'''
        self.assertEqual(a_str, str(an_angle))


    @unittest.skip('Not available in boost')
    def test_repr(self):
        """Test repr"""
        an_angle = angles.Angle()
        a_repr = '''0* 0' 0"'''
        self.assertEqual(a_repr, repr(an_angle))







class TestLimitedRangeAngle(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = 0 # TODO -360?
        self.upper_range = 360

        self.lower_minute_range = -60
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_range)
        self.rm1 = random.uniform(self.lower_minute_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_minute_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_range)
        self.rm2 = random.uniform(self.lower_minute_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_minute_range, self.upper_minute_range)

    # static methods

    def test_deg2rad_1(self):
        """Test deg2rad"""
        self.assertAlmostEqual(math.pi/2.0, angles.LimitedRangeAngle.deg2rad(90), self.places)

    def test_deg2rad_2(self):
        """Test deg2rad negative angle"""
        self.assertAlmostEqual(-math.pi, angles.LimitedRangeAngle.deg2rad(-180), self.places)

    def test_rad2deg_1(self):
        """Test rad2deg 1"""
        self.assertAlmostEqual(270, angles.LimitedRangeAngle.rad2deg(3.0*math.pi/2.0), self.places)

    def test_rad2deg_2(self):
        """Test rad2deg negative angle"""
        self.assertAlmostEqual(-180, angles.LimitedRangeAngle.rad2deg(-math.pi), self.places)

    # booleans

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_lt_angle1(self):
        """Test richcompare operator<()"""
        a = angles.LimitedRangeAngle(10)
        b = angles.LimitedRangeAngle(20)
        self.assertTrue(a < b)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_lt_angle2(self):
        """Test richcompare operator<()"""
        a = angles.LimitedRangeAngle(10)
        b = angles.LimitedRangeAngle(20)
        self.assertFalse(b < a)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_le_angle1(self):
        """Test richcompare operator<=()"""
        a = angles.LimitedRangeAngle(10)
        b = angles.LimitedRangeAngle(10)
        self.assertTrue(a <= b)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_le_angle2(self):
        """Test richcompare operator<=()"""
        a = angles.LimitedRangeAngle(20)
        b = angles.LimitedRangeAngle(20.6)
        self.assertFalse(b <= a)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_eq_angle1(self):
        """Test richcompare operator==()"""
        an_angle = angles.LimitedRangeAngle(1)
        another_angle = angles.LimitedRangeAngle(1)
        self.assertTrue(an_angle == another_angle)

    @unittest.skip('TODO boost wrap operator==()')
    def test_angle1_eq_angle2(self):
        """Test richcompare operator==()"""
        an_angle = angles.LimitedRangeAngle(1)
        another_angle = angles.LimitedRangeAngle(-1)
        self.assertFalse(an_angle == another_angle)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ne_angle1(self):
        """Test richcompare operator!=()"""
        an_angle = angles.LimitedRangeAngle(1)
        another_angle = angles.LimitedRangeAngle(1)
        self.assertFalse(an_angle != another_angle)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ne_angle2(self):
        """Test richcompare operator==()"""
        an_angle = angles.LimitedRangeAngle(1)
        another_angle = angles.LimitedRangeAngle(-1)
        self.assertTrue(an_angle != another_angle)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_gt_angle1(self):
        """Test richcompare operato>()"""
        a = angles.LimitedRangeAngle(30)
        b = angles.LimitedRangeAngle(20)
        self.assertTrue(a > b)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_gt_angle2(self):
        """Test richcompare operator>()"""
        a = angles.LimitedRangeAngle(30)
        b = angles.LimitedRangeAngle(20)
        self.assertFalse(b > a)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ge_angle1(self):
        """Test richcompare operator>=()"""
        a = angles.LimitedRangeAngle(10)
        b = angles.LimitedRangeAngle(10)
        self.assertTrue(a >= b)

    @unittest.skip('TODO boost wrap operator!=()')
    def test_angle1_ge_angle2(self):
        """Test richcompare operator>=()"""
        a = angles.LimitedRangeAngle(20.9)
        b = angles.LimitedRangeAngle(20.6)
        self.assertFalse(b >= a)

    # constructors

    def test_copy_constructor(self):
        """Test copy constructor"""
        an_angle = angles.LimitedRangeAngle(self.rd1)
        another_angle = angles.LimitedRangeAngle(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_copy_assign(self):
        """Test copy assign
        This is a Python reference copy not a deep copy."""
        an_angle = angles.LimitedRangeAngle(self.rd1)
        another_angle = angles.LimitedRangeAngle()
        another_angle = an_angle
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    @unittest.skip('Not available in boost')
    def test_deep_copy(self):
        """Test deep copy"""
        an_angle = angles.LimitedRangeAngle(self.rd1)
        another_angle = copy.deepcopy(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.LimitedRangeAngle()
        self.assertEqual(0, an_angle.value)


    def test_construct_degrees(self):
        """Test construct_degrees"""
        an_angle = angles.LimitedRangeAngle(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)


    def test_construct_degrees_minutes(self):
        """Test construct degrees minutes"""
        an_angle = angles.LimitedRangeAngle(45.0, 30.0)
        self.assertEqual(45.5, an_angle.value)


    def test_construct_degrees_minutes_seconds(self):
        """Test construct degrees minutes seconds"""
        an_angle = angles.LimitedRangeAngle(44, 59.0, 60)
        self.assertEqual(45.0, an_angle.value)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.LimitedRangeAngle(self.rd1/2, self.rm1, self.rs1)
        b = angles.LimitedRangeAngle(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.LimitedRangeAngle(self.rd1/2, self.rm1, self.rs1)
        b = angles.LimitedRangeAngle(self.rd1/2, self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.LimitedRangeAngle(self.rd1/2, self.rm1, self.rs1)
        b = angles.LimitedRangeAngle(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    # accessors

    def test_accessors_1(self):
        """Test value accessors 1"""
        an_angle = angles.LimitedRangeAngle()
        an_angle.value = 90
        self.assertEqual(90, an_angle.value)
        self.assertEqual(math.pi/2.0, an_angle.radians)

    def test_accessors_2(self):
        """Test radians accessor negative"""
        an_angle = angles.LimitedRangeAngle()
        an_angle.radians = -math.pi/2.0
        self.assertEqual(-90, an_angle.value)
        self.assertEqual(-math.pi/2.0, an_angle.radians)

 
    # operators

    # add

    def test_inplace_add(self):
        """Test angle += angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd1)
        a1 += a2
        self.assertAlmostEqual(self.rd1 + self.rd1, a1.value, self.places)

    def test_angle_plus_angle(self):
        """Test angle + angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd1)
        a3 = angles.LimitedRangeAngle()
        a3 = a1 + a2
        self.assertAlmostEqual(self.rd1 + self.rd1, a3.value, self.places)


    # subtract

    def test_inplace_subtract(self):
        """Test angle -= angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd1)
        a1 -= a2
        self.assertAlmostEqual(self.rd1 - self.rd1, a1.value, self.places)

    def test_angle_minus_angle(self):
        """Test angle - angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd1)
        a3 = angles.LimitedRangeAngle()
        a3 = a1 - a2
        self.assertAlmostEqual(self.rd1 - self.rd1, a3.value, self.places)


    @unittest.skip('TODO boost unitary minus?')
    def test_unitary_minus(self):
        """Test angle = -angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(-self.rd1)
        a1 = -a2
        self.assertAlmostEqual(a2.value, a1.value, self.places)


    # multiply

    def test_inplace_multiply(self):
        """Test angle *= angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd2)
        a1 *= a2
        self.assertAlmostEqual(self.rd1 * self.rd2, a1.value, self.places)


    def test_angle_times_angle(self):
        """Test angle * angle"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd2)
        a3 = a1 * a2
        self.assertAlmostEqual(self.rd1 * self.rd2, a3.value, self.places)


    # divide

    def test_angle_inplace_divide_double(self):
        """Test angle /= double"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd2)
        a1 /= a2
        self.assertAlmostEqual(self.rd1 / self.rd2, a1.value, self.places)


    def test_angle_divide_double(self):
        """Test angle / double"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(self.rd2)
        a3 = a1 / a2
        self.assertAlmostEqual(self.rd1 / self.rd2, a3.value, self.places)


    def test_angle_divide_zero(self):
        """Test angle / 0"""
        a1 = angles.LimitedRangeAngle(self.rd1)
        a2 = angles.LimitedRangeAngle(0)
        self.assertRaises(RuntimeError, lambda a, b: a / b, a1, a2)


    @unittest.skip('TODO fix normalize')
    def test_angle_normalize(self):
        """Test angle * double"""
        a1 = angles.LimitedRangeAngle(450)
        a2 = angles.LimitedRangeAngle()
        a2 = a1 * 10
        a2.normalize()
        self.assertEqual(45, a2.value)


   # strings

    def test_str(self):
        """Test str"""
        an_angle = angles.LimitedRangeAngle()
        a_str = '''0* 0' 0"'''
        self.assertEqual(a_str, str(an_angle))


    @unittest.skip('Not available in boost')
    def test_repr(self):
        """Test repr"""
        an_angle = angles.LimitedRangeAngle()
        a_repr = '''0* 0' 0"'''
        self.assertEqual(a_repr, repr(an_angle))






# TODO test others, RA, dec, lat, log in different classes?

if __name__ == '__main__':
    random.seed(time.time())
    unittest.main()
