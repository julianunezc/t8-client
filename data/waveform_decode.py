"""This script retrieves wave data from a remote machine via a REST API,
decodes the compressed data (using different compression formats: zint, zlib, or b64),
applies a scaling factor to the signal, and saves the decoded data to a CSV file.
Additionally, it generates a plot of the signal with time on the X-axis and
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

url = f"http://{DEVICE_IP}/rest/waves/{MACHINE}/{POINT}/{PMODE}/1555007154?array_fmt={FORMAT}"

r = requests.get(url, auth=(USER, PASS))
if r.status_code != 200:
    print("Error getting data. Status code: ", r.status_code)
    sys.exit(1)

ret = r.json()

# Extract json fields
srate = float(ret["sample_rate"])
factor = float(ret.get("factor", 1))
raw = ret["data"]

wave = decode_format[FORMAT](raw)

# Apply numeric factor
wave *= factor

# Get time axis
t = np.linspace(0, len(wave) / srate, len(wave))

# Save data to csv file
df = pd.DataFrame({"t": t, "amp": wave})
csv_filepath = os.path.join("data", "wave_data.csv")
df.to_csv(csv_filepath, index=False)

pylab.plot(t, wave)
pylab.xlabel("Time")  # Label for X-axis
pylab.ylabel("Amplitude")  # Label for Y-axis
pylab.title("Waveform Plot")  # Title of the plot
pylab.grid(True)
pylab.show()
