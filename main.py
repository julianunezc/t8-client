"""This script compares the spectrum of a waveform with a reference spectrum obtained
from the T8 device.
It processes the waveform, applies a Hanning window and zero padding,
computes its spectrum using FFT, and then plots both the calculated spectrum and
the reference T8 spectrum on the same graph for comparison.
"""

import matplotlib.pyplot as plt

from utils.spectrum import Spectrum
from utils.waveform import Waveform


def compare_two_spectra() -> None:
    """Compares the spectrum of a waveform with a reference spectrum (T8).

    Returns:
    None: This function creates a plot comparing both spectra.
    """
    # Charge the waveform and the reference spectrum
    wave = Waveform.from_api()
    t8_spectrum = Spectrum.from_api()

    # Define the frequency range to consider
    fmin = t8_spectrum.freq.min()
    fmax = t8_spectrum.freq.max()

    # Create the spectrum of the waveform
    calculated_spectrum = wave.create_spectrum(fmin, fmax)

    # Plot the spectra
    plt.figure(figsize=(10, 6))

    # Plot the waveform spectrum
    plt.plot(
        calculated_spectrum.filtered_freq,
        calculated_spectrum.filtered_amp,
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
    """Main function to compare the spectra of a wave and a reference T8 spectrum."""
    compare_two_spectra()


if __name__ == "__main__":
    main()
