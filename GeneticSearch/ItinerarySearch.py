"""Genetic algorithm for itinerary optimization."""

import random
import numbers

from GeneticSearch.AbstractSearch import AbstractSearch
from GeneticSearch.Town import Town
from MarkovGenerator.TownNameGenerator import TownNameGenerator

import Utils


class ItinerarySearch(AbstractSearch):
    """docstring for ItinerarySearch."""

    # Markov chains generator for French town names
    __nameGenerator = TownNameGenerator(7, 50)

    def __init__(self, towns, boardSize, precision,
                 population, mutateRate, selectRate):
        """Init the algorithm and generate the plan.

        Towns is the number of town to generate
        """
        self.__precision = precision
        self.__nbTowns = towns
        self.__boardSize = boardSize
        super(ItinerarySearch, self).__init__(population,
                                              mutateRate,
                                              selectRate)

    def _validate(self):
        """Validate the type of the given parameters.

        Towns must be an Integer
        """
        # Calling super.validate() for pop, mutation and select
        self._valid = super()._validate()
        if self._valid:
            if not isinstance(self.__nbTowns, int) or self.__nbTowns is None:
                self._valid = False
                print("Number of towns must be an integer")
            if self.__precision:
                pass
            if type(self.__boardSize) is tuple:
                tmp = self.__boardSize
                if (isinstance(tmp[0], numbers.Number)
                   and isinstance(tmp[1], numbers.Number)):
                    pass
            else:
                self._valid = False
                print("Board size must be a tuple of numbers")

    def start(self):
        if not self._valid:
            return

        self.__generateTowns(self.__nbTowns)
        # super().start()

    def __generateTowns(self, nbTowns):
        nameList = self.__nameGenerator.getMarkovList(nbTowns)
        self.__towns = []
        allCoords = []
        for i in range(nbTowns):
            coords = (0, 0)
            while True:
                x = random.randrange(self.__boardSize[0])
                y = random.randrange(self.__boardSize[1])
                coords = (x, y)
                if coords not in allCoords:
                    break

            allCoords.append(coords)
            town = Town(coords)
            self.__towns.append(town)
            town.name = nameList[i]

        self._generatePopulation()

    def _generatePopulation(self):
        """Generate random itinerary between towns.

        Itinerary must pass by a town only once
        """
        itineraries = []
        for i in range(self._population):
            itinerary = []
            tmpRange = range(self.__nbTowns)
            possible = list(tmpRange)
            for j in tmpRange:
                index = random.randrange(len(possible))
                itinerary.append(possible.pop(index))
            itineraries.append(itinerary)
        return itineraries

    def _cross(self, breeder1, breeder2):
        # Must return crossed item
        pass

    def _fitness(self, item):
        pass

    def _mutate(self, toMutate):
        # Must return mutated item
        pass

    def _endCondition(self, mostFit):
        # Must returns true if end conditions are met
        pass

    def _print(self, item):
        # Defines how an item of the list should be printed
        pass
