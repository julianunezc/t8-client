import sys
from base64 import b64decode
from datetime import datetime, timezone
from struct import unpack
from zlib import decompress

import numpy as np
import requests


def fetch_data(url: str, user: str, password: str) -> dict:
    """Fetches the data from the API.

    Parameters:
    url (str): The URL of the API.
    user (str): The username for the API.
    password (str): The password for the API.

    Returns:
    dict: The JSON response from the API.
    """
    response = requests.get(url, auth=(user, password))
    if response.status_code != 200:
        print(f"Error getting data. Status code: {response.status_code}")
        sys.exit(1)
    return response.json()


def get_unix_timestamp(
    year: int, month: int, day: int, hour: int, minute: int, second: int
) -> int:
    """Converts a UTC date and time to a Unix timestamp.

    Parameters:
    year (int): The year.
    month (int): The month.
    day (int): The day.
    hour (int): The hour.
    minute (int): The minute.
    second (int): The second.

    Returns:
    int: The Unix timestamp.
    """
    utc_time = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
    return int(utc_time.timestamp())


def zint_to_float(raw: str) -> np.ndarray:
    """Converts a ZINT-encoded string to a numpy array of floats.

    Parameters:
    raw (str): A ZINT-encoded string.

    Returns:
    np.ndarray: A numpy array of floats.
    """
    d = decompress(b64decode(raw.encode()))
    return np.array(
        [unpack("h", d[i * 2 : (i + 1) * 2])[0] for i in range(int(len(d) / 2))],
        dtype="f",
    )
