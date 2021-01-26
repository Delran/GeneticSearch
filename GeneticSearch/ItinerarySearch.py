"""Genetic algorithm for itinerary optimization."""
from GeneticSearch.AbstractSearch import AbstractSearch

import Utils


class ItinerarySearch(AbstractSearch):
    """docstring for ItinerarySearch."""

    def __init__(self, towns, precision, population, mutateRate, selectRate):
        """Init the algorithm and generate the plan.

        Towns is the number of town to generate
        """
        self.__precision = precision
        self.__towns = towns
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
            if not isinstance(self.__towns, int) or self.__towns is None:
                self._valid = False
                print("Number of towns must be an integer")
            if self.__precision:
                pass

    

    def _generatePopulation(self):
        # Must return the generated population as a list
        pass

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
