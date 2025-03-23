import csv
import os

import matplotlib.pyplot as plt
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
        output_dir = os.path.join(os.getcwd(), "output", "reports")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        # Save data into a CSV file
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["freq", "amp"])
            for freq, amp in zip(self.freq, self.amp):
                writer.writerow([freq, amp])

    def plot_data(self, filename: str = None):
        """Plots and saves the waveform data (time vs amplitude) as a PNG.

        Parameters:
        filename (str): The name of the file where the plot will be saved as a PNG.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.freq, self.amp, label="Spectrum")
        plt.xlim(0, max(self.freq))
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.title("Spectrum Data")
        plt.legend()

        output_dir = os.path.join(os.getcwd(), "output", "figures")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{filename}.png")

        # Save the figure to the file as a PNG
        plt.savefig(file_path, format="png")

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
