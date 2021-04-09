"""Return the pathname of the KOS root directory."""

import backend.analysis.point_finding as point_finding
import numpy as np
import matplotlib.pyplot as plot
import pytest

@pytest.fixture(name='time')
def fixture_time():
    """Time arrays used for testing"""
    return np.arange(0, 80, 0.01)

@pytest.fixture(name='disp')
def fixture_disp(time):
    """Displacement arrays used for testing"""
    return np.sin(time)

@pytest.fixture(name='peaks')
def fixture_peaks(time, disp):
    """Peak arrays used for testing"""
    return point_finding.find_peaks(time, disp)

def test_find_peaks(time, disp, peaks):
    """Testing peaks"""
    # plot.plot(time, disp);plot.plot(peaks[0], peaks[1]);plot.show()
    assert np.all([.9999 <= amplitude <= 1.0001 for amplitude in peaks[1]])
    return 

def test_find_basepoints(time, disp, peaks):
    """Return the pathname of the KOS root directory."""
    ind = point_finding.find_basepoints(time, disp, peaks)
    plot.plot(time, disp);plot.plot(time[ind], disp[ind]);plot.show()
    return 6

