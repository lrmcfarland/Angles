#!/usr/bin/env python

"""Unit tests for space objects."""

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

    def test_rad2deg_1(self):
        """Test rad2deg"""
        self.assertAlmostEqual(math.pi/2.0, angles.Angle.deg2rad(90), self.places)

    def test_rad2deg_2(self):
        """Test rad2deg negative angle"""
        self.assertAlmostEqual(-math.pi, angles.Angle.deg2rad(-180), self.places)

    def test_deg2rad_1(self):
        """Test deg2rad"""
        self.assertAlmostEqual(270, angles.Angle.rad2deg(3.0*math.pi/2.0), self.places)

    def test_deg2rad_2(self):
        """Test deg2rad negative angle"""
        self.assertAlmostEqual(-180, angles.Angle.rad2deg(-math.pi), self.places)

    # constructors

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.Angle()
        self.assertEqual(0, an_angle.value)


    def test_one_arg_constructor(self):
        """Test one argument constructor"""
        an_angle = angles.Angle(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)


    def test_two_arg_constructor(self):
        """Test two argument constructor"""
        an_angle = angles.Angle(-45.0, 30.0)
        self.assertEqual(-45.5, an_angle.value)


    def test_three_arg_constructor(self):
        """Test three argument constructor"""
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


    def test_copy_constructor(self):
        """Test copy constructor"""
        an_angle = angles.Angle(self.rd1)
        another_angle = angles.Angle(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_copy_assign_constructor(self):
        """Test copy assign_constructor"""
        an_angle = angles.Angle(self.rd1)
        another_angle = angles.Angle()
        another_angle = an_angle
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    # accessors

    def test_value_accessor_1(self):
        """Test value accessor negative"""
        an_angle = angles.Angle()
        an_angle.value = 90
        self.assertEqual(90, an_angle.value)
        self.assertEqual(math.pi/2.0, an_angle.radians)

    def test_radians_accessor_1(self):
        """Test radians accessor negative"""
        an_angle = angles.Angle()
        an_angle.radians = -math.pi/2.0
        self.assertEqual(-90, an_angle.value)
        self.assertEqual(-math.pi/2.0, an_angle.radians)

    def test_value_random(self):
        """Test value random"""
        an_angle = angles.Angle()
        an_angle.value = self.rd1
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)

    def test_radians_1(self):
        """Test radians property"""
        an_angle = angles.Angle(180)
        self.assertEqual(math.pi, an_angle.radians)

    def test_radians_2(self):
        """Test radians property negative"""
        an_angle = angles.Angle(-90)
        self.assertEqual(-math.pi/2, an_angle.radians)

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


    # test rich compare


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


    # operators

    def test_angle_plus_angle(self):
        """Test angle + angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a3 = angles.Angle()
        a3 = a1 + a2
        self.assertAlmostEqual(self.rd1 + self.rd1, a3.value, self.places)


    def test_angle_plus_double(self):
        """Test angle + double"""
        a1 = angles.Angle(self.rd1)
        self.assertRaises(TypeError, lambda a: a1 + self.rd1)


    def test_inplace_add(self):
        """Test angle += angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a1 += a2
        self.assertAlmostEqual(self.rd1 + self.rd1, a1.value, self.places)


    def test_angle_minus_angle(self):
        """Test angle - angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a3 = angles.Angle()
        a3 = a1 - a2
        self.assertAlmostEqual(self.rd1 - self.rd1, a3.value, self.places)


    def test_inplace_subtract(self):
        """Test angle -= angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd1)
        a1 -= a2
        self.assertAlmostEqual(self.rd1 - self.rd1, a1.value, self.places)

    @unittest.skip('TODO boost unitary minus?')
    def test_unitary_minus(self):
        """Test angle = -angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(-self.rd1)
        a1 = -a2
        self.assertAlmostEqual(a2.value, a1.value, self.places)


    def test_angle_minus_double(self):
        """Test angle - double"""
        a1 = angles.Angle(self.rd1)
        self.assertRaises(TypeError, lambda a: a1 - self.rd1)


    def test_angle_times_double(self):
        """Test angle * double"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle()
        a2 = a1 * self.rd1
        self.assertAlmostEqual(self.rd1 * self.rd1, a2.value, self.places)


    def test_double_times_angle(self):
        """Test double * angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle()
        a2 = self.rd1 * a1
        self.assertAlmostEqual(self.rd1 * self.rd1, a2.value, self.places)


    def test_angle_inplace_times_double(self):
        """Test angle *= double"""
        a1 = angles.Angle(self.rd1)
        a1 *= self.rd1
        self.assertAlmostEqual(self.rd1 * self.rd1, a1.value, self.places)


    def test_angle_divide_double(self):
        """Test angle / double"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle()
        a2 = a1 / self.rd1
        self.assertAlmostEqual(self.rd1 / self.rd1, a2.value, self.places)


    def test_double_divide_angle(self):
        """Test double / angle"""
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle()
        a2 = self.rd1 / a1
        self.assertAlmostEqual(self.rd1 / self.rd1, a2.value, self.places)


    def test_angle_inplace_divide_double(self):
        """Test angle /= double"""
        a1 = angles.Angle(self.rd1)
        a1 /= self.rd1
        self.assertAlmostEqual(self.rd1 / self.rd1, a1.value, self.places)


    def test_angle_divide_zero(self):
        """Test angle / 0"""
        a1 = angles.Angle(self.rd1)
        self.assertRaises(RuntimeError, lambda a: a / 0, a1)


    @unittest.skip('TODO fix normalize')
    def test_angle_normalize(self):
        """Test angle * double"""
        a1 = angles.Angle(450)
        a2 = angles.Angle()
        a2 = a1 * 10
        a2.normalize()
        self.assertEqual(45, a2.value)


