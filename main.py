"""Main file for Genetic search algorithm."""
from GeneticSearch.StringSearch import StringSearch
from GeneticSearch.ItinerarySearch import ItinerarySearch


def main():
    """Entry point function for genetic search algorithm."""
    # The higher the population is, the less number of generation
    # is needed to find the solution
    population = 1000
    # Higher rate of mutation give more stable results
    # while lower rate of mutation results are better
    # in best cases and worst in the worses cases
    mutationRate = 70
    # Lower selection rates works best combined with high population
    # High selection rates on high population can severly increase
    # computation time
    selectionRate = 30
    search = StringSearch("Je cherche cette phrase",
                          population, mutationRate, selectionRate)
    # search.start()

    searchIt = ItinerarySearch(20, (1000, 1000), 10,
                               population, mutationRate, selectionRate)
    searchIt.start()


if __name__ == "__main__":
    # Execute only if run as a script
    main()
