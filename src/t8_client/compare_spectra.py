"""This script compares the spectrum of a waveform with a reference spectrum obtained
from the T8 device.
It processes the waveform, applies a Hanning window and zero padding,
computes its spectrum using FFT, and then plots both the calculated spectrum and
the reference T8 spectrum on the same graph for comparison.
"""

import matplotlib.pyplot as plt

from t8_client.spectrum import Spectrum as sp
from t8_client.waveform import Waveform as wf


def compare_two_spectra(machine: str, point: str, pmode: str, date: str) -> None:
    """Compares the spectrum of a waveform with a reference spectrum (T8).

    Parameters:
    machine (str): The machine identifier.
    point (str): The point identifier.
    pmode (str): The mode (e.g., AM1).
    date (str): The date and time in 'DD-MM-YYYY HH:MM:SS' format.

    Returns:
    None: This function creates a plot comparing both spectra.
    """
    # Charge the waveform and the reference spectrum
    wave = wf.from_api(machine, point, pmode, date)
    t8_spectrum = sp.from_api(machine, point, pmode, date)

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
    """Main function to compare the spectrum of a wave and a reference T8 spectrum."""
    # Define the parameters (machine, point, pmode, date)
    machine = "LP_Turbine"
    point = "MAD31CY005"
    pmode = "AM1"
    date = "2019-04-11T18:25:54"

    compare_two_spectra(machine, point, pmode, date)


if __name__ == "__main__":
    main()
