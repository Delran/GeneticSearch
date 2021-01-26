"""Abstract class for Genetic Search algorithm."""

from abc import ABC, abstractmethod
import numbers
import random
import math
import time

import Utils


class AbstractSearch(ABC):
    """Create one for each genetic search."""

    _population = None
    _mutateRate = None
    _selectRate = None
    _valid = True

    def __init__(self, population, mutateRate, selectRate):
        """Take four arguments, result, population, mutation, selection."""
        """Result is the string the algorithm will be looking for"""
        self._population = population
        self._mutateRate = mutateRate
        self._selectRate = selectRate

        self._validate()

    def _validate(self):
        """Validate genetic search parameters."""
        valid = True
        if self._population is None or not isinstance(self._population,
                                                      numbers.Number):
            print("Population is None or not a number")
            valid = False
        if self._mutateRate is None or not isinstance(self._mutateRate,
                                                      numbers.Number):
            print("MutateRate is None or not a number")
            valid = False
        if self._selectRate is None or not isinstance(self._selectRate,
                                                      numbers.Number):
            print("SelectRate is None or not a number")
            valid = False

        return valid

    def start(self):
        """Start the genetic search."""
        if not self._valid:
            print("Parameters are not valid")
            return

        start = time.perf_counter()

        # Initial population
        # Defined by child class
        items = self._generatePopulation()

        generations = 0
        while True:
            # We sort the population their fitness
            items = Utils.quickSort(items,
                                    sortFn=lambda item: self._fitness(item))
            # Polymorphic print and endCondition functions
            self._print(items[0])
            if self._endCondition(items[0]):
                break

            selection = self.__select(items)
            crossed = self.__getCrossed(selection)
            items = self.__getMutated(crossed)
            generations += 1

        end = time.perf_counter()
        # Polymorphic finish function
        self._finish(generations, end - start)

    def _finish(self, generations, time):
        print(f"Population     : {self._population}")
        print(f"Selection rate : {self._selectRate}")
        print(f"Mutation rate  : {self._mutateRate}")
        print(f"Generations    : {generations}")
        print(f"Elapsed time   : {time:0.4f} seconds")

    def __print(self, list):
        for item in list:
            print(item)

    def __getCrossed(self, list):
        """Return a list of randomly crossed items.

        This function chooses randomly which items should be crossed
        until the desired population is reached.
        Items are crossed using the self._cross abstract function.
        """
        crossed = []
        reproduced = 0
        randLength = len(list)
        while reproduced < self._population:
            rand1 = random.randrange(randLength)
            rand2 = random.randrange(randLength)
            child = self._cross(list[rand1], list[rand2])
            crossed.append(child)
            reproduced += 1
        return crossed

    def __getMutated(self, list):
        """Return a list with mutated elements.

        This function calls the self._mutate abstract function
        at a random rate defined by the self._mutateRate variable
        """
        mutated = []

        mutateChance = int(self._mutateRate * 100)
        for item in list:
            rand = random.randint(0, 100)
            if rand <= mutateChance:
                # Mutate
                item = self._mutate(item)
            mutated.append(item)
        return mutated

    def __select(self, list):
        """Only keeps the desired rate of the most fit items."""
        # List is sorted by fitness so not much to do here
        return list[:math.floor(self._selectRate*self._population)]

    @abstractmethod
    def _print(self, item):
        # Defines how an item of the list should be printed
        ...

    @abstractmethod
    def _cross(self, breeder1, breeder2):
        # Must return crossed item
        ...

    @abstractmethod
    def _fitness(self, item):
        ...

    @abstractmethod
    def _mutate(self, toMutate):
        # Must return mutated item
        ...

    @abstractmethod
    def _generatePopulation(self):
        # Must return the generated population as a list
        ...

    @abstractmethod
    def _endCondition(self, mostFit):
        # Must returns true if end conditions are met
        ...
