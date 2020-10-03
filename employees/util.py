import json


def load_data(path: str) -> dict:
    """Loading data from a file. Load all file because it is small.

    :param path: File path in `json` format
    :return: dict with list of user data
    """
    with open(path) as file:
        data = json.load(file)
    return data
