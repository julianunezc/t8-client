# Spectrum Comparator

This project implements an algorithm to calculate the spectrum from a waveform and compare it with the spectrum obtained from the T8. The result is a plot showing both spectra superimposed: the calculated one and the one obtained from the T8.

## Installation

### 1. Clone the repository
   ```bash
   git clone https://github.com/julianunezc/T8Spectrum.git
   cd T8Spectrum
   ```

### 2. Install Poetry

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

### 3. Install the dependencies
With Poetry installed, you can now install the project dependencies. Simply run:

```bash
poetry install
```
This will create a virtual environment and install all the required dependencies defined in the `pyproject.toml` file.

## Project Structure

The project is organized into several directories and files:

### 1. Main algorithm (`main.py`)
   This file contains the core logic of the project. It handles the process of loading a waveform, generating its spectrum, and comparing it with the reference spectrum obtained from the T8 device. The key steps involved in this process are:

- **Load the Waveform and T8 Spectrum Data**: The waveform data is loaded from API using the Waveform class, and the reference T8 spectrum is loaded using the Spectrum class.

- **Define the frequency Range**: The frequency range is determined based on the minimum and maximum frequency values in the T8 spectrum.

- **Calculate the Spectrum of the Waveform**: The waveform's spectrum is generated using the `wave.create_spectrum(fmin, fmax) ` method, which applies a Hanning window, zero-padding, and computes the Fast Fourier Transform (FFT). The calculated spectrum is filtered within a frequency range defined by the T8 spectrum.

- **Plot the Spectra**: A plot is generated showing both the calculated waveform spectrum and the reference T8 spectrum, with the two spectra superimposed for easy comparison.

### 2. Utils Directory (`utils\`)
   This directory contains auxiliary modules that handle various tasks necessary for the spectrum comparison. It includes:

  - **`functions.py`**: Contains helper functions for tasks such as extracting and converting data from the T8 API, handling environment variables, and other utility methods.
   
  - **`waveform.py`**: Contains the `Waveform` class, which represents a waveform with attributes such as time, amplitude, sampling rate, and windowed and padded amplitude values. It includes a method to load waveform data from API, applies a Hanning window to the waveform, use a method to zero-pads the windowed waveform to increase frequency resolution in the FFT, and prints a string representation showing the waveform instance. The `create_spectrum()` method performs the FFT on the padded waveform, computes frequency and amplitude values, and returns a Spectrum object with the computed values.
  
      This class is essential for preparing the waveform data and calculating its frequency spectrum, which can then be compared with the T8 device's reference spectrum.
   
   - **`spectrum.py`**: Contains the `Spectrum` class, which represents a spectrum with frequency values in Hz and their corresponding amplitudes, along with filtered versions of those arrays used after applying frequency range filtering. It includes methods to load spectrum data from API, filter the frequency and amplitude arrays to keep only those within a specified range, and prints a string representation showing the frequency range in Hz and the number of samples.

### 3. Tests Directory (`tests\`)
This folder contains the unit and integration tests for the project.
   - **`test_waveform.py`**: This file contains the unit tests for the `Waveform` class. It verifies the correct initialization of the class as well as the functionality of applying a Hanning window to the amplitudes.

## Main Algorithm

The core of the spectrum comparison algorithm is implemented in the `main.py` script. The process involves the following key steps:

- **Loading the Waveform and T8 Spectrum Data**: The waveform data is loaded from API using the Waveform class, and the reference T8 spectrum is loaded using the Spectrum class.

- **Processing the Waveform**: The waveform undergoes processing to generate its frequency spectrum using the `create_spectrum()` method. The spectrum is calculated by applying a Hanning window and zero-padding to the waveform, then computing the Fast Fourier Transform (FFT). The calculated spectrum is filtered within a frequency range defined by the T8 spectrum.

- **Comparison Plot**: A plot is generated showing both the calculated waveform spectrum and the reference T8 spectrum, with the two spectra superimposed for easy comparison.

## Running the Project

This project requires the following environment variables to access T8 data. You must define them in a .env file at the root of the project. The credentials are confidential, so make sure to obtain them from the appropriate source.

- `T8_USER`: Username to access T8 data.
- `T8_PASSWORD`: Password associated with the T8 user account
- `DEVICE_IP`: The IP address of the T8 device.
- `MACHINE`: The identifier or name of the machine being monitored by the T8 device.
- `POINT`: The specific measurement point on the machine that is being monitored.
- `PMODE`: The measurement mode or operational mode of the device or machine.
- `TIME`: The specific timestamp (in the format 'DD-MM-YYYY HH:MM:SS').

The main script (`main`) simply calls `compare_two_spectra`, making it easy to execute the comparison. To run it and visualize the results:

1. Ensure you have the required environment variables.

2. Place the .env file at the root directory of the project.
3. Run the script:
```bash
poetry run python main.py
```

After running the script, a plot will be generated comparing the spectrum calculated from the waveform and the reference T8 spectrum.



