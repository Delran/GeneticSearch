"""Main file for Genetic search algorithm."""
from GeneticSearch.StringSearch import StringSearch


def main():
    """Entry point function for genetic search algorithm."""
    population = 50
    mutationRate = 75
    selectionRate = 1.5
    search = StringSearch("Je cherche cette phrase",
                          population, mutationRate, selectionRate)
    search.start()


if __name__ == "__main__":
    # Execute only if run as a script
    main()
