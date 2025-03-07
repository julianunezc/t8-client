"""This script retrieves spectrum data from a remote device via a REST API,
decodes the compressed data (using different compression formats: zint, zlib, or b64),
applies a scaling factor to the amplitude, and saves the decoded frequency and
amplitude data to a CSV file.
Additionally, it generates a plot of the spectrum with frequency on the X-axis and
amplitude on the Y-axis."""

import csv
import sys
from base64 import b64decode
from struct import unpack
from zlib import decompress

import matplotlib.pyplot as pylab
import numpy as np
import requests

FORMAT = "zint"  # zint | zlib | b64
DEVICE_IP = "lzfs45.mirror.twave.io/lzfs45"
USER = ""  # User required
PASS = ""  # Password required

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

url = f"http://{DEVICE_IP}/rest/spectra/{MACHINE}/{POINT}/{PMODE}/1555007154?array_fmt={FORMAT}"


r = requests.get(url, auth=(USER, PASS))
if r.status_code != 200:
    print("Error getting data. Status code: ", r.status_code)
    sys.exit(1)

ret = r.json()

# Extract json fields
fmin = ret.get("min_freq", 0)
fmax = ret["max_freq"]
factor = ret["factor"]
raw = ret["data"]

sp = decode_format[FORMAT](raw)

# Apply numeric factor
sp *= factor

# Get frequency axis
freq = np.linspace(fmin, fmax, len(sp))

# Save the data to a CSV file
with open("data/spectrum_data.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["freq", "amp"])
    # Write data rows (frequency and corresponding spectrum values)
    writer.writerows(zip(freq, sp))

# Get frequency axis
pylab.plot(freq, sp)
pylab.xlabel("Frequency (Hz)")  # Label for X-axis
pylab.ylabel("Amplitude")  # Label for Y-axis
pylab.title("Spectrum Plot")  # Title of the plot
pylab.grid(True)
pylab.show()
