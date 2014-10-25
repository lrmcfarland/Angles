#!/usr/bin/env python

test_header = """\"\"\"THIS IS A GENERATED FILE. EDITS WILL BE OVERWRITTEN.

Unit tests for angle objects.

It uses the random number generator to select test targets, i.e. the
test is different each time it is run. It is designed to stay in range
except when testing the range limits, but it may exceeded them in
which case the test should be investigated.

\"\"\"

import copy
import math
import random
import time
import unittest

import angles

"""

angle_class_template = """
class TestAngle(unittest.TestCase):

    def setUp(self):

        \"\"\"Set up test parameters.\"\"\"

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

    # Note these are different from python/Boost in that they are
    # module methods not instance methods.

    def test_deg2rad_1(self):
        \"\"\"Test deg2rad\"\"\"
        self.assertAlmostEqual(math.pi/2.0, angles.deg2rad(90), self.places)

    def test_deg2rad_2(self):
        \"\"\"Test deg2rad negative angle\"\"\"
        self.assertAlmostEqual(-math.pi, angles.deg2rad(-180), self.places)

    def test_rad2deg_1(self):
        \"\"\"Test rad2deg 1\"\"\"
        self.assertAlmostEqual(270, angles.rad2deg(3.0*math.pi/2.0), self.places)

    def test_rad2deg_2(self):
        \"\"\"Test rad2deg negative angle\"\"\"
        self.assertAlmostEqual(-180, angles.rad2deg(-math.pi), self.places)

    # booleans

    def test_angle1_lt_angle1(self):
        \"\"\"Test richcompare operator<()\"\"\"
        a = angles.Angle(10)
        b = angles.Angle(20)
        self.assertTrue(a < b)

    def test_angle1_lt_angle2(self):
        \"\"\"Test richcompare operator<()\"\"\"
        a = angles.Angle(10)
        b = angles.Angle(20)
        self.assertFalse(b < a)

    def test_angle1_le_angle1(self):
        \"\"\"Test richcompare operator<=()\"\"\"
        a = angles.Angle(10)
        b = angles.Angle(10)
        self.assertTrue(a <= b)

    def test_angle1_le_angle2(self):
        \"\"\"Test richcompare operator<=()\"\"\"
        a = angles.Angle(20)
        b = angles.Angle(20.6)
        self.assertFalse(b <= a)

    def test_angle1_eq_angle1(self):
        \"\"\"Test richcompare operator==()\"\"\"
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(1)
        self.assertTrue(an_angle == another_angle)

    def test_angle1_eq_angle2(self):
        \"\"\"Test richcompare operator==()\"\"\"
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(-1)
        self.assertFalse(an_angle == another_angle)

    def test_angle1_ne_angle1(self):
        \"\"\"Test richcompare operator!=()\"\"\"
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(1)
        self.assertFalse(an_angle != another_angle)

    def test_angle1_ne_angle2(self):
        \"\"\"Test richcompare operator==()\"\"\"
        an_angle = angles.Angle(1)
        another_angle = angles.Angle(-1)
        self.assertTrue(an_angle != another_angle)

    def test_angle1_gt_angle1(self):
        \"\"\"Test richcompare operato>()\"\"\"
        a = angles.Angle(30)
        b = angles.Angle(20)
        self.assertTrue(a > b)

    def test_angle1_gt_angle2(self):
        \"\"\"Test richcompare operator>()\"\"\"
        a = angles.Angle(30)
        b = angles.Angle(20)
        self.assertFalse(b > a)

    def test_angle1_ge_angle1(self):
        \"\"\"Test richcompare operator>=()\"\"\"
        a = angles.Angle(10)
        b = angles.Angle(10)
        self.assertTrue(a >= b)

    def test_angle1_ge_angle2(self):
        \"\"\"Test richcompare operator>=()\"\"\"
        a = angles.Angle(20.9)
        b = angles.Angle(20.6)
        self.assertFalse(b >= a)

    # constructors

    @unittest.skip('TODO Not yet available in Manual, but it is in Boost')
    def test_copy_constructor(self):
        \"\"\"Test copy constructor\"\"\"
        an_angle = angles.Angle(self.rd1)
        another_angle = angles.Angle(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_copy_assign(self):
        \"\"\"Test copy assign
        This is a Python reference copy not a deep copy.\"\"\"
        an_angle = angles.Angle(self.rd1)
        another_angle = angles.Angle()
        another_angle = an_angle
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)


    @unittest.skip('TODO: Not yet available')
    def test_deep_copy(self):
        \"\"\"Test deep copy\"\"\"
        an_angle = angles.Angle(self.rd1)
        another_angle = copy.deepcopy(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_default_constructor(self):
        \"\"\"Test default constructor\"\"\"
        an_angle = angles.Angle()
        self.assertEqual(0, an_angle.value)


    def test_construct_degrees(self):
        \"\"\"Test construct_degrees\"\"\"
        an_angle = angles.Angle(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)


    def test_construct_degrees_minutes(self):
        \"\"\"Test construct degrees minutes\"\"\"
        an_angle = angles.Angle(-45.0, 30.0)
        self.assertEqual(-45.5, an_angle.value)


    def test_construct_degrees_minutes_seconds(self):
        \"\"\"Test construct degrees minutes seconds\"\"\"
        an_angle = angles.Angle(-44, 59.0, 60)
        self.assertEqual(-45.0, an_angle.value)


    def test_mixed_sign_constructor_1(self):
        \"\"\"Test mixed sign constructor 1\"\"\"
        # divide 2 to keep in range
        a = angles.Angle(-self.rd1/2, self.rm1, self.rs1)
        b = angles.Angle(-self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        \"\"\"Test mixed sign constructor 2\"\"\"
        a = angles.Angle(-self.rd1/2, self.rm1, self.rs1)
        b = angles.Angle(-self.rd1/2, self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        \"\"\"Test mixed sign constructor 3\"\"\"
        a = angles.Angle(-self.rd1/2, self.rm1, self.rs1)
        b = angles.Angle(-self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    # accessors

    def test_accessors_1(self):
        \"\"\"Test value accessors 1\"\"\"
        an_angle = angles.Angle()
        an_angle.value = 90
        self.assertEqual(90, an_angle.value)
        self.assertEqual(math.pi/2.0, an_angle.radians)

    def test_accessors_2(self):
        \"\"\"Test radians accessor negative\"\"\"
        an_angle = angles.Angle()
        an_angle.radians = -math.pi/2.0
        self.assertEqual(-90, an_angle.value)
        self.assertEqual(-math.pi/2.0, an_angle.radians)


    # operators

    # add

    def test_inplace_add(self):
        \"\"\"Test angle += angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a1 += a2
        self.assertAlmostEqual(self.rd1 + self.rd2, a1.value, self.places)

    def test_angle_plus_angle(self):
        \"\"\"Test angle + angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a3 = angles.Angle()
        a3 = a1 + a2
        self.assertAlmostEqual(self.rd1 + self.rd2, a3.value, self.places)


    # subtract

    def test_inplace_subtract(self):
        \"\"\"Test angle -= angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a1 -= a2
        self.assertAlmostEqual(self.rd1 - self.rd2, a1.value, self.places)

    def test_angle_minus_angle(self):
        \"\"\"Test angle - angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a3 = angles.Angle()
        a3 = a1 - a2
        self.assertAlmostEqual(self.rd1 - self.rd2, a3.value, self.places)


    def test_unitary_minus(self):
        \"\"\"Test angle = -angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = -a1
        self.assertAlmostEqual(a1.value, -a2.value, self.places)


    # multiply

    def test_inplace_multiply(self):
        \"\"\"Test angle *= angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a1 *= a2
        self.assertAlmostEqual(self.rd1 * self.rd2, a1.value, self.places)


    def test_angle_times_angle(self):
        \"\"\"Test angle * angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a3 = a1 * a2
        self.assertAlmostEqual(self.rd1 * self.rd2, a3.value, self.places)


    # divide

    def test_angle_inplace_divide_angle(self):
        \"\"\"Test angle /= angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a1 /= a2
        self.assertAlmostEqual(self.rd1 / self.rd2, a1.value, self.places)


    def test_angle_divide_angle(self):
        \"\"\"Test angle / angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(self.rd2)
        a3 = a1 / a2
        self.assertAlmostEqual(self.rd1 / self.rd2, a3.value, self.places)


    # TODO works in Boost.
    # 
    # NameError: global name 'DivideByZeroError' is not defined
    #   File "test_angles.py", line 362
    # self.assertRaises(Angles::DivideByZeroError, lambda a: a / 0.0, a1)
    #                                       ^
    # SyntaxError: invalid syntax
    #
    @unittest.skip('TODO Not yet available in Manual, but it is in Boost')
    def test_angle_divide_zero(self):
        \"\"\"Test angle / 0\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = angles.Angle(0)
        self.assertRaises(RuntimeError, lambda a, b: a / b, a1, a2)


   # strings

    def test_str(self):
        \"\"\"Test str\"\"\"
        an_angle = angles.Angle()
        a_str = '''0* 0' 0\"'''
        self.assertEqual(a_str, str(an_angle))


    def test_repr(self):
        \"\"\"Test repr\"\"\"
        an_angle = angles.Angle()
        a_repr = '''0* 0' 0\"'''
        self.assertEqual(a_repr, repr(an_angle))

""" # end angle class template









