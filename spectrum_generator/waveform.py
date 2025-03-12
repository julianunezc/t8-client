import os

import numpy as np
import pandas as pd


class Waveform:
    """A class to represent a waveform."""

    def __init__(
        self,
        time: np.ndarray,
        amp: np.ndarray,
        srate: float = 5120,
    ):
        """Initializes a Waveform object with time and amplitude arrays.

        time (np.ndarray): A numpy array containing the time values of the waveform.
        amp (np.ndarray): A numpy array containing the amplitude values of the waveform.
        srate (float): The sampling rate of the waveform, default is 5120 Hz.
        windowed_amps (np.ndarray): A numpy array containing
                                    the windowed amplitude values.

        """
        self.time = time
        self.amp = amp
        self.srate = srate
        self.windowed_amps = None

    @classmethod
    def from_csv(cls, filename: str):
        """Loads waveform data from a CSV file."""
        current_dir = os.path.dirname(__file__)
        filepath = os.path.join(current_dir, "..", "data", filename)
        data = pd.read_csv(filepath)
        time = data["t"].to_numpy()
        amp = data["amp"].to_numpy()
        return cls(time, amp)

    def hanning_window(self) -> np.ndarray:
        """Applies a Hanning window to the waveform.
        
        Returns:
        np.ndarray: A numpy array containing the windowed amplitude values.

        """
        num_samples = len(self.amp)
        window = np.hanning(num_samples)
        self.windowed_amps = self.amp * window
        return self.windowed_amps

    def __repr__(self) -> str:
        """Visualization of the waveform.

        Returns:
        str: A string representation of the Waveform instance.

        """
        return f"Waveform(srate={self.srate}, duration={self.time[-1]}s)"
