from __future__ import annotations
from typing import List, Optional, Tuple
from functools import reduce
from PIL import Image, ImageDraw
from Point import Point
from copy import deepcopy

class ConvexPolygon:
    def __init__(self, coordinates: List[Point]):
        self.points = self._convex_hull(coordinates)

    def __repr__(self):
        return str(self.points) + " : " + str(self.num_vertices())

    def __eq__(self, other):
        if type(other) != ConvexPolygon:
            return False

        if len(self.points) != len(other.points):
            return False

        for (pa, pb) in zip(self.points, other.points):
            if pa != pb:
                return False

        return True

    @staticmethod
    def _convex_hull(points):
        TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

        def cmp(a, b):
            return (a > b) - (a < b)

        def _turn(p, q, r):
            return cmp((q.x - p.x) * (r.y - p.y) - (r.x - p.x) * (q.y - p.y), 0)

        def _keep_left(hull, r):
            while len(hull) > 1 and _turn(hull[-2], hull[-1], r) != TURN_LEFT:
                hull.pop()
            if not len(hull) or hull[-1] != r:
                hull.append(r)
            return hull

        points = sorted(points)

        l = reduce(_keep_left, points, [])
        u = reduce(_keep_left, reversed(points), [])
        return l.extend(u[i] for i in range(1, len(u) - 1)) or l

    def inside_point(self, point: Point) -> bool:
        pass

    def num_vertices(self) -> int:
        return len(self.points)

    def num_edges(self) -> int:
        n = self.num_vertices()
        if n <= 1:
            return 0
        elif n == 2:
            return 1
        else:
            return n

    def perimeter(self) -> float:
        n = self.num_vertices()
        if n <= 1:
            return 0
        elif n == 2:
            [v0, v1] = self.points
            return v0.distance(v1)
        else:
            perimeter = 0.0
            for idx, p in enumerate(self.points):
                previous = self.points[-1] if idx == 0 else self.points[idx - 1]
                perimeter += previous.distance(p)
            return perimeter

    def area(self) -> float:
        n = self.num_vertices()
        if n <= 2:
            return 0

        area = 0.0
        for i in range(n - 1):
            area += self.points[i].x * self.points[i + 1].y
        area += self.points[n - 1].x * self.points[0].y
        for i in range(n - 1):
            area -= self.points[i + 1].x * self.points[i].y
        area -= self.points[0].x * self.points[n - 1].y
        return abs(area) / 2.0

    def centroid(self) -> Optional[Point]:
        n = self.num_vertices()
        if n == 0:
            return None
        meanX, meanY = 0.0, 0.0
        for p in self.points:
            meanX += p.x
            meanY += p.y
        meanX /= n
        meanY /= n
        return Point(meanX, meanY)

    def is_regular(self) -> bool:
        n = self.num_vertices()
        if n <= 1:
            return True
        if n == 2:
            return False

        # All vertices are to the same distance to each other
        d = self.points[0].distance(self.points[1])
        for idx, p in enumerate(self.points):
            previous = self.points[-1] if idx == 0 else self.points[idx - 1]
            if abs(previous.distance(p) - d) > 1e-7:
                return False
        return True

    def bounding_box(self) -> Optional[Tuple[Point, Point]]:
        n = self.num_vertices()
        if n == 0:
            return None
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return (Point(min(xs), min(ys)), Point(max(xs), max(ys)))

    def draw(self, outline="#000000"):
        img = Image.new("RGB", (400, 400), "White")
        dib = ImageDraw.Draw(img)
        (pmin, pmax) = self.bounding_box()
        dx = pmax.x - pmin.x
        dy = pmax.y - pmin.y
        myPol = [
            (396.0 * (p.x - pmin.x) / dx + 2, 400 - (396.0 * (p.y - pmin.y) / dy + 2))
            for p in self.points
        ]
        dib.polygon(myPol, outline=outline)
        img.save("image.png")

    @staticmethod
    def union(cp1: ConvexPolygon, cp2: ConvexPolygon):
        return ConvexPolygon(deepcopy(cp1.points) + deepcopy(cp2.points))


if __name__ == "__main__":
    print(ConvexPolygon([Point(0, 0), Point(0, 0)]))
