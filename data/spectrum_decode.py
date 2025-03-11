"""This script retrieves spectrum data from a remote device via a REST API,
decodes the compressed data (using different compression formats: zint, zlib, or b64),
applies a scaling factor to the amplitude, and saves the decoded frequency and
amplitude data to a CSV file.
Additionally, it generates a plot of the spectrum with frequency on the X-axis and
amplitude on the Y-axis."""

import os
import sys
from base64 import b64decode
from struct import unpack
from zlib import decompress

import matplotlib.pyplot as pylab
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

FORMAT = "zint"  # zint | zlib | b64
DEVICE_IP = "lzfs45.mirror.twave.io/lzfs45"
USER = os.getenv("T8_USER")
PASS = os.getenv("T8_PASSWORD")

MACHINE = "LP_Turbine"
POINT = "MAD31CY005"
PMODE = "AM1"


def zint_to_float(raw):
    d = decompress(b64decode(raw.encode()))
    return np.array(
        [unpack("h", d[i * 2 : (i + 1) * 2])[0] for i in range(int(len(d) / 2))],
        dtype="f",
    )


def zlib_to_float(raw):
    d = decompress(b64decode(raw.encode()))
    return np.array(
        [unpack("f", d[i * 4 : (i + 1) * 4])[0] for i in range(int(len(d) / 4))],
        dtype="f",
    )


def b64_to_float(raw):
    return np.fromstring(b64decode(raw.encode()), dtype="f")


decode_format = {"zint": zint_to_float, "zlib": zlib_to_float, "b64": b64_to_float}

url = f"http://{DEVICE_IP}/rest/spectra/{MACHINE}/{POINT}/{PMODE}/1555007154"


r = requests.get(url, auth=(USER, PASS))
if r.status_code != 200:
    print("Error getting data. Status code: ", r.status_code)
    sys.exit(1)

# Extract json fields
fmin = r.json().get("min_freq", 0)
fmax = r.json()["max_freq"]
factor = r.json()["factor"]
raw = r.json()["data"]

sp = decode_format[FORMAT](raw)

# Apply numeric factor
sp *= factor

# Get frequency axis
freq = np.linspace(fmin, fmax, len(sp))

# Save data to csv file
df = pd.DataFrame({"freq": freq, "amp": sp})
csv_filepath = os.path.join("data", "spectrum_data.csv")
df.to_csv(csv_filepath, index=False)

pylab.plot(freq, sp)
pylab.xlabel("Frequency (Hz)")  # Label for X-axis
pylab.ylabel("Amplitude")  # Label for Y-axis
pylab.title("Spectrum Plot")  # Title of the plot
pylab.grid(True)
pylab.show()