# ===================================
# ===== Angle Template Template =====
# ===================================










angle_template_template = """

# -----------------------------
# ----- %(TypeName)s -----
# -----------------------------


class Test%(TypeName)s(unittest.TestCase):

    def setUp(self):

        \"\"\"Set up test parameters.\"\"\"

        self.places = 7 # precision

        # range must be much less than limit or limits exceeded.

        self.lower_range_limit = %(lower_range_limit)s
        self.upper_range_limit = %(upper_range_limit)s

        self.lower_range = %(lower_range_limit)s / 2.0
        self.upper_range = %(upper_range_limit)s / 2.0

        self.lower_minute_range = -60 # seconds too
        self.upper_minute_range =  60 # seconds too

        self.rd1 = random.uniform(self.lower_range, self.upper_range)
        self.rm1 = random.uniform(self.lower_minute_range, self.upper_minute_range)
        self.rs1 = random.uniform(self.lower_minute_range, self.upper_minute_range)

        self.rd2 = random.uniform(self.lower_range, self.upper_range)
        self.rm2 = random.uniform(self.lower_minute_range, self.upper_minute_range)
        self.rs2 = random.uniform(self.lower_minute_range, self.upper_minute_range)

    # range errors

    # TODO works in Boost as a RuntimeError
    # 
    # NameError: global name 'RangeError' is not defined
    #
    # self.assertRaises(Angles::RangeError, lambda a: a / 0.0, a1)
    #                                       ^
    # SyntaxError: invalid syntax
    #
    @unittest.skip('TODO Not yet available in Manual, but it is in Boost')
    def test_construction_range_error_lo(self):
        \"\"\"Test range error lo\"\"\"
        self.assertRaises(RuntimeError, lambda: angles.%(TypeName)s(%(lower_range_limit)s - 1))


    # TODO works in Boost as a RuntimeError
    # 
    # NameError: global name 'RangeError' is not defined
    #
    # self.assertRaises(Angles::RangeError, lambda a: a / 0.0, a1)
    #                                       ^
    # SyntaxError: invalid syntax
    #
    @unittest.skip('TODO Not yet available in Manual, but it is in Boost')
    def test_construction_range_error_hi(self):
        \"\"\"Test range error hi\"\"\"
        self.assertRaises(RuntimeError, lambda: angles.%(TypeName)s(%(upper_range_limit)s + 1))


    # static/module methods

    def test_deg2rad_1(self):
        \"\"\"Test deg2rad\"\"\"
        self.assertAlmostEqual(math.pi/2.0, angles.deg2rad(90), self.places)

    def test_deg2rad_2(self):
        \"\"\"Test deg2rad negative angle\"\"\"
        self.assertAlmostEqual(-math.pi, angles.deg2rad(-180), self.places)

    def test_rad2deg_1(self):
        \"\"\"Test rad2deg 1\"\"\"
        self.assertAlmostEqual(270, angles.rad2deg(3.0*math.pi/2.0), self.places)

    def test_rad2deg_2(self):
        \"\"\"Test rad2deg negative angle\"\"\"
        self.assertAlmostEqual(-180, angles.rad2deg(-math.pi), self.places)

    # booleans

    def test_angle1_lt_angle1(self):
        \"\"\"Test richcompare operator<()\"\"\"
        a = angles.%(TypeName)s(10)
        b = angles.%(TypeName)s(20)
        self.assertTrue(a < b)

    def test_angle1_lt_angle2(self):
        \"\"\"Test richcompare operator<()\"\"\"
        a = angles.%(TypeName)s(10)
        b = angles.%(TypeName)s(20)
        self.assertFalse(b < a)

    def test_angle1_le_angle1(self):
        \"\"\"Test richcompare operator<=()\"\"\"
        a = angles.%(TypeName)s(10)
        b = angles.%(TypeName)s(10)
        self.assertTrue(a <= b)

    def test_angle1_le_angle2(self):
        \"\"\"Test richcompare operator<=()\"\"\"
        a = angles.%(TypeName)s(20)
        b = angles.%(TypeName)s(20.6)
        self.assertFalse(b <= a)

    def test_angle1_eq_angle1(self):
        \"\"\"Test richcompare operator==()\"\"\"
        an_angle = angles.%(TypeName)s(1)
        another_angle = angles.%(TypeName)s(1)
        self.assertTrue(an_angle == another_angle)

    def test_angle1_eq_angle2(self):
        \"\"\"Test richcompare operator==()\"\"\"
        an_angle = angles.%(TypeName)s(1)
        another_angle = angles.%(TypeName)s(2)
        self.assertFalse(an_angle == another_angle)

    def test_angle1_ne_angle1(self):
        \"\"\"Test richcompare operator!=()\"\"\"
        an_angle = angles.%(TypeName)s(1)
        another_angle = angles.%(TypeName)s(1)
        self.assertFalse(an_angle != another_angle)

    def test_angle1_ne_angle2(self):
        \"\"\"Test richcompare operator!=()\"\"\"
        an_angle = angles.%(TypeName)s(1)
        another_angle = angles.%(TypeName)s(2)
        self.assertTrue(an_angle != another_angle)

    def test_angle1_gt_angle1(self):
        \"\"\"Test richcompare operator>()\"\"\"
        a = angles.%(TypeName)s(12)
        b = angles.%(TypeName)s(6)
        self.assertTrue(a > b)

    def test_angle1_gt_angle2(self):
        \"\"\"Test richcompare operator>()\"\"\"
        a = angles.%(TypeName)s(12)
        b = angles.%(TypeName)s(6)
        self.assertFalse(b > a)

    def test_angle1_ge_angle1(self):
        \"\"\"Test richcompare operator>=()\"\"\"
        a = angles.%(TypeName)s(12)
        b = angles.%(TypeName)s(6)
        self.assertTrue(a >= b)

    def test_angle1_ge_angle2(self):
        \"\"\"Test richcompare operator>=()\"\"\"
        a = angles.%(TypeName)s(12)
        b = angles.%(TypeName)s(6)
        self.assertFalse(b >= a)

    # constructors

    @unittest.skip('TODO Not yet available in Manual, but it is in Boost')
    def test_copy_constructor(self):
        \"\"\"Test copy constructor\"\"\"
        an_angle = angles.%(TypeName)s(self.rd1)
        another_angle = angles.%(TypeName)s(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_copy_assign(self):
        \"\"\"Test copy assign
        This is a Python reference copy not a deep copy.\"\"\"
        an_angle = angles.%(TypeName)s(self.rd1)
        another_angle = angles.%(TypeName)s()
        another_angle = an_angle
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    @unittest.skip('TODO: Not yet available in Boost or Manual')
    def test_deep_copy(self):
        \"\"\"Test deep copy\"\"\"
        an_angle = angles.%(TypeName)s(self.rd1)
        another_angle = copy.deepcopy(an_angle)
        self.assertAlmostEqual(self.rd1, another_angle.value, self.places)

    def test_default_constructor(self):
        \"\"\"Test default constructor\"\"\"
        an_angle = angles.%(TypeName)s()
        self.assertEqual(0, an_angle.value)


    def test_construct_degrees(self):
        \"\"\"Test construct_degrees\"\"\"
        an_angle = angles.%(TypeName)s(self.rd1)
        self.assertAlmostEqual(self.rd1, an_angle.value, self.places)


    def test_construct_degrees_minutes(self):
        \"\"\"Test construct degrees minutes\"\"\"
        an_angle = angles.%(TypeName)s(15.0, 30.0)
        self.assertEqual(15.5, an_angle.value)


    def test_construct_degrees_minutes_seconds(self):
        \"\"\"Test construct degrees minutes seconds\"\"\"
        an_angle = angles.%(TypeName)s(14, 59.0, 60)
        self.assertEqual(15.0, an_angle.value)


    def test_mixed_sign_constructor_1(self):
        \"\"\"Test mixed sign constructor 1\"\"\"
        # divide 2 to keep in range
        a = angles.%(TypeName)s(self.rd1/2, self.rm1, self.rs1)
        b = angles.%(TypeName)s(self.rd1/2, -self.rm1, self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_2(self):
        \"\"\"Test mixed sign constructor 2\"\"\"
        a = angles.%(TypeName)s(self.rd1/2, self.rm1, self.rs1)
        b = angles.%(TypeName)s(self.rd1/2, self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    def test_mixed_sign_constructor_3(self):
        \"\"\"Test mixed sign constructor 3\"\"\"
        a = angles.%(TypeName)s(self.rd1/2, self.rm1, self.rs1)
        b = angles.%(TypeName)s(self.rd1/2, -self.rm1, -self.rs1)
        self.assertAlmostEqual(a.value, b.value, self.places)


    # accessors

    def test_accessors_1(self):
        \"\"\"Test value accessors 1\"\"\"
        an_angle = angles.%(TypeName)s()
        an_angle.value = 90
        self.assertEqual(90, an_angle.value)
        self.assertEqual(math.pi/2.0, an_angle.radians)

    def test_accessors_2(self):
        \"\"\"Test radians accessor negative\"\"\"
        an_angle = angles.%(TypeName)s()
        an_angle.radians = -math.pi/2.0
        self.assertEqual(-90, an_angle.value)
        self.assertEqual(-math.pi/2.0, an_angle.radians)


    # operators

    # add

    def test_inplace_add(self):
        \"\"\"Test angle += angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(self.rd2)
        a1 += a2
        self.assertAlmostEqual(self.rd1 + self.rd2, a1.value, self.places)

    def test_angle_plus_angle(self):
        \"\"\"Test angle + angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(self.rd2)
        a3 = angles.%(TypeName)s()
        a3 = a1 + a2
        self.assertAlmostEqual(self.rd1 + self.rd2, a3.value, self.places)


    # subtract

    def test_inplace_subtract(self):
        \"\"\"Test angle -= angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(self.rd2)

        if %(unsigned)s:
            if a1 > a2:
                a1 -= a2
                self.assertAlmostEqual(self.rd1 - self.rd2, a1.value, self.places)
            else:
                a2 -= a1
                self.assertAlmostEqual(self.rd2 - self.rd1, a2.value, self.places)
        else:
            a1 -= a2
            self.assertAlmostEqual(self.rd1 - self.rd2, a1.value, self.places)


    def test_angle_minus_angle(self):
        \"\"\"Test angle - angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(self.rd2)
        a3 = angles.%(TypeName)s()

        if %(unsigned)s:
            if a1 > a2:
                a3 = a1 - a2
            else:
                a3 = a2 - a1
            self.assertAlmostEqual(math.fabs(self.rd1 - self.rd2), a3.value, self.places)
        else:
            a3 = a1 - a2
            self.assertAlmostEqual(self.rd1 - self.rd2, a3.value, self.places)


    def test_unitary_minus(self):
        \"\"\"Test angle = -angle\"\"\"
        a1 = angles.Angle(self.rd1)
        a2 = -a1
        self.assertAlmostEqual(a1.value, -a2.value, self.places)


    # multiply

    def test_inplace_multiply(self):
        \"\"\"Test angle *= angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(2) # less than max limit
        a1 *= a2
        self.assertAlmostEqual(self.rd1 * 2, a1.value, self.places)

    def test_angle_times_angle(self):
        \"\"\"Test angle * angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(2)
        a3 = a1 * a2
        self.assertAlmostEqual(self.rd1 * 2, a3.value, self.places)


    # divide

    def test_angle_inplace_divide_angle(self):
        \"\"\"Test angle /= angle\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(2)
        a1 /= a2
        self.assertAlmostEqual(self.rd1 / 2, a1.value, self.places)

    def test_angle_divide_angle(self):
        \"\"\"Test angle / angle foo\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(2)
        a3 = a1 / a2
        self.assertAlmostEqual(self.rd1 / 2, a3.value, self.places)


    # TODO works in Boost.
    # 
    # NameError: global name 'DivideByZeroError' is not defined
    #   File "test_angles.py", line 362
    # self.assertRaises(Angles::DivideByZeroError, lambda a: a / 0.0, a1)
    #                                       ^
    # SyntaxError: invalid syntax
    # TODO RuntimeError works for RangeError???
    #
    @unittest.skip('TODO Not yet available in Manual, but it is in Boost')
    def test_angle_divide_zero(self):
        \"\"\"Test angle / 0\"\"\"
        a1 = angles.%(TypeName)s(self.rd1)
        a2 = angles.%(TypeName)s(0)
        self.assertRaises(RuntimeError, lambda a, b: a / b, a1, a2)


"""

