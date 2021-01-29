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

    _generationMostFits = []

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

        elif 0.0 <= self._mutateRate <= 100.0:
            self._mutateRate /= 100
        else:
            print(f"{self._mutateRate} is an incorrect value "
                  "for a mutation rate, value should be given in percent")
            valid = False

        if self._selectRate is None or not isinstance(self._selectRate,
                                                      numbers.Number):
            print("SelectRate is None or not a number")
            valid = False
        elif 0.0 <= self._selectRate <= 100.0:
            self._selectRate /= 100
            nbSelect = self._selectRate * self._population
            if nbSelect < 1:
                print("The selection rate is too small "
                      "for the given population, "
                      "either increase the selection rate or the population\n"
                      f"{self._selectRate} * {self._population} = {nbSelect}")

                valid = False
        else:
            print(f"{self._selectRate} is an incorrect value "
                  "for a selection rate, value should be given in percent")
            valid = False

        return valid

    def start(self):
        """Start the genetic search."""
        if not self._valid:
            print("Parameters are not valid")
            return

        self._selectTime = 0
        self._crossTime = 0
        self._mutateTime = 0

        start = time.perf_counter()

        # Initial population
        # Defined by child class
        items = self._generatePopulation()

        self._generations = 0

        while True:
            # Implemented a quickSort before realising that python list had
            # a builtin timsort, list.sort is on average 5 times faster than
            # my own shitty quickSort
            # items = Utils.quickSort(items, sortFn=self._sortFunction)

            timer = time.perf_counter()

            selection = self._select(items)

            self._selectTime += time.perf_counter() - timer
            timer = time.perf_counter()

            # Polymorphic print and endCondition functions
            mostFit = selection[0]

            self._generationMostFits.append(mostFit)
            self._print(mostFit)
            print(self._fitness(mostFit))
            if self._endCondition(mostFit):
                break

            crossed = self.__getCrossed(selection)

            self._crossTime += time.perf_counter() - timer
            timer = time.perf_counter()

            items = self.__getMutated(crossed)

            self._mutateTime += time.perf_counter() - timer

            self._generations += 1

        self._time = time.perf_counter() - start
        # Polymorphic finish function
        self._finish()

    def _sortFunction(self, pivot, item):
        pivot = self._fitness(pivot)
        item = self._fitness(item)
        if item < pivot:
            return 1
        elif item > pivot:
            return -1
        else:
            return 0

    def _finish(self):
        print(f"Population     : {self._population}")
        print(f"Selection rate : {self._selectRate}")
        print(f"Mutation rate  : {self._mutateRate}")
        print(f"Generations    : {self._generations}")
        print(f"Elapsed time   : {self._time:0.4f} seconds")
        print(f"Time in select : {self._selectTime:0.4f} seconds")
        print(f"Time in cross  : {self._crossTime:0.4f} seconds")
        print(f"Time in mutate : {self._mutateTime:0.4f} seconds")

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

    # Select is implemented by default
    def _select(self, list, descending=True):
        """Only keeps the desired rate of the most fit items."""
        list.sort(key=lambda item: self._fitness(item), reverse=descending)
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
