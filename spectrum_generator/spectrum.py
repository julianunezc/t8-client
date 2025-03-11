import os

import numpy as np
import pandas as pd


class Spectrum:
    """A class to represent a spectrum."""

    def __init__(self, freq: np.ndarray, amp: np.ndarray):
        """Initializes a Waveform object with time and amplitude arrays.

        Parameters:
        time (np.ndarray): Contains the frequency values (in Hz).
        amp (np.ndarray): Contains the amplitude values corresponding to the freqs.

        """
        self.freq = freq
        self.amp = amp

    @classmethod
    def from_csv(cls, filename: str):
        """Loads spectrum data from a CSV file."""
        current_dir = os.path.dirname(__file__)
        filepath = os.path.join(current_dir, "..", "data", filename)
        data = pd.read_csv(filepath)
        freq = data["freq"].to_numpy()
        amp = data["amp"].to_numpy()
        return cls(freq, amp)

    def __repr__(self) -> str:
        """Visualization of the spectrum.

        Returns:
        str: A string representation of the Waveform instance.

        """
        return (
            f"Spectrum(freq_range=({self.freq[0]:.2f}Hz, {self.freq[-1]:.2f}Hz), "
            f"num_samples={len(self.freq)})"
        )
