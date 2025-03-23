import csv
import os

import numpy as np

import t8_client.functions as fun


class Spectrum:
    """A class to represent a spectrum."""

    def __init__(self, freq: np.ndarray, amp: np.ndarray):
        """Initializes a Spectrum object with frequency and amplitude arrays.

        Parameters:
        freq (np.ndarray): Contains the frequency values (in Hz).
        amp (np.ndarray): Contains the amplitude values corresponding to the freqs.
        filtered_freq (np.ndarray): Contains the filtered frequency values (in Hz).
        filtered_amp (np.ndarray): Contains the filtered amplitude values
                                    corresponding to the freqs.
        """
        self.freq = freq
        self.amp = amp
        self.filtered_freq = None
        self.filtered_amp = None

    @classmethod
    def from_api(cls, machine: str, point: str, pmode: str, date: str):
        """Loads spectrum data from API using the provided parameters.

        Parameters:
        machine (str): The machine identifier.
        point (str): The point identifier.
        pmode (str): The mode (e.g., AM1).
        date (str): The date and time in 'YYYY-MM-DDTHH:MM:SS' format.

        Returns:
        Spectrum: A Spectrum object with the data loaded from the API.
        """
        # Get configuration values from .env
        user, password, host = fun.load_env_variables()

        # Calculate Unix timestamp using the provided date and time
        timestamp = fun.get_unix_timestamp_from_iso(date)

        # API URL
        url = f"http://{host}/rest/spectra/{machine}/{point}/{pmode}/{timestamp}"

        # Fetch the spectrum data from the API
        r = fun.fetch_data(url, user, password)

        # Process the spectrum data
        fmin = r.get("min_freq", 0)
        fmax = r["max_freq"]
        factor = r["factor"]
        raw = r["data"]

        # Decode and convert the spectrum data
        sp = fun.zint_to_float(raw)
        sp *= factor

        # Create freq array
        freq = np.linspace(fmin, fmax, len(sp))
        return cls(freq, sp)

    def save_to_csv(self, filename: str):
        """Saves the frequencies in Hz and amplitudes of the spectrum into a CSV file.
        The file is always saved in the './output/reports/' directory.

        Parameters:
        filename (str): The name of the file where the spectrum data will be saved.
        """
        output_directory = os.path.join(
            os.path.dirname(__file__), "../../output/reports/"
        )
        filename = os.path.join(output_directory, filename)
        os.makedirs(output_directory, exist_ok=True)
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["freq", "amp"])
            for freq, amp in zip(self.freq, self.amp):
                writer.writerow([freq, amp])

    def apply_filter(self, fmin: float, fmax: float):
        """Filters the frequencies and amplitudes within a specified range.

        Parameters:
        fmin (float): The minimum frequency for filtering.
        fmax (float): The maximum frequency for filtering.

        Returns:
        Updates the filtered_freq and filtered_amp attributes.
        """
        filter_mask = (self.freq >= fmin) & (self.freq <= fmax)
        self.filtered_freq = self.freq[filter_mask]
        self.filtered_amp = self.amp[filter_mask]

    def __repr__(self) -> str:
        """Visualization of the spectrum.

        Returns:
        str: A string representation of the Spectrum instance.
        """
        return (
            f"Spectrum(freq_range=({self.freq[0]:.2f}Hz, {self.freq[-1]:.2f}Hz), "
            f"num_samples={len(self.freq)})"
        )
