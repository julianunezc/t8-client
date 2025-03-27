"""
This script compares the spectrum of a waveform with a reference spectrum obtained
from the T8 device.

It uses environment variables for API authentication (USER, PASSW, HOST).

This file contains the following functions:

    * compare_two_spectra - Fetches and compares the spectra from both the T8 device
                            and the waveform, then plots them.
    * main - Main function of the script.
"""

import os

import matplotlib.pyplot as plt

from t8_client.spectrum import Spectrum as Sp
from t8_client.waveform import Waveform as Wf


def compare_two_spectra(machine: str, point: str, pmode: str, date: str) -> None:
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
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format
        based on local time (Madrid, Spain).
    """
    params = {
        "user": os.getenv("USER"),
        "passw": os.getenv("PASSW"),
        "host": os.getenv("HOST"),
        "machine": machine,
        "point": point,
        "pmode": pmode,
        "date": date,
    }

    wave = Wf.from_api(params)
    t8_spectrum = Sp.from_api(params)

    fmin, fmax = t8_spectrum.freq.min(), t8_spectrum.freq.max()

    calculated_spectrum = wave.create_spectrum(fmin, fmax)

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

    # Customize the plot and display it
    plt.title("Spectrum Comparison", fontsize=14)
    plt.xlabel("Frequency (Hz)", fontsize=12)
    plt.ylabel("Amplitude", fontsize=12)
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


def main() -> None:
    """
    Main function to compare the spectrum of a waveform with its T8 reference spectrum.
    """
    # Define the parameters for the comparison (machine, point, pmode, date)
    machine = "LP_Turbine"
    point = "MAD31CY005"
    pmode = "AM1"
    date = "2019-04-12T20:27:24"

    # Compare the spectra
    compare_two_spectra(machine, point, pmode, date)


if __name__ == "__main__":
    main()
