"""Module for point classes for the Itinerary genetic search."""

import math

# Distances dictionnary to avoid recalculating already
# calculated distances
distances = {}


def distance(src, dest):
    """Calculate distance between given towns."""
    if not (type(src) is Town and type(dest) is Town):
        raise TypeError("Town.distance must take two Towns")

    t1 = src.id
    t2 = dest.id
    # Distances are the same no matter the towns order
    # We order the dictionnary keys by id so that
    # each pair of town has the same key no matter
    # in which order they are sent
    tuple = (t1, t2) if t1 > t2 else (t2, t1)

    if tuple in distances:
        return distances[tuple]

    # If distance isn't in the dictionnary we calculate it
    x = abs(dest.x - src.x)
    y = abs(dest.y - src.y)
    dist = math.sqrt(x ** 2 + y ** 2)

    distances[tuple] = dist
    return dist


class Town(object):
    """Town class is basically a point with a few other property."""

    # TODO : Board size and avoid out of range points
    def __init__(self, id, coords):
        """Init with coords as tuple."""
        self.id = id
        self.x = coords[0]
        self.y = coords[1]

    # Experimentations with python properties
    def name():
        """Property function."""
        doc = "Name of the town."

        def fget(self):
            return self._name

        def fset(self, value):
            self._name = value

        def fdel(self):
            del self._name
        return locals()
    name = property(**name())
