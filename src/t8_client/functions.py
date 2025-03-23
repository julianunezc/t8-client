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


def get_unix_timestamp_from_iso(time_str: str) -> int:
    """Converts a ISO date and time string to a Unix timestamp.

    Parameters:
    time_str (str): Date and time in the format 'YYYY-MM-DDTHH:MM:SS'.

    Returns:
    int: The Unix timestamp.
    """
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def get_iso_from_unix_timestamp(timestamp: int) -> str:
    """Converts a Unix timestamp to a ISO date and time string.

    Parameters:
    timestamp (int): The Unix timestamp.

    Returns:
    str: The date and time in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    iso_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return iso_time.strftime("%Y-%m-%dT%H:%M:%S")


def get_timestamps(url: str, machine: str, point: str, pmode: str) -> list:
    """Fetches the list of available waveform or spectrum timestamps from the API.

    Parameters:
    url (str): The URL to fetch the data.
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Pmode value.

    Returns:
    list: A list of timestamps in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    # Get configuration values from .env file
    user, password, _ = load_env_variables()

    # Fetch the waveform data from the API
    r = fetch_data(url, user, password)

    timestamps = []
    for item in r.get("_items", []):
        url_self = item["_links"]["self"]  # Obtaining the corresponding URL
        parts = url_self.split("/")  # URL parts
        ts = parts[-1]  # Extracting last part of the URL
        formatted_ts = get_iso_from_unix_timestamp(int(ts))  # Converting to ISO format
        timestamps.append(formatted_ts)
    return timestamps


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
