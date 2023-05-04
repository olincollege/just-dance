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
    score_data = get_leaderboard(filename)
    return score_data[-1][-1]


