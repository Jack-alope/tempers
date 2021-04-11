"""Return the pathname of the KOS root directory."""

import sys
import backend.analysis.point_finding as point_finding
import numpy as np
#import matplotlib.pyplot as plot
import pytest

sys.setrecursionlimit(10000000)

@pytest.fixture(name='time')
def fixture_time():
    """Time arrays used for testing"""
    return np.arange(0, 40, 0.001)

@pytest.fixture(name='disp')
def fixture_disp(time):
    """Displacement arrays used for testing"""
    return np.sin(time) + 1

@pytest.fixture(name='peaks')
def fixture_peaks(time, disp):
    """Peak arrays used for testing"""
    return point_finding.find_peaks(time, disp)

@pytest.fixture(name='base_indicies')
def fixture_base_indicies(disp, peaks):
    """temp"""
    return point_finding.find_basepoints_frontpoints(disp, peaks)[0]

@pytest.fixture(name='front_indicies')
def fixture_front_indicies(disp, peaks):
    """Temp"""
    return point_finding.find_basepoints_frontpoints(disp, peaks)[1]

def test_find_peaks(peaks):
    """Testing peaks"""
    #plot.plot(time, disp);plot.plot(peaks[0], 0*peaks[1]);plot.show()
    #print(time % np.pi)
    assert np.all([1.56 <= time % np.pi <= 1.58 for time in peaks[0]])
    assert np.all([1.99 <= amplitude <= 2.01 for amplitude in peaks[1]])
    return 5

#def test_find_basepoints_frontpoints(time, disp, peaks):
#    """Return the pathname of the KOS root directory."""
    #ind, frontpoints =
    #point_finding.find_basepoints_frontpoints(disp, peaks)
#    return 6

#def test_find_analysispoints(time, disp, peaks, base_indicies, front_indicies):
#    """temp|"""
#    inds = point_finding.find_analysispoints(disp, peaks, base_indicies, front_indicies)[1]
#    plot.plot(time, disp)
#    for i in range(len(inds)):
#        plot.plot(time[inds[i]], disp[inds[i]], marker='o')
#    plot.show()
