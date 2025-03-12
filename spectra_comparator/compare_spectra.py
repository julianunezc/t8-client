"""This script compares the spectrum of a waveform with a reference spectrum obtained
from the T8 device.
It processes the waveform, applies a Hanning window and zero padding,
computes its spectrum using FFT, and then plots both the calculated spectrum and
the reference T8 spectrum on the same graph for comparison.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from spectrum import Spectrum
from waveform import Waveform


def zero_padding(wave: Waveform, factor: int) -> np.ndarray:
    """Apply zero padding to a waveform.

    Parameters:
    wave (Waveform): The input waveform.
    factor (int): The zero padding factor.

    Returns:
    np.ndarray: The zero padded waveform.

    """
    if wave.windowed_amps is None:
        raise ValueError("Waveform must be windowed before applying zero padding.")

    padded_len = len(wave.windowed_amps) * factor
    num_samples = len(wave.windowed_amps)

    padded_amps = np.pad(wave.windowed_amps, (0, padded_len - num_samples), "constant")

    return padded_amps


def filter_frequency_range(
    freqs: np.ndarray, amps: np.ndarray, min_freq: float, max_freq: float
) -> tuple:
    """Filter the frequencies and amplitudes to keep only the values
    within a specified range.

    Parameters:
    freqs (np.ndarray): Frequencies.
    amps (np.ndarray): Amplitudes.
    min_freq (float): Minimum frequency for filtering.
    max_freq (float): Maximum frequency for filtering.

    Returns:
    tuple: Filtered frequencies and amplitudes.

    """
    freq_filter = (freqs >= min_freq) & (freqs <= max_freq)
    return freqs[freq_filter], amps[freq_filter]


def create_spectrum(wave: Waveform) -> Spectrum:
    """Create the spectrum of a waveform.

    Parameters:
    wave (Waveform): The wave to analyze.

    Returns:
    Spectrum: The spectrum of the waveform.

    """
    # Apply Hanning window
    if wave.windowed_amps is None:
        wave.hanning_window()

    # Apply zero padding
    padded_amps = zero_padding(wave, factor=4)

    # Compute the FFT
    amps = fft(padded_amps)
    freqs = fftfreq(len(padded_amps), 1.0 / wave.srate)  # Compute the frequencies
    # Keep only the positive frequencies
    positive_freqs = freqs[: len(freqs) // 2]
    positive_amps = np.abs(amps)[: len(freqs) // 2]

    # Filter frequencies within the given range
    filtered_freqs, filtered_amps = filter_frequency_range(
        positive_freqs, positive_amps, 2.5, 2000
    )

    return Spectrum(freq=filtered_freqs, amp=filtered_amps)


def compare_two_spectra(wave_filename: str, spectrum_filename: str) -> None:
    """Compares the spectrum of a waveform with a reference spectrum (T8).

    Parameters:
    wave_filename (str): The waveform CSV to analyze.
    t8_filename (str): The filename of the reference spectrum (T8) CSV.

    Returns:
    None: This function creates a plot comparing both spectra.
    """
    # Charge the waveform and the reference spectrum
    wave = Waveform.from_csv(wave_filename)
    t8_spectrum = Spectrum.from_csv(spectrum_filename)

    # Create the spectrum of the waveform
    calculated_spectrum = create_spectrum(wave)

    # Plot the spectra
    plt.figure(figsize=(10, 6))

    # Plot the waveform spectrum
    plt.plot(
        calculated_spectrum.freq,
        calculated_spectrum.amp,
        label="Calculated Spectrum",
        color="b",
        lw=2,
    )

    # Plot the reference spectrum
    plt.plot(
        t8_spectrum.freq,
        t8_spectrum.amp,
        label="T8 Spectrum",
        color="r",
        lw=2,
        linestyle="--",
    )

    plt.title("Comparación de Espectros", fontsize=14)
    plt.xlabel("Frecuencia (Hz)", fontsize=12)
    plt.ylabel("Amplitud", fontsize=12)
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


def main():
    """Main function to compare the spectra of a waveform and a reference T8 spectrum"""

    # Filenames
    wave_filename = "wave_data.csv"
    t8_filename = "spectrum_data.csv"

    # Compare the spectra
    compare_two_spectra(wave_filename, t8_filename)


if __name__ == "__main__":
    main()
