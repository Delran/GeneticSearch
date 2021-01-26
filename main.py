"""Main file for Genetic search algorithm."""
from GeneticSearch.StringSearch import StringSearch


def main():
    """Entry point function for genetic search algorithm."""
    population = 500
    mutationRate = 0.5
    selectionRate = 0.25
    search = StringSearch("Je cherche ça phrase",
                          population, mutationRate, selectionRate)
    search.start()


if __name__ == "__main__":
    # Execute only if run as a script
    main()
