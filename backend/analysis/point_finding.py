"""This module is responsible for finding relevant points used in analysis"""

import peakutils
import numpy as np

def find_peaks(time, disp):
    """Finds usable peaks"""
    unformatted_peaks = peakutils.indexes(disp, .1, .10)[1:-1]
    peaks = (time[unformatted_peaks], disp[unformatted_peaks], unformatted_peaks)
    return peaks

def find_basepoints_frontpoints(disp, peaks):
    """Use the dfdt_recursive func to find basepoints and frontpointspyl"""
    peak_indicies = peaks[2]
    basepoints = [dfdt_recursive(disp, peak_index, lambda x:x-1) for peak_index in peak_indicies]
    frontpoints = [dfdt_recursive(disp, peak_index, lambda x:x+1) for peak_index in peak_indicies]
    return (basepoints, frontpoints)

def find_analysispoints(disp, peaks, base_indicies, front_indicies):
    """Finds the points for 10, 50, 90% contracted and relaxed"""
    peak_indicies= peaks[2]
    percents = [.1, .5, .9]
    getter = lambda p_ind, b_ind: [get_points(disp, p_ind, b_ind, perc) for perc in percents]
    contract_points = list(map(getter,peak_indicies,base_indicies))
    relax_points = list(map(getter,front_indicies,peak_indicies))
    return contract_points, relax_points

def dfdt_recursive(disp, peak_index, incrementor):
    """Recursively moves along graph until it changes direction"""
    new_index = incrementor(peak_index)
    if disp[new_index] - disp[peak_index] > 0:
        return peak_index
    return dfdt_recursive(disp, new_index, incrementor)

def get_points(disp, start_index, finish_index, percentage):
    """Goes from disp at start until its further away than the
    percentage"""
    # TODO: This will need to linearly approximate, not just return
    # the index. Also return error handling
    max_dist_from_start = np.absolute(percentage * (disp[start_index] - disp[finish_index]))
    for new_index in range(start_index, finish_index, -1):
        if np.absolute(disp[start_index] - disp[new_index]) > max_dist_from_start:
            return new_index
    return False
            