class TestLimitedRangeAngle(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = 0
        self.upper_degree_range = 360
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm1 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm2 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_range, self.upper_minute_range)


    def test_inherited_rad2deg_1(self):
        """Test inherited rad2deg"""
        self.assertAlmostEqual(math.pi/2.0, angles.LimitedRangeAngle.deg2rad(90), self.places)

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

    # constructors and minimum/maximum accessors

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.LimitedRangeAngle()
        self.assertEqual(0, an_angle.value)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(360, an_angle.maximum)


    def test_one_arg_constructor(self):
        """Test one argument constructor"""
        an_angle = angles.LimitedRangeAngle(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(360, an_angle.maximum)


    def test_two_arg_constructor(self):
        """Test two argument constructor"""
        an_angle = angles.LimitedRangeAngle(45.0, 30.0)
        self.assertEqual(45.5, an_angle.value)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(360, an_angle.maximum)


    def test_three_arg_constructor(self):
        """Test three argument constructor"""
        an_angle = angles.LimitedRangeAngle(44, 59.0, 60)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(360, an_angle.maximum)


    def test_four_arg_constructor(self):
        """Test four argument constructor"""
        an_angle = angles.LimitedRangeAngle(-44, 59, 60, -90)
        self.assertEqual(-45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(360, an_angle.maximum)


    def test_five_arg_constructor(self):
        """Test five argument constructoer"""
        an_angle = angles.LimitedRangeAngle(43, 119, 60, -90, 90)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.LimitedRangeAngle(self.rd1/2, self.rm1, self.rs1)
        b = angles.LimitedRangeAngle(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.LimitedRangeAngle(self.rd1/2, self.rm1, self.rs1)
        b = angles.LimitedRangeAngle(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.LimitedRangeAngle(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.LimitedRangeAngle(-self.rd1/2, -self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_4(self):
        """Test mixed sign constructor 4"""
        a = angles.LimitedRangeAngle(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.LimitedRangeAngle(-self.rd1/2, self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_5(self):
        """Test mixed sign constructor 5"""
        a = angles.LimitedRangeAngle(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.LimitedRangeAngle(-self.rd1/2, -self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_6(self):
        """Test mixed sign constructor 6"""
        a = angles.LimitedRangeAngle(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.LimitedRangeAngle(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_out_of_range_constructor_hi(self):
        """Test out of range error hi"""
        self.assertRaises(RuntimeError, lambda: angles.LimitedRangeAngle(720))


    def test_out_of_range_constructor_lo(self):
        """Test out of range error lo"""
        self.assertRaises(RuntimeError, lambda: angles.LimitedRangeAngle(-1))


class TestDeclination(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = -90
        self.upper_degree_range = 90
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm1 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm2 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_range, self.upper_minute_range)


    def test_inherited_rad2deg_1(self):
        """Test inherited rad2deg"""
        self.assertAlmostEqual(math.pi/2.0, angles.Declination.deg2rad(90), self.places)

    # strings

    def test_str(self):
        """Test str"""
        an_angle = angles.Declination()
        a_str = '''0* 0' 0"'''
        self.assertEqual(a_str, str(an_angle))


    @unittest.skip('Not available in boost')
    def test_repr(self):
        """Test repr"""
        an_angle = angles.Declination()
        a_repr = '''0* 0' 0"'''
        self.assertEqual(a_repr, repr(an_angle))

    # constructors and minimum/maximum accessors

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.Declination()
        self.assertEqual(0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_one_arg_constructor(self):
        """Test one argument constructor"""
        an_angle = angles.Declination(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_two_arg_constructor(self):
        """Test two argument constructor"""
        an_angle = angles.Declination(45.0, 30.0)
        self.assertEqual(45.5, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_three_arg_constructor(self):
        """Test three argument constructor"""
        an_angle = angles.Declination(44, 59.0, 60)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_four_arg_constructor(self):
        """Test four argument constructor"""
        an_angle = angles.Declination(-44, 59, 60, -90)
        self.assertEqual(-45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_five_arg_constructor(self):
        """Test five argument constructoer"""
        an_angle = angles.Declination(43, 119, 60, -90, 90)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.Declination(self.rd1/2, self.rm1, self.rs1)
        b = angles.Declination(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.Declination(self.rd1/2, self.rm1, self.rs1)
        b = angles.Declination(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.Declination(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Declination(-self.rd1/2, -self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_4(self):
        """Test mixed sign constructor 4"""
        a = angles.Declination(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Declination(-self.rd1/2, self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_5(self):
        """Test mixed sign constructor 5"""
        a = angles.Declination(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Declination(-self.rd1/2, -self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_6(self):
        """Test mixed sign constructor 6"""
        a = angles.Declination(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Declination(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_out_of_range_constructor_hi(self):
        """Test out of range error hi"""
        self.assertRaises(RuntimeError, lambda: angles.Declination(720))


    def test_out_of_range_constructor_lo(self):
        """Test out of range error lo"""
        self.assertRaises(RuntimeError, lambda: angles.Declination(-91))


# copy of declination
class TestLatitude(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = -90
        self.upper_degree_range = 90
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm1 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm2 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_range, self.upper_minute_range)


    def test_inherited_rad2deg_1(self):
        """Test inherited rad2deg"""
        self.assertAlmostEqual(math.pi/2.0, angles.Latitude.deg2rad(90), self.places)

    # strings

    def test_str(self):
        """Test str"""
        an_angle = angles.Latitude()
        a_str = '''0* 0' 0"'''
        self.assertEqual(a_str, str(an_angle))


    @unittest.skip('Not available in boost')
    def test_repr(self):
        """Test repr"""
        an_angle = angles.Latitude()
        a_repr = '''0* 0' 0"'''
        self.assertEqual(a_repr, repr(an_angle))

    # constructors and minimum/maximum accessors

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.Latitude()
        self.assertEqual(0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_one_arg_constructor(self):
        """Test one argument constructor"""
        an_angle = angles.Latitude(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_two_arg_constructor(self):
        """Test two argument constructor"""
        an_angle = angles.Latitude(45.0, 30.0)
        self.assertEqual(45.5, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_three_arg_constructor(self):
        """Test three argument constructor"""
        an_angle = angles.Latitude(44, 59.0, 60)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_four_arg_constructor(self):
        """Test four argument constructor"""
        an_angle = angles.Latitude(-44, 59, 60, -90)
        self.assertEqual(-45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_five_arg_constructor(self):
        """Test five argument constructoer"""
        an_angle = angles.Latitude(43, 119, 60, -90, 90)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.Latitude(self.rd1/2, self.rm1, self.rs1)
        b = angles.Latitude(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.Latitude(self.rd1/2, self.rm1, self.rs1)
        b = angles.Latitude(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.Latitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Latitude(-self.rd1/2, -self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_4(self):
        """Test mixed sign constructor 4"""
        a = angles.Latitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Latitude(-self.rd1/2, self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_5(self):
        """Test mixed sign constructor 5"""
        a = angles.Latitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Latitude(-self.rd1/2, -self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_6(self):
        """Test mixed sign constructor 6"""
        a = angles.Latitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Latitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_out_of_range_constructor_hi(self):
        """Test out of range error hi"""
        self.assertRaises(RuntimeError, lambda: angles.Latitude(720))


    def test_out_of_range_constructor_lo(self):
        """Test out of range error lo"""
        self.assertRaises(RuntimeError, lambda: angles.Latitude(-91))


class TestLongitude(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = -180
        self.upper_degree_range = 180
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm1 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm2 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_range, self.upper_minute_range)


    def test_inherited_rad2deg_1(self):
        """Test inherited rad2deg"""
        self.assertAlmostEqual(math.pi/2.0, angles.Longitude.deg2rad(90), self.places)

    # strings

    def test_str(self):
        """Test str"""
        an_angle = angles.Longitude()
        a_str = '''0* 0' 0"'''
        self.assertEqual(a_str, str(an_angle))


    @unittest.skip('Not available in boost')
    def test_repr(self):
        """Test repr"""
        an_angle = angles.Longitude()
        a_repr = '''0* 0' 0"'''
        self.assertEqual(a_repr, repr(an_angle))

    # constructors and minimum/maximum accessors

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.Longitude()
        self.assertEqual(0, an_angle.value)
        self.assertEqual(-180, an_angle.minimum)
        self.assertEqual(180, an_angle.maximum)


    def test_one_arg_constructor(self):
        """Test one argument constructor"""
        an_angle = angles.Longitude(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)
        self.assertEqual(-180, an_angle.minimum)
        self.assertEqual(180, an_angle.maximum)


    def test_two_arg_constructor(self):
        """Test two argument constructor"""
        an_angle = angles.Longitude(45.0, 30.0)
        self.assertEqual(45.5, an_angle.value)
        self.assertEqual(-180, an_angle.minimum)
        self.assertEqual(180, an_angle.maximum)


    def test_three_arg_constructor(self):
        """Test three argument constructor"""
        an_angle = angles.Longitude(44, 59.0, 60)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-180, an_angle.minimum)
        self.assertEqual(180, an_angle.maximum)


    def test_four_arg_constructor(self):
        """Test four argument constructor"""
        an_angle = angles.Longitude(-44, 59, 60, -90)
        self.assertEqual(-45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(180, an_angle.maximum)


    def test_five_arg_constructor(self):
        """Test five argument constructoer"""
        an_angle = angles.Longitude(43, 119, 60, -90, 90)
        self.assertEqual(45.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.Longitude(self.rd1/2, self.rm1, self.rs1)
        b = angles.Longitude(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.Longitude(self.rd1/2, self.rm1, self.rs1)
        b = angles.Longitude(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.Longitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Longitude(-self.rd1/2, -self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_4(self):
        """Test mixed sign constructor 4"""
        a = angles.Longitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Longitude(-self.rd1/2, self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_5(self):
        """Test mixed sign constructor 5"""
        a = angles.Longitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Longitude(-self.rd1/2, -self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_6(self):
        """Test mixed sign constructor 6"""
        a = angles.Longitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.Longitude(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_out_of_range_constructor_hi(self):
        """Test out of range error hi"""
        self.assertRaises(RuntimeError, lambda: angles.Longitude(720))


    def test_out_of_range_constructor_lo(self):
        """Test out of range error lo"""
        self.assertRaises(RuntimeError, lambda: angles.Longitude(-191))









class TestRA(unittest.TestCase):

    def setUp(self):

        """Set up test parameters."""

        self.places = 7 # precision

        self.lower_range = 0
        self.upper_degree_range = 24
        self.upper_minute_range = 60

        self.rd1 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm1 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_degree_range)
        self.rm2 = random.uniform(self.lower_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_range, self.upper_minute_range)


    def test_inherited_rad2deg_1(self):
        """Test inherited rad2deg"""
        self.assertAlmostEqual(math.pi/2.0, angles.RA.deg2rad(90), self.places)

    # strings

    def test_str(self):
        """Test str"""
        an_angle = angles.RA()
        a_str = '''0 hr 0' 0"'''
        self.assertEqual(a_str, str(an_angle))


    @unittest.skip('Not available in boost')
    def test_repr(self):
        """Test repr"""
        an_angle = angles.RA()
        a_repr = '''0 hr 0' 0"'''
        self.assertEqual(a_repr, repr(an_angle))

    # constructors and minimum/maximum accessors

    def test_default_constructor(self):
        """Test default constructor"""
        an_angle = angles.RA()
        self.assertEqual(0, an_angle.value)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(24, an_angle.maximum)


    def test_one_arg_constructor(self):
        """Test one argument constructor"""
        an_angle = angles.RA(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(24, an_angle.maximum)


    def test_two_arg_constructor(self):
        """Test two argument constructor"""
        an_angle = angles.RA(23.0, 30.0)
        self.assertEqual(23.5, an_angle.value)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(24, an_angle.maximum)


    def test_three_arg_constructor(self):
        """Test three argument constructor"""
        an_angle = angles.RA(23, 59.0, 60)
        self.assertEqual(24, an_angle.value)
        self.assertEqual(0, an_angle.minimum)
        self.assertEqual(24, an_angle.maximum)


    def test_four_arg_constructor(self):
        """Test four argument constructor"""
        an_angle = angles.RA(-23, 59, 60, -90)
        self.assertEqual(-24.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(24, an_angle.maximum)


    def test_five_arg_constructor(self):
        """Test five argument constructoer"""
        an_angle = angles.RA(22, 119, 60, -90, 90)
        self.assertEqual(24.0, an_angle.value)
        self.assertEqual(-90, an_angle.minimum)
        self.assertEqual(90, an_angle.maximum)


    def test_mixed_sign_constructor_1(self):
        """Test mixed sign constructor 1"""
        # divide 2 to keep in range
        a = angles.RA(self.rd1/2, self.rm1, self.rs1)
        b = angles.RA(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        """Test mixed sign constructor 2"""
        a = angles.RA(self.rd1/2, self.rm1, self.rs1)
        b = angles.RA(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        """Test mixed sign constructor 3"""
        a = angles.RA(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.RA(-self.rd1/2, -self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_4(self):
        """Test mixed sign constructor 4"""
        a = angles.RA(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.RA(-self.rd1/2, self.rm1, -self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_5(self):
        """Test mixed sign constructor 5"""
        a = angles.RA(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.RA(-self.rd1/2, -self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_6(self):
        """Test mixed sign constructor 6"""
        a = angles.RA(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        b = angles.RA(-self.rd1/2, self.rm1, self.rs1, -self.upper_degree_range)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_out_of_range_constructor_hi(self):
        """Test out of range error hi"""
        self.assertRaises(RuntimeError, lambda: angles.RA(24.1))


    def test_out_of_range_constructor_lo(self):
        """Test out of range error lo"""
        self.assertRaises(RuntimeError, lambda: angles.RA(-1.0))







# TODO test others, RA, dec, lat, log in different classes?

if __name__ == '__main__':
    random.seed(time.time())
    unittest.main()
