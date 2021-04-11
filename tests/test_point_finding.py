"""Return the pathname of the KOS root directory."""

import backend.analysis.point_finding as point_finding
import numpy as np
import matplotlib.pyplot as plot
import pytest

import sys
sys.setrecursionlimit(10000000) 

@pytest.fixture(name='time')
def fixture_time():
    """Time arrays used for testing"""
    return np.arange(0, 40, 0.001)

@pytest.fixture(name='disp')
def fixture_disp(time):
    """Displacement arrays used for testing"""
    return np.sin(3*time)

@pytest.fixture(name='peaks')
def fixture_peaks(time, disp):
    """Peak arrays used for testing"""
    return point_finding.find_peaks(time, disp)

@pytest.fixture(name='base_indicies')
def fixture_base_indicies(disp, peaks):
    return point_finding.find_basepoints_frontpoints(disp, peaks)[0]

def test_find_peaks(time, disp, peaks):
    """Testing peaks"""
    #plot.plot(time, disp);plot.plot(peaks[0], 0*peaks[1]);plot.show()
    #assert np.all([1.569 <= time % np.pi <= 1.571 for time in peaks[0]])
    assert np.all([.99 <= amplitude <= 1.01 for amplitude in peaks[1]])
    return 

def test_find_basepoints_frontpoints(time, disp, peaks):
    """Return the pathname of the KOS root directory."""
    ind, frontpoints = point_finding.find_basepoints_frontpoints(disp, peaks)
    return 6

def test_find_analysispoints(time, disp, peaks, base_indicies):
    inds = point_finding.find_analysispoints(disp, peaks, base_indicies)
    plot.plot(time, disp);plot.plot(time[inds], disp[inds], marker='o');plot.show()
    return