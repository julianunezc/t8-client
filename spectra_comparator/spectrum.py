import os

import numpy as np
from common import fetch_data, get_unix_timestamp, zint_to_float
from dotenv import load_dotenv


class Spectrum:
    """A class to represent a spectrum."""

    def __init__(self, freq: np.ndarray, amp: np.ndarray):
        """Initializes a Spectrum object with time and amplitude arrays.

        Parameters:
        time (np.ndarray): Contains the frequency values (in Hz).
        amp (np.ndarray): Contains the amplitude values corresponding to the freqs.
        """
        self.freq = freq
        self.amp = amp

    @classmethod
    def from_api(
        cls, year: int, month: int, day: int, hour: int, minute: int, second: int
    ):
        """Loads spectrum data from API using parameters stored in environment variables
        and returns a Spectrum object.

        Parameters:
        year (int): The year.
        month (int): The month.
        day (int): The day.
        hour (int): The hour.
        minute (int): The minute.
        second (int): The second.

        Returns:
        Spectrum: A Spectrum object with the data loaded from the API.
        """
        # Get configuration values from .env
        load_dotenv()
        USER = os.getenv("T8_USER")
        PASS = os.getenv("T8_PASSWORD")
        DEVICE_IP = os.getenv("DEVICE_IP")
        MACHINE = os.getenv("MACHINE")
        POINT = os.getenv("POINT")
        PMODE = os.getenv("PMODE")

        # Calculate Unix timestamp using the provided date and time
        timestamp = get_unix_timestamp(year, month, day, hour, minute, second)

        # API URL
        url = f"http://{DEVICE_IP}/rest/spectra/{MACHINE}/{POINT}/{PMODE}/{timestamp}"

        # Fetch the spectrum data from the API
        r = fetch_data(url, USER, PASS)

        # Process the spectrum data
        fmin = r.get("min_freq", 0)
        fmax = r["max_freq"]
        factor = r["factor"]
        raw = r["data"]

        # Decode and convert the spectrum data
        sp = zint_to_float(raw)
        sp *= factor

        # Create freq array
        freq = np.linspace(fmin, fmax, len(sp))

        return cls(freq, sp)

    def __repr__(self) -> str:
        """Visualization of the spectrum.

        Returns:
        str: A string representation of the Spectrum instance.

        """
        return (
            f"Spectrum(freq_range=({self.freq[0]:.2f}Hz, {self.freq[-1]:.2f}Hz), "
            f"num_samples={len(self.freq)})"
        )
