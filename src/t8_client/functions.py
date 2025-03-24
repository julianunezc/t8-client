"""
This script accumulates all necessary functions for the execution of
`main.py` and `compare_spectra.py`.

This file contains the following functions:

    * fetch_data - fetches data from the API with authentication.
    * get_unix_timestamp_from_iso - converts an ISO 8601 string to a Unix timestamp.
    * get_iso_from_unix_timestamp - converts a Unix timestamp to an ISO 8601 string.
    * get_timestamps - retrieves available waveform or spectrum timestamps.
    * zint_to_float - decodes a ZINT-encoded string into a NumPy array of floats.
"""

import sys
from base64 import b64decode
from datetime import datetime, timezone
from struct import unpack
from zlib import decompress

import numpy as np
import requests


def fetch_data(url: str, user: str, passw: str) -> dict:
    """
    Fetches the data from the API.

    Parameters
    ----------
    url : str
        The URL of the API to fetch data from.
    user : str
        User to connect with.
    passw : str
        Password to connect with.

    Returns
    -------
    dict
        The JSON response from the API as a dictionary.

    Raises
    ------
    SystemExit
        If the response status code is not 200, the function exits the program.
    """
    response = requests.get(url, auth=(user, passw))
    if response.status_code != 200:
        print(f"Error getting data. Status code: {response.status_code}")
        sys.exit(1)
    return response.json()


def get_unix_timestamp_from_iso(time_str: str) -> int:
    """
    Converts an ISO 8601 date and time string to a Unix timestamp.

    Parameters
    ----------
    time_str : str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.

    Returns
    -------
    int
        The Unix timestamp representing the given date and time.
    """
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def get_iso_from_unix_timestamp(timestamp: int) -> str:
    """
    Converts a Unix timestamp to an ISO 8601 date and time string.

    Parameters
    ----------
    timestamp : int
        The Unix timestamp to convert.

    Returns
    -------
    str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    iso_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return iso_time.strftime("%Y-%m-%dT%H:%M:%S")


def get_timestamps(url: str, user: str, passw: str) -> list:
    """
    Fetches the list of available waveform or spectrum timestamps from the API.

    Parameters
    ----------
    url : str
        The URL of the API to fetch data from.
    user : str
        User to connect with.
    passw : str
        Password to connect with.

    Returns
    -------
    list
        A list of timestamps in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    # Fetch the waveform data from the API
    r = fetch_data(url, user, passw)

    timestamps = []
    for item in r.get("_items", []):
        url_self = item["_links"]["self"]  # Obtaining the corresponding URL
        parts = url_self.split("/")  # URL parts
        ts = parts[-1]  # Extracting last part of the URL
        formatted_ts = get_iso_from_unix_timestamp(int(ts))  # Converting to ISO format
        timestamps.append(formatted_ts)
    return timestamps


def zint_to_float(raw: str) -> np.ndarray:
    """
    Converts a ZINT-encoded string to a numpy array of floats.

    Parameters
    ----------
    raw : str
        A ZINT-encoded string (base64 encoded compressed string).

    Returns
    -------
    np.ndarray
        A numpy array of floats decoded from the ZINT-encoded string.
    """
    d = decompress(b64decode(raw.encode()))
    return np.array(
        [unpack("h", d[i * 2 : (i + 1) * 2])[0] for i in range(int(len(d) / 2))],
        dtype="f",
    )
