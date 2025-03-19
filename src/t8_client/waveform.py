import numpy as np
from scipy.fft import fft, fftfreq

import t8_client.functions as fun
from t8_client.spectrum import Spectrum


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
    def from_api(cls):
        """Loads waveform data from API using parameters stored in environment variables
        and returns a Waveform object.


        Returns:
        Waveform: A Waveform object with the data loaded from the API.
        """
        # Get configuration values from .env file
        USER, PASS, HOST, MACHINE, POINT, PMODE, DATE = fun.load_env_variables()

        # Calculate Unix timestamp using the provided date and time
        timestamp = fun.get_unix_timestamp(DATE)

        # API URL
        url = f"http://{HOST}/rest/waves/{MACHINE}/{POINT}/{PMODE}/{timestamp}"

        # Fetch the waveform data from the API
        r = fun.fetch_data(url, USER, PASS)

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

    def hanning_window(self):
        """Applies a Hanning window to the waveform.

        Returns:
        Updates the windowed_amps attribute."""
        num_samples = len(self.amp)
        window = np.hanning(num_samples)
        self.windowed_amps = self.amp * window

    def zero_padding(self):
        """Apply zero padding to the windowed waveform.

        Returns:
        Updates the padded_amps attribute.
        """
        if self.windowed_amps is None:
            raise ValueError("Waveform must be windowed before applying zero padding.")

        n = len(self.windowed_amps)
        padded_len = 2 ** np.ceil(np.log2(n)).astype(int)
        self.padded_amps = np.pad(self.windowed_amps, (0, padded_len - n), "constant")

    def create_spectrum(self, fmin: float, fmax: float) -> Spectrum:
        """Create the spectrum of a waveform.

        Parameters:
        fmin (float): The minimum frequency to consider.
        fmax (float): The maximum frequency

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
        sp = Spectrum(freq=freqs, amp=amps)

        # Filter frequencies within the given range
        sp.apply_filter(fmin, fmax)

        return sp

    def __repr__(self) -> str:
        """Visualization of the waveform.

        Returns:
        str: A string representation of the Waveform instance.
        """
        return f"Waveform(srate={self.srate}, duration={self.time[-1]}ms)"
