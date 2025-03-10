"""."""

import os

import numpy as np
import pandas as pd


class Waveform:
    """A class to represent a waveform."""

    def __init__(self, time: np.ndarray, amp: np.ndarray):
        """Initializes a Waveform object with time and amplitude arrays.

        Parameters:
        time (np.ndarray): A numpy array containing the time values.
        amp (np.ndarray): A numpy array containing the amplitude values.

        """
        self.time = time
        self.amp = amp

    @classmethod
    def from_csv(cls, filename: str):
        """Loads waveform data from a CSV file."""
        filepath = os.path.join("data", filename)
        data = pd.read_csv(filepath)
        return cls(data["t"], data["amp"])


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
        filepath = os.path.join("data", filename)
        data = pd.read_csv(filepath)
        return cls(data["freq"], data["amp"])


def main():
    pass


if __name__ == "__main__":
    main()