test_dms_string = """
   # strings

    def test_str(self):
        \"\"\"Test str\"\"\"
        an_angle = angles.%(TypeName)s()
        a_str = '''0* 0' 0\"'''
        self.assertEqual(a_str, str(an_angle))


    def test_repr(self):
        \"\"\"Test repr\"\"\"
        an_angle = angles.%(TypeName)s()
        a_repr = '''0* 0' 0\"'''
        self.assertEqual(a_repr, repr(an_angle))

"""

test_hms_string = """
   # strings

    def test_str(self):
        \"\"\"Test str\"\"\"
        an_angle = angles.%(TypeName)s()
        a_str = '''0:0:0'''
        self.assertEqual(a_str, str(an_angle))

    def test_repr(self):
        \"\"\"Test repr\"\"\"
        an_angle = angles.%(TypeName)s()
        a_repr = '''0:0:0'''
        self.assertEqual(a_repr, repr(an_angle))

"""

test_main = """

if __name__ == '__main__':
    random.seed(time.time())
    unittest.main()
"""

# ================
# ===== main =====
# ================

if __name__ == '__main__':

    angle_classes = list()
    angle_classes.append({'TypeName': 'Angle'})

    angle_templates = list()

    angle_templates.append({'TypeName': 'LimitedRangeAngle',
                            'lower_range_limit': -360,
                            'upper_range_limit':  360,
                            'dms string': True,
                            'unsigned': False})

    angle_templates.append({'TypeName': 'Declination',
                            'lower_range_limit': -90,
                            'upper_range_limit':  90,
                            'dms string': True,
                            'unsigned': False})

    angle_templates.append({'TypeName': 'Latitude',
                            'lower_range_limit': -90,
                            'upper_range_limit':  90,
                            'dms string': True,
                            'unsigned': False})

    angle_templates.append({'TypeName': 'Longitude',
                            'lower_range_limit': -180,
                            'upper_range_limit':  180,
                            'dms string': True,
                            'unsigned': False})

    angle_templates.append({'TypeName': 'RA',
                            'lower_range_limit':  0,
                            'upper_range_limit': 24,
                            'dms string': False,
                            'unsigned': True})


    flnm = 'test_angles.py'
    afp = open(flnm, 'w')

    afp.write(test_header)

    for angle_class in angle_classes:
        afp.write(angle_class_template % angle_class)

    for angle_template in angle_templates:
        afp.write(angle_template_template % angle_template)
        if angle_template['dms string']:
            afp.write(test_dms_string % angle_template)
        else:
            afp.write(test_hms_string % angle_template)

    # TODO different string template for RA

    afp.write(test_main)

    afp.close()
