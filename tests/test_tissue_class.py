"""
Testing for the point finding class
"""

#import matplotlib.pyplot as plt
import numpy as np

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
    assert np.all([.399 <= point <= .401 for point in tissue_object.contract_points[1][1]])
    assert np.all([.999 <= point <= 1.001 for point in tissue_object.contract_points[2][1]])
    assert np.all([1.599 <= point <= 1.601 for point in tissue_object.contract_points[3][1]])
    assert np.all([1.799 <= point <= 1.801 for point in tissue_object.contract_points[4][1]])

    assert np.all([.199 <= point <= .201 for point in tissue_object.relax_points[0][1]])
    assert np.all([.399 <= point <= .401 for point in tissue_object.relax_points[1][1]])
    assert np.all([.999 <= point <= 1.001 for point in tissue_object.relax_points[2][1]])
    assert np.all([1.599 <= point <= 1.601 for point in tissue_object.relax_points[3][1]])
    assert np.all([1.799 <= point <= 1.801 for point in tissue_object.relax_points[4][1]])

# TODO: Test fringe conditions for basepoints and frontpoints

def test_beating_freq(tissue_object):
    """Testing that the beatinf frequency is 1/period"""
    assert (1/(2*np.pi)-.002) <= \
        tissue_object.calculated_values['beating_freq'] <= (1/(2*np.pi)+.002)

def test_t2rel_50(tissue_object):
    """Test that the tissue object properly uses calculation function"""
    assert (np.pi - .002)/2 <= \
        tissue_object.calculated_values['t2rel50'] <= (np.pi + .002)/2

def test_t50(tissue_object):
    """test that t50 is half period for sin"""
    assert np.pi - .002 <= \
        tissue_object.calculated_values['t50'] <= np.pi + .002

    t50 = tissue_object.calculated_values['c50'] + tissue_object.calculated_values['r50']
    assert -.002 <= np.absolute(t50 - tissue_object.calculated_values['t50']) <= .002
    assert (np.pi - .002)/2 <= tissue_object.calculated_values['c50'] <= (np.pi + .002)/2
    assert (np.pi - .002)/2 <= tissue_object.calculated_values['r50'] <= (np.pi + .002)/2

def test_dfdt(tissue_object):
    """Checks that dfdt is functioning properly with supplied values"""
    assert tissue_object.calculated_values['negdfdt'] < 0

    slope_diff = tissue_object.calculated_values['negdfdt'] + \
                tissue_object.calculated_values['dfdt']
    assert -.001 <= slope_diff <= .001
