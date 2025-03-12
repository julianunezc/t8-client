import numpy as np
import pytest

from spectra_comparator.waveform import Waveform


# Fixture for sample waveform
@pytest.fixture
def sample_waveform():
    time = np.array([1, 2, 3, 4, 5])
    amp = np.array([0, 1, -1, 0, 3])
    srate = 1024
    return Waveform(time, amp, srate)


def test_waveform_init(sample_waveform):
    assert np.array_equal(sample_waveform.time, np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(sample_waveform.amp, np.array([0, 1, -1, 0, 3]))
    assert sample_waveform.srate == 1024
    assert sample_waveform.windowed_amps is None


def test_waveform_hanning_window(sample_waveform):
    sample_waveform.hanning_window()

    hanning_window = np.hanning(len(sample_waveform.amp))
    expected_results = sample_waveform.amp * hanning_window

    assert np.allclose(sample_waveform.windowed_amps, expected_results)
