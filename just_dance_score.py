import csv


def get_leaderboard(filename):
    """
    Retrieve the leaderboard data from a CSV file.

    Args:
        filename (str): The name of the CSV file to read
            the leaderboard data from.

    Returns:
        A list of lists representing the leaderboard data read from
         the CSV file. Each sub-list represents a row of the CSV file.
    """
    data = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    return data


def give_current_score(filename):
    """
    This function reads the leaderboard data from a file with the
    given filename and returns the last (current) score in the leaderboard.

    Args:
        filename (str): The name of the file containing the leaderboard data.

    Returns:
        int: The last (current) score in the leaderboard.
        """
    score_data = get_leaderboard(filename)
    return int(score_data[-1][-1])


