"""
Testing for the calculations
"""

#import matplotlib.pyplot as plt
import numpy as np
from backend.analysis import calculations

def test_beating_freq(tissue_object):
    """Testing that the beatinf frequency is 1/period"""
    assert (1/(2*np.pi)-.001) <= \
        tissue_object.calculated_values['beating_freq'][0] <= (1/(2*np.pi)+.001)

def test_time_between(tissue_object):
    """Tetsing that time2pk is correct using known values"""
    assert np.pi - .001 <= \
        calculations.time_between(tissue_object.peaks[0], tissue_object.basepoints[0])[0] \
            <= np.pi + .001

    assert np.pi - .001 <= \
        calculations.time_between(tissue_object.peaks[0], tissue_object.frontpoints[0])[0] \
            <= np.pi + .001

    assert np.pi/2 - .001 <= \
        calculations.time_between(tissue_object.peaks[0], tissue_object.contract_points[2][0])[0] \
            <= np.pi/2 + .001

    assert np.pi/2 - .001 <= \
        calculations.time_between(tissue_object.peaks[0], tissue_object.relax_points[2][0])[0] \
            <= np.pi/2 + .001

def test_dfdt():
    """Checks basic slope calculations is working"""
    assert calculations.dfdt([[1,1], [1,1], [1]], [[2,2],[2,2],[3]])[0] == 1
    assert calculations.dfdt([[1,1], [1,1], [3]], [[2,2],[2,2],[1]])[0] == -1
