"""
Testing for the point finding class
"""

#import matplotlib.pyplot as plt
import numpy as np
import pytest
from backend.analysis.tissues import TissuePoints

@pytest.fixture(name='tissue_object')
def fixture_tissue_object():
    """Initalize a sine graph based object"""
    time = np.arange(0, 40, 0.001)
    disp = np.sin(time) + 1
    return TissuePoints(13, 3, .1, .1, disp, time)

def test_find_peaks(tissue_object):
    """Testing peaks are where they schould be"""
    assert np.all([1.570 <= time % np.pi <= 1.572 for time in tissue_object.peaks[0]])
    assert np.all([1.999 <= amplitude <= 2.001 for amplitude in tissue_object.peaks[1]])

def test_find_basepoints_frontpoints(tissue_object):
    """Testing that basepoints and peaks are as expected"""
    assert np.all([-.001 <= point <= .001 for point in tissue_object.basepoints[1]])
    assert np.all([-.001 <= point <= .001 for point in tissue_object.frontpoints[1]])

def test_find_analysispoints(tissue_object):
    """Testing annalysis points disp is as expected"""
    assert np.all([.199 <= point <= .201 for point in tissue_object.contract_points[0][1]])
    assert np.all([.999 <= point <= 1.001 for point in tissue_object.contract_points[1][1]])
    assert np.all([1.799 <= point <= 1.801 for point in tissue_object.contract_points[2][1]])

    assert np.all([.199 <= point <= .201 for point in tissue_object.relax_points[0][1]])
    assert np.all([.999 <= point <= 1.001 for point in tissue_object.relax_points[1][1]])
    assert np.all([1.799 <= point <= 1.801 for point in tissue_object.relax_points[2][1]])

# TODO: Test fringe conditions for basepoints and frontpoints
