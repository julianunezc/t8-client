import csv
import os
from typing import Self

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

import t8_client.functions as fun
from t8_client.spectrum import Spectrum as Sp


class Waveform:
    """A class to represent a waveform."""

    def __init__(self, time: np.ndarray, amp: np.ndarray, srate: float) -> None:
        """
        Initializes a Waveform object with time and amplitude arrays.

        Parameters
        ----------
        time : np.ndarray
            Contains the time values of the waveform.
        amp : np.ndarray
            Contains the amplitude values of the waveform.
        srate : float
            The sampling rate of the waveform.
        windowed_amps : np.ndarray, optional
            Contains the windowed amplitude values applying
            a Hanning window, initialized as None.
        padded_amps : np.ndarray, optional
            Contains the windowed waveform with zero padding applied,
            initialized as None.
        """
        self.time = time
        self.amp = amp
        self.srate = srate
        self.windowed_amps = None
        self.padded_amps = None

    @classmethod
    def from_api(
        cls: type[Self],
        params: dict[str, str],
    ) -> Self:
        """
        Loads waveform data from API using the provided parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing the necessary parameters:
            user : str
                User to connect with.
            passw : str
                Password to connect with.
            host : str
                The host address of the API.
            machine : str
                Machine tag.
            point : str
                Point tag.
            pmode : str
                Processing mode tag.
            date : str
                Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.

        Returns
        -------
        Waveform
            A Waveform object with the data loaded from the API.
        """
        # Extract parameters
        user = params["user"]
        passw = params["passw"]
        host = params["host"]
        machine = params["machine"]
        point = params["point"]
        pmode = params["pmode"]
        date = params["date"]

        # Calculate Unix timestamp using the provided date and time
        timestamp = fun.get_unix_timestamp_from_iso(date)

        # API URL
        url = f"http://{host}/rest/waves/{machine}/{point}/{pmode}/{timestamp}"

        # Fetch the waveform data from the API
        r = fun.fetch_data(url, user, passw)

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

    def save_to_csv(self, filename: str) -> None:
        """
        Saves the time in ms and amplitude data of the waveform into a CSV file.
        The file is always saved in the './output/reports/' directory.

        Parameters
        ----------
        filename : str
            The name of the file where the waveform data will be saved.
        """
        output_dir = os.path.join(os.getcwd(), "output", "reports")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["time", "amp"])
            writer.writerows(zip(self.time, self.amp))

    def plot_data(self, filename: str) -> None:
        """
        Plots and saves the waveform data (time vs amplitude) as a PNG.
        The file is always saved in the './output/figures/' directory.

        Parameters
        ----------
        filename : str
            The name of the file where the waveform plot will be saved as a PNG.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.time, self.amp, label="Waveform")
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.title("Waveform Data")
        plt.legend()

        output_dir = os.path.join(os.getcwd(), "output", "figures")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{filename}.png")

        # Save the figure to the file
        plt.savefig(file_path, format="png")
        plt.show()

    def hanning_window(self) -> None:
        """
        Applies a Hanning window to the waveform and
        updates the windowed_amps attribute.
        """
        num_samples = len(self.amp)
        window = np.hanning(num_samples)
        self.windowed_amps = self.amp * window

    def zero_padding(self) -> None:
        """
        Applies zero padding to the windowed waveform
        and updates the padded_amps attribute.
        """
        if self.windowed_amps is None:
            raise ValueError("Waveform must be windowed before applying zero padding.")

        n = len(self.windowed_amps)
        padded_len = 2 ** np.ceil(np.log2(n)).astype(int)
        self.padded_amps = np.pad(self.windowed_amps, (0, padded_len - n), "constant")

    def create_spectrum(self, fmin: float, fmax: float) -> Sp:
        """
        Creates the spectrum of a waveform.

        Parameters
        ----------
        fmin : float
            The minimum frequency for filtering.
        fmax : float
            The maximum frequency for filtering.

        Returns
        -------
        Spectrum
            The spectrum of the waveform.
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
        spectrum = Sp(freq=freqs, amp=amps)

        # Filter frequencies within the given range
        spectrum.apply_filter(fmin, fmax)

        return spectrum

    def __repr__(self) -> str:
        """
        Visualization of the waveform.

        Returns
        -------
        str
            A string representation of the Waveform instance.
        """
        return f"Waveform(srate={self.srate}, duration={self.time[-1]}ms)"
