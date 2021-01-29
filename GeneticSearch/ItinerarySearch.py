"""Genetic algorithm for itinerary optimization."""

import random
import numbers
import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# To adjust towns name in pyplot
from adjustText import adjust_text

from GeneticSearch.AbstractSearch import AbstractSearch
from GeneticSearch.Towns import Town
from MarkovGenerator.TownNameGenerator import TownNameGenerator

import GeneticSearch.Towns as Towns
# import Utils


class ItinerarySearch(AbstractSearch):
    """docstring for ItinerarySearch."""

    # Markov chains generator for French town names
    __nameGenerator = TownNameGenerator(7, 30)

    def __init__(self, towns, boardSize, end,
                 population, mutateRate, selectRate):
        """Init the algorithm and generate the plan.

        Towns is the number of town to generate
        """
        self.__end = end
        self.__nbTowns = towns
        self.__boardSize = boardSize
        self.__last = math.inf
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
            if self.__end:
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
        """Start function, calls the super's start."""
        if not self._valid:
            return

        self.__generateTowns(self.__nbTowns)

        super().start()

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

            # Keep track of the coordinates so we can avoid
            # adding two towns at the same coordinates
            allCoords.append(coords)
            # Giving i as ID
            town = Town(i, coords)
            self.__towns.append(town)
            town.name = nameList[i]

    # Redefining fitness sorting function to sort descending
    def _sortFunction(self, pivot, item):
        pivot = self._fitness(pivot)
        item = self._fitness(item)
        if item > pivot:
            return 1
        elif item < pivot:
            return -1
        else:
            return 0

    def _finish(self, generations, time, selectTime, crossTime, mutateTime):

        figure = plt.figure()
        _xlim = (0, self.__boardSize[0])
        _ylim = (0, self.__boardSize[1])
        ax = figure.add_subplot(111, xlim=_xlim, ylim=_ylim)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        self.__ln, = ax.plot(0, 0, '-o')

        # abscissa = []
        # ordinates = []
        # mostFit = self._generationMostFits[-1]
        # for id in mostFit:
        #     abscissa.append(self.__towns[id].x)
        #     ordinates.append(self.__towns[id].y)

        # self.__ln.set_data(abscissa, ordinates)

        abscissa = []
        ordinates = []
        mostFit = self._generationMostFits[0]
        for id in mostFit:
            abscissa.append(self.__towns[id].x)
            ordinates.append(self.__towns[id].y)

        texts = []
        for x, y, id in zip(abscissa, ordinates, mostFit):
            texts.append(ax.text(x, y, self.__towns[id].name, color='green'))

        for txt in figure.texts:
            txt.remove()
        # Adusting text so it don't overlap
        # adjust_text(texts, autoalign='y',
        #             only_move={'points': 'xy', 'text': 'xy'},
        #             force_points=0.5, force_text=0.5,
        #             arrowprops=dict(arrowstyle="-", color='b', lw=0.8))

        ani = FuncAnimation(figure, self.__update, blit=True, interval=200)
        plt.show()
        super()._finish(generations, time, selectTime, crossTime, mutateTime)

    __updateGeneration = 0

    def __update(self, frame):
        if self.__updateGeneration >= len(self._generationMostFits):
            return self.__ln,

        abscissa = []
        ordinates = []
        mostFit = self._generationMostFits[self.__updateGeneration]
        self.__updateGeneration += 1
        for id in mostFit:
            abscissa.append(self.__towns[id].x)
            ordinates.append(self.__towns[id].y)

        texts = []
        for x, y, id in zip(abscissa, ordinates, mostFit):
            texts.append(plt.text(x, y, self.__towns[id].name))

        # # Adusting text so it don't overlap
        # adjust_text(texts, autoalign='y',
        #             only_move={'points': 'xy', 'text': 'xy'},
        #             force_points=0.5, force_text=0.5,
        #             arrowprops=dict(arrowstyle="-", color='b', lw=0.8))

        self.__ln.set_data(abscissa, ordinates)
        return self.__ln,

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
        """Cross two itinerary, returns the crossed itinerary.

        Itineraries are crossed by replacing half of the the breeder2 genetic
        into the breeder1 and modifying breeder1's genetic material to respect
        the rule of towns that should only be visited once
        """
        # Keeping reminder for odd itineraries
        length = len(breeder1)
        quotient = int(length / 2)
        remainder = length % 2

        # Range from zero to half the itinerary + remainder
        start = random.randrange(quotient + remainder)
        # end at start + half the itinerary whtiout remainder
        end = start + quotient
        crossed = []
        tmpRange = range(length)
        possible = list(tmpRange)
        for i in tmpRange:
            if start <= i <= end:
                crossed.append(-1)
            else:
                item = breeder2[i]
                crossed.append(item)
                possible.remove(item)
        # Iterate and replace -1 with breeder1's towns id
        # only if the id is not already in the crossed item
        for i in tmpRange:
            if crossed[i] == -1:
                item = breeder1[i]
                if item not in crossed:
                    crossed[i] = item
                    possible.remove(item)

        leftovers = len(possible)
        if leftovers >= 1:
            # Iterate one last time to replace leftovers randomly
            # crossing can't be perfect because each town must be
            # visited only once
            for i in tmpRange:
                if crossed[i] == -1:
                    index = random.randrange(leftovers)
                    crossed[i] = possible.pop(index)
                leftovers = len(possible)
                if leftovers == 0:
                    break
        return crossed

    def _fitness(self, item):
        totalDist = 0.0
        for i in range(len(item)-1):
            src = self.__towns[item[i]]
            dist = self.__towns[item[i+1]]
            totalDist += Towns.distance(src, dist)
        return totalDist

    def _select(self, list, descending=True):
        return super()._select(list, descending=False)

    def _mutate(self, toMutate):
        # Must return mutated item

        # Randrange up to len - 1 as we will invert item at i and i+1
        index = random.randrange(len(toMutate)-1)
        tmp = toMutate[index]
        toMutate[index] = toMutate[index + 1]
        toMutate[index + 1] = tmp
        return toMutate

    def _endCondition(self, mostFit):
        # Must returns true if end conditions are met
        fitness = self._fitness(mostFit)
        if fitness == self.__last:
            self.__endCount += 1
            if self.__endCount >= self.__end:
                return True
        else:
            self.__endCount = 0
        self.__last = fitness
        return False

    def _print(self, item):
        # Defines how an item of the list should be printed
        printStr = ""
        for i in range(len(item)):
            if i != 0:
                printStr += '->'
            printStr += str(item[i])
        print(printStr)
