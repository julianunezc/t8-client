import os
import sys
from base64 import b64decode
from datetime import datetime, timezone
from struct import unpack
from zlib import decompress

import numpy as np
import requests
from dotenv import load_dotenv


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


def get_unix_timestamp_from_str(time_str: str) -> int:
    """Converts a UTC date and time from an environment variable to a Unix timestamp.

    Parameters:
    time_str (str): Date and time in the format 'DD-MM-YYYY HH:MM:SS'.

    Returns:
    int: The Unix timestamp.
    """
    utc_time = datetime.strptime(time_str, "%d-%m-%Y %H:%M:%S")
    utc_time = utc_time.replace(tzinfo=timezone.utc)
    return int(utc_time.timestamp())


def get_str_from_unix_timestamp(timestamp: int) -> str:
    """Converts a Unix timestamp to a UTC date and time string.

    Parameters:
    timestamp (int): The Unix timestamp.

    Returns:
    str: The date and time in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S")


def load_env_variables() -> tuple:
    """Loads environment variables from .env file.

    Returns:
    tuple: A tuple containing user, password and host.
    """
    load_dotenv()
    user = os.getenv("T8_USER")
    password = os.getenv("T8_PASSWORD")
    host = os.getenv("HOST")
    return user, password, host


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
