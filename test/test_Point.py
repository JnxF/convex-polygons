from unittest import TestCase
from hypothesis import given
from hypothesis.strategies import floats

from Point import Point


class TestPoint(TestCase):
    def test_distance(self):
        self.assertAlmostEqual(Point(0, 0).distance(Point(1, 1)), 1.41421356237)
        self.assertAlmostEqual(Point(5, 6).distance(Point(10, 20)), 14.8660687473)
        self.assertAlmostEqual(Point(-30, 2).distance(Point(5, 9)), 35.6931365951)

    @given(
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
    )
    def test_distance_is_reflexive(self, fl1, fl2, fl3, fl4):
        p1 = Point(fl1, fl2)
        p2 = Point(fl3, fl4)
        d1 = p1.distance(p2)
        d2 = p2.distance(p1)
        self.assertAlmostEqual(d1, d2)

    @given(
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
    )
    def test_distance_is_positive(self, fl1, fl2, fl3, fl4):
        p1 = Point(fl1, fl2)
        p2 = Point(fl3, fl4)
        self.assertGreaterEqual(p1.distance(p2), 0)

    @given(
        floats(allow_nan=False, allow_infinity=False, min_value=-1e10, max_value=1e10),
        floats(allow_nan=False, allow_infinity=False, min_value=-1e10, max_value=1e10),
        floats(allow_nan=False, allow_infinity=False, min_value=-1e10, max_value=1e10),
        floats(allow_nan=False, allow_infinity=False, min_value=-1e10, max_value=1e10),
        floats(allow_nan=False, allow_infinity=False, min_value=-1e10, max_value=1e10),
        floats(allow_nan=False, allow_infinity=False, min_value=-1e10, max_value=1e10),
    )
    def test_distance_verifies_triangle_inequality(self, fl1, fl2, fl3, fl4, fl5, fl6):
        p = Point(fl1, fl2)
        q = Point(fl3, fl4)
        r = Point(fl5, fl6)
        self.assertGreaterEqual(p.distance(q) + q.distance(r), p.distance(r))

    @given(
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
    )
    def test_distance_to_itself_is_zero(self, fl1, fl2):
        p = Point(fl1, fl2)
        self.assertAlmostEqual(p.distance(p), 0)
