"""Module for point classes for the Itinerary genetic search"""

import math


def distance(src, dest):
    if not (type(src) is Town and type(dest) is Town):
        raise TypeError("Town.distance must take two Towns")

    x = math.abs(dest.x - src.x)
    y = math.abs(dest.y - src.y)
    return math.sqrt(x ** 2 + y ** 2)


class Town(object):
    """Town class is basically a point with a few other property."""

    # TODO : Board size and avoid out of range points
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    # Experimentations with python properties
    def name():
        doc = "Name of the town."

        def fget(self):
            return self._name

        def fset(self, value):
            self._name = value

        def fdel(self):
            del self._name
        return locals()
    name = property(**name())
