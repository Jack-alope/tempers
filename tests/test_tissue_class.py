"""
Testing for the point finding class
"""

# import matplotlib.pyplot as plt
import numpy as np


def test_find_peaks(tissue_object):
    """Testing peaks are where they schould be"""
    assert np.all([round(time % np.pi, 3) == 1.571 for time in tissue_object.peaks[0]])
    assert np.all(
        [round(amplitude, 3) == 3.000 for amplitude in tissue_object.peaks[1]]
    )


def test_find_basepoints_frontpoints(tissue_object):
    """Testing that basepoints and peaks are as expected"""
    assert np.all([round(point, 3) == 1.000 for point in tissue_object.basepoints[1]])
    assert np.all([round(point, 3) == 1.000 for point in tissue_object.frontpoints[1]])


def test_find_analysispoints(tissue_object):
    """Testing annalysis points disp is as expected"""
    assert np.all(
        [round(point, 2) == 1.200 for point in tissue_object.contract_points[0][1]]
    )
    assert np.all(
        [round(point, 2) == 1.400 for point in tissue_object.contract_points[1][1]]
    )
    assert np.all(
        [round(point, 2) == 2.000 for point in tissue_object.contract_points[2][1]]
    )
    assert np.all(
        [round(point, 2) == 2.600 for point in tissue_object.contract_points[3][1]]
    )
    assert np.all(
        [round(point, 2) == 2.800 for point in tissue_object.contract_points[4][1]]
    )

    assert np.all(
        [round(point, 2) == 1.200 for point in tissue_object.relax_points[0][1]]
    )
    assert np.all(
        [round(point, 2) == 1.400 for point in tissue_object.relax_points[1][1]]
    )
    assert np.all(
        [round(point, 2) == 2.000 for point in tissue_object.relax_points[2][1]]
    )
    assert np.all(
        [round(point, 2) == 2.600 for point in tissue_object.relax_points[3][1]]
    )
    assert np.all(
        [round(point, 2) == 2.800 for point in tissue_object.relax_points[4][1]]
    )


# TODO: Test fringe conditions for basepoints and frontpoints


def test_beating_freq(tissue_object):
    """Testing that the beatinf frequency is 1/period"""
    assert (
        (1 / (2 * np.pi) - 0.002)
        <= tissue_object.calculated_values["beating_freq"]
        <= (1 / (2 * np.pi) + 0.002)
    )


def test_t2rel_50(tissue_object):
    """Test that the tissue object properly uses calculation function"""
    assert (
        (np.pi - 0.002) / 2
        <= tissue_object.calculated_values["t2rel50"]
        <= (np.pi + 0.002) / 2
    )


def test_t50(tissue_object):
    """test that t50 is half period for sin"""
    assert np.pi - 0.002 <= tissue_object.calculated_values["t50"] <= np.pi + 0.002

    t50 = (
        tissue_object.calculated_values["c50"] + tissue_object.calculated_values["r50"]
    )
    assert -0.002 <= np.absolute(t50 - tissue_object.calculated_values["t50"]) <= 0.002
    assert (
        (np.pi - 0.002) / 2
        <= tissue_object.calculated_values["c50"]
        <= (np.pi + 0.002) / 2
    )
    assert (
        (np.pi - 0.002) / 2
        <= tissue_object.calculated_values["r50"]
        <= (np.pi + 0.002) / 2
    )


# def test_dfdt(tissue_object):
#    """Checks that dfdt is functioning properly with supplied values"""
#    assert tissue_object.calculated_values['negdfdt'] < 0

#    slope_diff = tissue_object.calculated_values['negdfdt'] + \
#                tissue_object.calculated_values['dfdt']
#    assert -.001 <= slope_diff <= .001
