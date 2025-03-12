# Spectrum Comparator

This project implements an algorithm to calculate the spectrum from a waveform and compare it with the spectrum obtained from the T8. The final result is a graph with the two spectra superimposed: the calculated one and the one obtained from the T8.

## Installation

### 1. Clone the repository
   ```bash
   git https://github.com/julianunezc/T8Spectrum.git
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

### 1. **Data Directory (`data\`)**
   This folder contains the scripts for decoding both the spectrum and the waveform, as well as their respective CSV files and graphical representations. It also includes a script for timestamp conversion:
   
- **`spectrum_decode.py`**: Script to decode the spectrum data.
- **`waveform_decode.py`**: Script to decode the waveform data.
- **`timestamp.py`**: Script for converting timestamps from UTC to Unix format.
- **`.csv`**: CSV files corresponding to the decoded spectrum and waveform.
- **`.png`**: Graphical representations of the spectrum and waveform as PNG files.

### 2. **Core Directory (`spectra_comparator\`)**
   This is the core module of the project, containing the main logic for calculating and comparing the spectra. It includes:

  - **`compare_spectra.py`**: The main script that calculates the spectrum from the waveform and compares it with the spectrum obtained from the T8. The output is a graph with both spectra superimposed.
   
  - **`waveform.py`**: Contains the `Waveform` class, which represents a waveform with attributes such as time, amplitude, sampling rate and windowed amplitude values. It includes a method to load waveform data from CSV file, apply a Hanning window to the waveform, and a string representation showing the waveform instance.
   
   - **`spectrum.py`**: Contains the `Spectrum` class, which represents a spectrum with frequency values in Hz and their corresponding amplitudes. It includes methods to load spectrum data from CSV file and a string representation showing the frequency range in Hz and the number of samples.

### 3. Tests Directory (`tests\`)
This folder contains the unit and integration tests for the project.
   - **`test_waveform.py`**: This file contains the unit tests for the `Waveform` class. It verifies the correct initialization of the class as well as the functionality of applying a Hanning window to the amplitudes.

## Main Algorithm

The core of the spectrum comparison algorithm is implemented in the `compare_two_spectra` function. The process involves the following key steps:

- **Loading the Waveform and T8 Spectrum Data**: The waveform data is loaded from a CSV file using the Waveform class, and the reference T8 spectrum is loaded using the Spectrum class.

- **Windowing and Zero Padding**: The waveform is windowed using a Hanning window, and zero padding is applied to increase frequency resolution.

- **Fast Fourier Transform (FFT)**: The FFT is applied to the windowed and padded waveform to calculate the spectrum.

- **Filtering Frequency Range**: The calculated spectrum is filtered to keep frequencies between 2.5 Hz and 2000 Hz for comparison purposes.

- **Comparison Plot**: A plot is generated showing both the calculated waveform spectrum and the reference T8 spectrum, with the two spectra superimposed for easy comparison.

## Running the Project

The main function (`main`) simply calls `compare_two_spectra` with predefined filenames, making it easy to execute the comparison. To run it and visualize the results:

1. Ensure you have the required waveform and spectrum data available in CSV format.
- The waveform data should include time (t) and amplitude (amp) columns.
- The spectrum data should include frequency (freq) and amplitude (amp) columns.

2. Place the waveform data CSV and the reference spectrum CSV into the `data\` folder.
3. Run the script:
```bash
poetry run python spectra_comparator/compare_spectra.py
```

By default, the script will use the filenames `wave_data.csv` and `spectrum_data.csv` located in the `data\` folder. If your files have different names, you can modify the wave_filename and t8_filename variables in the main() function inside the `compare_spectra.py` script.

After running the script, a plot will be generated comparing the spectrum calculated from the waveform and the reference T8 spectrum.



