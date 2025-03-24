"""
This script compares the spectrum of a waveform with a reference spectrum obtained
from the T8 device.

It uses environment variables for API authentication (`USER`, `PASSW`, `HOST`).

This file contains the following functions:

    * compare_two_spectra - fetches and compares the spectra from both the T8 device
                            and the waveform, and plots them.
    * main - main function of the script
"""

import os

import matplotlib.pyplot as plt

from t8_client.spectrum import Spectrum as sp
from t8_client.waveform import Waveform as wf


def compare_two_spectra(machine: str, point: str, pmode: str, date: str):
    """
    Compares the spectrum of a waveform with a reference spectrum (T8).

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.
    date : str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    # Charge the waveform and the reference spectrum
    user = os.getenv("USER")
    passw = os.getenv("PASSW")
    host = os.getenv("HOST")
    wave = wf.from_api(user, passw, host, machine, point, pmode, date)
    t8_spectrum = sp.from_api(user, passw, host, machine, point, pmode, date)

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

    plt.title("Spectrum Comparison", fontsize=14)
    plt.xlabel("Frequency (Hz)", fontsize=12)
    plt.ylabel("Amplitude", fontsize=12)
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


def main():
    """
    Main function to compare the spectrum of a wave and her reference T8 spectrum.
    """
    # Define the parameters (machine, point, pmode, date)
    machine = "LP_Turbine"
    point = "MAD31CY005"
    pmode = "AM1"
    date = "2019-04-11T18:25:54"

    compare_two_spectra(machine, point, pmode, date)


if __name__ == "__main__":
    main()
