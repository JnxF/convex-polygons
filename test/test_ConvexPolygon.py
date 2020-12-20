import math
from unittest import TestCase

from hypothesis import given, assume
from hypothesis.strategies import floats, integers

from ConvexPolygon import ConvexPolygon
from Point import Point


class TestConvexPolygon(TestCase):
    def test_num_vertices(self):
        self.assertEqual(ConvexPolygon([]).num_vertices(), 0)
        self.assertEqual(ConvexPolygon([Point(2, 1)]).num_vertices(), 1)
        self.assertEqual(ConvexPolygon([Point(2, 1), Point(3, 4)]).num_vertices(), 2)
        self.assertEqual(
            ConvexPolygon([Point(2, 1), Point(3, 4), Point(5, 6)]).num_vertices(), 3
        )

    def test_num_edges(self):
        self.assertEqual(ConvexPolygon([]).num_edges(), 0)
        self.assertEqual(ConvexPolygon([Point(2, 1)]).num_edges(), 0)
        self.assertEqual(ConvexPolygon([Point(2, 1), Point(3, 4)]).num_edges(), 1)
        self.assertEqual(
            ConvexPolygon([Point(2, 1), Point(3, 4), Point(5, 6)]).num_edges(), 3
        )

    def test_perimeter(self):
        self.assertEqual(ConvexPolygon([]).perimeter(), 0)
        self.assertEqual(ConvexPolygon([Point(2, 1)]).perimeter(), 0)
        self.assertEqual(
            ConvexPolygon([Point(0, 0), Point(1, 1)]).perimeter(), math.sqrt(2)
        )
        self.assertEqual(
            ConvexPolygon([Point(0, 0), Point(0, 3), Point(4, 0)]).perimeter(), 12
        )

    def test_area(self):
        self.assertEqual(ConvexPolygon([]).area(), 0)
        self.assertEqual(ConvexPolygon([Point(2, 1)]).area(), 0)
        self.assertEqual(ConvexPolygon([Point(0, 0), Point(1, 1)]).area(), 0)
        self.assertEqual(
            ConvexPolygon([Point(0, 0), Point(0, 3), Point(4, 0)]).area(), 6
        )
        self.assertEqual(
            ConvexPolygon(
                [Point(5, 5), Point(10, 5), Point(10, 10), Point(5, 10)]
            ).area(),
            25,
        )
        self.assertEqual(
            ConvexPolygon(
                [Point(3, 4), Point(5, 6), Point(9, 5), Point(12, 8), Point(5, 11)]
            ).area(),
            35,
        )

    def test_centroid(self):
        self.assertIsNone(ConvexPolygon([]).centroid())
        self.assertEqual(ConvexPolygon([Point(2, 1)]).centroid(), Point(2, 1))
        self.assertEqual(
            ConvexPolygon([Point(0, 0), Point(1, 1)]).centroid(), Point(0.5, 0.5)
        )
        self.assertEqual(
            ConvexPolygon([Point(0, 0), Point(1, 1), Point(2, 0)]).centroid(),
            Point(1, 1 / 3),
        )

    def test_is_regular(self):
        self.assertTrue(ConvexPolygon([]).is_regular())
        self.assertTrue(ConvexPolygon([Point(1, 2)]).is_regular())

    @given(
        floats(allow_nan=False, allow_infinity=False, min_value=-1e5, max_value=1e5),
        floats(allow_nan=False, allow_infinity=False, min_value=-1e5, max_value=1e5),
        floats(allow_nan=False, allow_infinity=False, min_value=1e-3),
        floats(allow_nan=False, allow_infinity=False, min_value=1e-3),
    )
    def test_two_side_polygons_are_not_regular(self, x1, y1, dx, dy):
        p1 = Point(x1, y1)
        p2 = Point(x1 + dx, y1 + dy)
        self.assertFalse(ConvexPolygon([p1, p2]).is_regular())

    @given(
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
        floats(allow_nan=False, allow_infinity=False),
    )
    def test_all_squares_are_regular(self, x, y, side):
        assume(0 <= side <= 1e5)
        assume(abs(x) <= 1e5)
        assume(abs(y) <= 1e5)
        self.assertTrue(
            ConvexPolygon(
                [
                    Point(x, y),
                    Point(x + side, y),
                    Point(x + side, y + side),
                    Point(x, y + side),
                ]
            ).is_regular()
        )

    @given(
        integers(min_value=3, max_value=1000),
        floats(allow_nan=False, allow_infinity=False, min_value=0.1, max_value=1e6),
    )
    def test_generated_regular_polygons_are_regular(self, n, r):
        ang = 2.0 * math.pi / n
        points = [Point(r * math.sin(i * ang), r * math.cos(i * ang)) for i in range(n)]
        self.assertTrue(ConvexPolygon(points).is_regular())

    def test_bounding_box(self):
        self.assertIsNone(ConvexPolygon([]).bounding_box())
        self.assertEqual(
            ConvexPolygon([Point(3, 5)]).bounding_box(), (Point(3, 5), Point(3, 5))
        )
        self.assertEqual(
            ConvexPolygon([Point(1, 4), Point(3, 2)]).bounding_box(),
            (Point(1, 2), Point(3, 4)),
        )

    def test_union(self):
        triangle = ConvexPolygon([Point(0, 0), Point(0, 5), Point(0, 5)])
        self.assertEqual(triangle, ConvexPolygon.union(triangle, triangle))

        bigSquare = ConvexPolygon(
            [Point(-10, -10), Point(10, -10), Point(10, 10), Point(-10, 10)]
        )
        littleSquare = ConvexPolygon(
            [Point(-5, -5), Point(5, -5), Point(5, 5), Point(-5, 5)]
        )
        self.assertEqual(bigSquare, ConvexPolygon.union(bigSquare, littleSquare))

        unitSquare = ConvexPolygon([Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)])
        singlePoint = ConvexPolygon([Point(10, 10)])
        self.assertEqual(
            ConvexPolygon.union(unitSquare, singlePoint),
            ConvexPolygon([Point(0, 0), Point(1, 0), Point(0, 1), Point(10, 10)]),
        )
