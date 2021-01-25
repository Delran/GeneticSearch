"""Docstring for GeneticSearch Module."""
import numbers
import random
import math
import time

import Utils


class GeneticSearch():
    """Create one for each genetic search."""

    __population = None
    __mutateRate = None
    __selectRate = None
    __finalString = None

    def __init__(self, finalString, population, mutateRate, selectRate):
        """Take four arguments, result, population, mutation, selection."""
        """Result is the string the algorithm will be looking for"""

        self.__validate(finalString, population, mutateRate, selectRate)

    def __validate(self, finalString, population, mutateRate, selectRate):
        """Validate genetic search parameters."""
        self.__valid = True
        if finalString is None or type(finalString) is not str:
            print("Result is None or not a string")
            self.__valid = False
        if population is None or not isinstance(population, numbers.Number):
            print("Population is None or not a number")
            self.__valid = False
        if mutateRate is None or not isinstance(mutateRate, numbers.Number):
            print("MutateRate is None or not a number")
            self.__valid = False
        if selectRate is None or not isinstance(selectRate, numbers.Number):
            print("SelectRate is None or not a number")
            self.__valid = False

        if self.__valid is False:
            return

        self.__finalString = finalString
        self.__population = population
        self.__mutateRate = mutateRate
        self.__selectRate = selectRate

    def start(self):
        """Start the genetic search."""
        if not self.__valid:
            print("Parameters are not valid")
            return

        start = time.perf_counter()

        strs = []
        # Initial population
        for i in range(self.__population):
            strs.append(Utils.generateRandomString(len(self.__finalString)))

        generations = 0
        while True:
            # We sort the population their fitness
            strs = Utils.quickSort(strs,
                                   sortFn=lambda str: self.__getFitness(str))
            print(strs[0])
            if strs[0] == self.__finalString:
                break

            selection = self.__select(strs)
            crossed = self.__cross(selection)
            strs = self.__mutate(crossed)
            generations += 1

        end = time.perf_counter()
        self.__finish(generations, end - start)

    def __finish(self, generations, time):
        print(f"Found string   : {self.__finalString}")
        print(f"Population     : {self.__population}")
        print(f"Selection rate : {self.__selectRate}")
        print(f"Mutation rate  : {self.__mutateRate}")
        print(f"Generations    : {generations}")
        print(f"Elapsed time   : {time:0.4f} seconds")

    def __print(self, list):
        for str in list:
            print(str)

    def __getFitness(self, str):
        """Docstring for getFitness."""
        fitness = 0
        for i in range(len(str)):
            fitness += str[i] == self.__finalString[i]
        return fitness

    def __select(self, strList):
        """Docstring for select."""
        # List is sorted by fitness so not much to do here
        return strList[:math.floor(self.__selectRate*self.__population)]

    def __cross(self, strList):
        """Docstring for crosss."""
        crossed = []
        reproduced = 0
        randLength = len(strList)
        while reproduced < self.__population:
            rand1 = random.randrange(randLength)
            rand2 = random.randrange(randLength)
            child = Utils.mixStrings(strList[rand1], strList[rand2])
            crossed.append(child)
            reproduced += 1
        return crossed

    def __mutate(self, strList):
        """Docstring for mutate."""
        mutated = []

        mutateChance = int(self.__mutateRate * 100)
        for str in strList:
            rand = random.randint(0, 100)
            if rand <= mutateChance:
                # Mutate
                str = Utils.changeOneChar(str)
            mutated.append(str)
        return mutated
