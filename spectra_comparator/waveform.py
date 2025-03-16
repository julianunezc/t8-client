import os

import numpy as np
from common import fetch_data, get_unix_timestamp, zint_to_float
from dotenv import load_dotenv


class Waveform:
    """A class to represent a waveform."""

    def __init__(self, time: np.ndarray, amp: np.ndarray, srate: float):
        """Initializes a Waveform object with time and amplitude arrays.

        Attributes:
        time (np.ndarray): A numpy array containing the time values of the waveform.
        amp (np.ndarray): A numpy array containing the amplitude values of the waveform.
        srate (float): The sampling rate of the waveform.
        windowed_amps (np.ndarray): A numpy array containing
                                    the windowed amplitude values.
        """
        self.time = time
        self.amp = amp
        self.srate = srate
        self.windowed_amps = None

    @classmethod
    def from_api(
        cls, year: int, month: int, day: int, hour: int, minute: int, second: int
    ):
        """Loads waveform data from API using parameters stored in environment variables
        and returns a Waveform object.

        Parameters:
        year (int): The year.
        month (int): The month.
        day (int): The day.
        hour (int): The hour.
        minute (int): The minute.
        second (int): The second.

        Returns:
        Waveform: A Waveform object with the data loaded from the API.
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
        url = f"http://{DEVICE_IP}/rest/waves/{MACHINE}/{POINT}/{PMODE}/{timestamp}"

        # Fetch the waveform data from the API
        r = fetch_data(url, USER, PASS)

        # Process the waveform data
        srate = float(r["sample_rate"])
        factor = float(r.get("factor", 1))
        raw = r["data"]

        # Decode and convert the waveform data
        wave = zint_to_float(raw)
        wave *= factor

        # Create time array
        time = np.linspace(0, len(wave) / srate, len(wave)) * 1000  # Convert to ms

        return cls(time, wave, srate)

    def hanning_window(self):
        """Applies a Hanning window to the waveform.
        Stores the windowed amplitude values."""
        num_samples = len(self.amp)
        window = np.hanning(num_samples)
        self.windowed_amps = self.amp * window

    def __repr__(self) -> str:
        """Visualization of the waveform.

        Returns:
        str: A string representation of the Waveform instance.
        """
        return f"Waveform(srate={self.srate}, duration={self.time[-1]}ms)"
