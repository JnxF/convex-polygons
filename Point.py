from __future__ import annotations

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other: Point):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def __eq__(self, other):
        if type(other) != Point:
            return False
        return abs(self.x - other.x) < 1e-7 and abs(self.y - other.y) < 1e-7

    def __lt__(self, other):
        if type(other) != Point:
            return False
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
