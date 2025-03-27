"""
This script accumulates all necessary functions for the execution of
`main.py`in t8_client/ and `compare_spectra.py` in spectra_comparison/.

This file contains the following functions:

    * fetch_data - Fetches data from the API with authentication.
    * get_unix_timestamp_from_iso - Converts an ISO 8601 string in local time
                                    to a Unix timestamp.
    * get_iso_from_unix_timestamp - Converts a Unix timestamp to an ISO 8601 string
                                    in local time.
    * get_timestamps - Retrieves available waveform or spectrum timestamps.
    * zint_to_float - Decodes a ZINT-encoded string into a NumPy array of floats.
"""

import sys
import zoneinfo
from base64 import b64decode
from datetime import datetime
from struct import unpack
from zlib import decompress

import numpy as np
import requests


def fetch_data(url: str, user: str, passw: str) -> dict:
    """
    Fetches the data from the API using authentication.

    Parameters
    ----------
    url : str
        The URL of the API to fetch data from.
    user : str
        User for authentication.
    passw : str
        Password for authentication.

    Returns
    -------
    dict
        The JSON response from the API parsed into a dictionary.

    Raises
    ------
    SystemExit
        If the response status code is not 200, the function exits the program.
    """
    response = requests.get(url, auth=(user, passw))
    if response.status_code != 200:  # noqa: PLR2004
        print(f"Error getting data. Status code: {response.status_code}")
        sys.exit(1)
    return response.json()


def get_unix_timestamp_from_iso(iso_str: str) -> int:
    """
    Converts an ISO 8601 datetime string in local time to a Unix timestamp.

    Parameters
    ----------
    iso_str : str
        Datetime value in ISO 8601 format ('YYYY-MM-DDTHH:MM:SS') in local time.

    Returns
    -------
    int
        Unix timestamp corresponding to the provided ISO 8601 datetime.
    """
    dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S")
    local_timezone = zoneinfo.ZoneInfo("Europe/Madrid")
    dt = dt.replace(tzinfo=local_timezone)
    return int(dt.timestamp())


def get_iso_from_unix_timestamp(timestamp: int) -> str:
    """
    Converts a Unix timestamp to an ISO 8601 datetime string in local time.

    Parameters
    ----------
    timestamp : int
        The Unix timestamp to be converted.

    Returns
    -------
    str
        ISO 8601 datetime string ('YYYY-MM-DDTHH:MM:SS') based on the local time.
    """
    local_tz = zoneinfo.ZoneInfo("Europe/Madrid")
    dt = datetime.fromtimestamp(timestamp, tz=local_tz)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def get_timestamps(url: str, user: str, passw: str) -> list:
    """
    Fetches available waveform or spectrum timestamps from the API.

    Parameters
    ----------
    url : str
        The URL of the API to fetch data from.
    user : str
        User for authentication.
    passw : str
        Password for authentication.

    Returns
    -------
    list
        A list of available timestamps in ISO 8601 format ('YYYY-MM-DDTHH:MM:SS').
    """
    # Fetch the waveform data from the API
    data = fetch_data(url, user, passw)

    timestamps = []
    for item in data.get("_items", []):
        url_self = item["_links"]["self"]  # Obtaining the corresponding URL
        parts = url_self.split("/")  # URL parts
        ts = parts[-1]  # Extracting last part of the URL
        formatted_ts = get_iso_from_unix_timestamp(int(ts))  # Converting to ISO format
        timestamps.append(formatted_ts)
    return timestamps


def zint_to_float(encoded_str: str) -> np.ndarray:
    """
    Converts a ZINT-encoded string to a numpy array of floats.

    Parameters
    ----------
    encoded_str : str
        A ZINT-encoded string (base64 encoded compressed string).

    Returns
    -------
    np.ndarray
        A numpy array of floats decoded from the ZINT-encoded string.
    """
    decoded_data = decompress(b64decode(encoded_str.encode()))
    return np.array(
        [
            unpack("h", decoded_data[i * 2 : (i + 1) * 2])[0]
            for i in range(int(len(decoded_data) / 2))
        ],
        dtype="f",
    )
