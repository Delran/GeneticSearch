"""Util functions for genetic search algorithm."""
import string
import random

# Storing the length of the printable const
nbPrintables = len(string.printable)


def getRandomPrintable():
    """Return a random printable char."""
    ret = ""
    while True:
        index = random.randrange(nbPrintables)
        ret = string.printable[index]
        if not ret.isspace() or ret == " ":
            break
    return ret


def isPrintable(toCheck):
    """Check if a string is made of printable.

    Only accepts spaces as printable whitespace
    """
    if not isinstance(toCheck, str):
        raise TypeError("Utils.isPrintable only accepts strings")

    for char in toCheck:
        if char != " ":
            if char.isspace() or char not in string.printable:
                return False
    return True


def generateRandomString(length):
    """Generate a random string with the given length."""
    randomStr = ""
    for i in range(length):
        randomStr += getRandomPrintable()
    return randomStr


def mixStrings(str1, str2):
    """Randomly mixes two given string."""
    ret = ""
    length = len(str1)
    rand = random.randint(1, length-1)
    for i in range(length):
        char = str1[i] if i < rand else str2[i]
        ret += char
    return ret


def changeOneChar(str):
    """Change a random char of the given string to another printable."""
    ret = ""
    length = len(str)
    rand = random.randrange(length)
    for i in range(length):
        char = str[i] if i != rand else getRandomPrintable()
        ret += char
    return ret


# Deprecated, way to slow compared to python builtin list.sort()
def quickSort(list, sortFn):
    """Quick sort with sorting function."""
    """Given list will be sorted using the function passed in argument"""
    """The sort isn't in place and will use additional memory"""

    # TODO: Should sorting function do the comparison between the items ?

    # Using python lists as sub arrays
    greater = []
    equal = []
    lesser = []

    # Used to count the number of matched items
    # small optimization to avoid using len()
    nbAbove = 0
    nbBelow = 0

    pivot = list[0]
    for item in list:
        # Getting sorting function result for current item
        ret = sortFn(pivot, item)
        if ret == 1:
            nbAbove += 1
            greater.append(item)
        elif ret == -1:
            nbBelow += 1
            lesser.append(item)
        else:
            equal.append(item)

    # Recursively sorting the greater and less item lists
    # only if there is more than one element
    sortedLow = quickSort(lesser, sortFn) if nbBelow > 1 else lesser
    sortedHigh = quickSort(greater, sortFn) if nbAbove > 1 else greater

    # Equals items doesn't need to be sorted
    # Using python easy list merging to avoid headaches
    return sortedLow + equal + sortedHigh
