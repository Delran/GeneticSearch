"""Main file for Genetic search algorithm."""
from GeneticSearch import GeneticSearch


def main():
    """Entry point function for genetic search algorithm."""
    population = 500
    mutationRate = 0.5
    selectionRate = 0.25
    search = GeneticSearch("Je cherche cette phrase",
                           population, mutationRate, selectionRate)
    search.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
