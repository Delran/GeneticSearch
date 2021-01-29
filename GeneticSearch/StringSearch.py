"""Genetic search algorithm for strings."""
from GeneticSearch.AbstractSearch import AbstractSearch

import Utils


class StringSearch(AbstractSearch):
    """Search for the given string using the a genetic search."""

    def __init__(self, finalString, population, mutateRate, selectRate):
        """Init string genetic search algorithm."""
        self.__finalString = finalString
        super(StringSearch, self).__init__(population,
                                           mutateRate,
                                           selectRate)

    def _validate(self):
        """Validate the type of the given parameters.

        Check if the finalString has any unsuported chars
        """
        self._valid = super()._validate()
        if self._valid:
            if (self.__finalString is None
               or type(self.__finalString) is not str):

                print("Looking for string is None or not a string")
                self._valid = False

            elif not Utils.isPrintable(self.__finalString):
                print(f"\"{self.__finalString}\" has unprintable chars")
                self._valid = False

    def _generatePopulation(self):
        """Generate the initial population for the algorithm.

        Here are entirely random strings made of printable chars
        """
        strs = []
        strLen = len(self.__finalString)
        for i in range(self._population):
            strs.append(Utils.generateRandomString(strLen))
        return strs

    def _fitness(self, str):
        """Return the fitness of the given string.

        Fitness is defined by the number of matching chars between
        the string and finalString
        """
        fitness = 0
        for i in range(len(str)):
            fitness += str[i] == self.__finalString[i]
        return fitness

    def _print(self, str):
        print(str)

    def _cross(self, str1, str2):
        """Cross the given strings."""
        return Utils.mixStrings(str1, str2)

    def _mutate(self, str):
        """Mutate the given strings."""
        return Utils.changeOneChar(str)

    def _endCondition(self, str):
        """Finish if the most fit string maches finalString."""
        return str == self.__finalString

    def _finish(self, generations, time, time2, time3, time4, time5):
        """Super calls this functions when algorithm finishes."""
        print(f"Found string   : {self.__finalString}")
        # Super finish will display general informations about the search
        super()._finish(generations, time, time2, time3, time4, time5)
