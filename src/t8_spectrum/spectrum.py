import numpy as np

import t8_spectrum.functions as fun


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
    def from_api(cls):
        """Loads spectrum data from API using parameters stored in environment variables
        and returns a Spectrum object.

        Returns:
        Spectrum: A Spectrum object with the data loaded from the API.
        """
        # Get configuration values from .env
        USER, PASS, DEVICE_IP, MACHINE, POINT, PMODE, TIME = fun.load_env_variables()

        # Calculate Unix timestamp using the provided date and time
        timestamp = fun.get_unix_timestamp(TIME)

        # API URL
        url = f"http://{DEVICE_IP}/rest/spectra/{MACHINE}/{POINT}/{PMODE}/{timestamp}"

        # Fetch the spectrum data from the API
        r = fun.fetch_data(url, USER, PASS)

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
