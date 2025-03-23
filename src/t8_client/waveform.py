import csv
import os

import numpy as np
from scipy.fft import fft, fftfreq

import t8_client.functions as fun
from t8_client.spectrum import Spectrum as sp


class Waveform:
    """A class to represent a waveform."""

    def __init__(self, time: np.ndarray, amp: np.ndarray, srate: float):
        """Initializes a Waveform object with time and amplitude arrays.

        Attributes:
        time (np.ndarray): A numpy array containing the time values of the waveform.
        amp (np.ndarray): A numpy array containing the amplitude values of the waveform.
        srate (float): The sampling rate of the waveform.
        windowed_amps (np.ndarray): A numpy array containing
                                    the windowed amplitude values applying
                                    a Hanning window.
        padded_amps (np.ndarray): A numpy array containing the windowed waveform
                                    with zero padding applied.
        """
        self.time = time
        self.amp = amp
        self.srate = srate
        self.windowed_amps = None
        self.padded_amps = None

    @classmethod
    def from_api(cls, machine: str, point: str, pmode: str, date: str):
        """Loads waveform data from API using the provided parameters.

        Parameters:
        machine (str): The machine identifier.
        point (str): The point identifier.
        pmode (str): The mode (e.g., AM1).
        date (str): The date and time in 'YYYY-MM-DDTHH:MM:SS' format.

        Returns:
        Waveform: A Waveform object with the data loaded from the API.
        """
        # Get configuration values from .env file
        user, password, host = fun.load_env_variables()

        # Calculate Unix timestamp using the provided date and time
        timestamp = fun.get_unix_timestamp_from_iso(date)

        # API URL
        url = f"http://{host}/rest/waves/{machine}/{point}/{pmode}/{timestamp}"

        # Fetch the waveform data from the API
        r = fun.fetch_data(url, user, password)

        # Process the waveform data
        srate = float(r["sample_rate"])
        factor = float(r.get("factor", 1))
        raw = r["data"]

        # Decode and convert the waveform data
        wave = fun.zint_to_float(raw)
        wave *= factor

        # Create time array
        time = np.linspace(0, len(wave) / srate, len(wave)) * 1000  # Convert to ms
        return cls(time, wave, srate)

    def save_to_csv(self, filename: str):
        """Saves the time in ms and amplitude data of the waveform into a CSV file.
        The file is always saved in the './output/reports/' directory.

        Parameters:
        filename (str): The name of the file where the data will be saved.
        """
        output_directory = os.path.join(
            os.path.dirname(__file__), "../../output/reports/"
        )
        filename = os.path.join(output_directory, filename)
        os.makedirs(output_directory, exist_ok=True)
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["time", "amp"])
            writer.writerows(zip(self.time, self.amp))

    def hanning_window(self):
        """Applies a Hanning window to the waveform.

        Returns:
        Updates the windowed_amps attribute.
        """
        num_samples = len(self.amp)
        window = np.hanning(num_samples)
        self.windowed_amps = self.amp * window

    def zero_padding(self):
        """Applies zero padding to the windowed waveform.

        Returns:
        Updates the padded_amps attribute.
        """
        if self.windowed_amps is None:
            raise ValueError("Waveform must be windowed before applying zero padding.")

        n = len(self.windowed_amps)
        padded_len = 2 ** np.ceil(np.log2(n)).astype(int)
        self.padded_amps = np.pad(self.windowed_amps, (0, padded_len - n), "constant")

    def create_spectrum(self, fmin: float, fmax: float) -> sp:
        """Creates the spectrum of a waveform.

        Parameters:
        fmin (float): The minimum frequency to consider.
        fmax (float): The maximum frequency to consider.

        Returns:
        Spectrum: The spectrum of the waveform.
        """
        # Apply Hanning window
        if self.windowed_amps is None:
            self.hanning_window()

        # Apply zero padding
        if self.padded_amps is None:
            self.zero_padding()

        # Compute the FFT
        amps = fft(self.padded_amps) * 2 * np.sqrt(2)
        amps = np.abs(amps) / len(amps)
        freqs = fftfreq(len(self.padded_amps), 1.0 / self.srate)  # Compute the freqs

        # Create a Spectrum object
        spectrum = sp(freq=freqs, amp=amps)

        # Filter frequencies within the given range
        spectrum.apply_filter(fmin, fmax)

        return spectrum

    def __repr__(self) -> str:
        """Visualization of the waveform.

        Returns:
        str: A string representation of the Waveform instance.
        """
        return f"Waveform(srate={self.srate}, duration={self.time[-1]}ms)"
