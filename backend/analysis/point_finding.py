'''This module is responsible for finding relevant points used in analysis'''

import peakutils
import sys 

def find_peaks(time, disp):
    ''' Finds usable peaks '''
    unformatted_peaks = peakutils.indexes(disp, .1, .10)[1:-1]
    peaks = (time[unformatted_peaks], disp[unformatted_peaks], unformatted_peaks)
    return peaks

def find_basepoints_frontpoints(disp, peaks):
    '''Use the dfdt_recursive func to find basepoints and frontpointspyl'''
    peak_indicies = peaks[2]
    basepoints = [dfdt_recursive(disp, peak_index, lambda x:x-1) for peak_index in peak_indicies]
    frontpoints = [dfdt_recursive(disp, peak_index, lambda x:x+1) for peak_index in peak_indicies]
    return (basepoints, frontpoints)

def find_analysispoints(disp, peaks, base_values):
    base_index = base_values[1]
    peak_index = peaks[2][1]
    ind = disp_recursive(disp, peak_index, base_index, lambda x:x-1, .1)
    
    return ind

def dfdt_recursive(disp, peak_index, incrementor):
    ''' Recursively moves along graph until it changes direction '''
    new_index = incrementor(peak_index)
    if disp[new_index] - disp[peak_index] > 0:
        return peak_index
    return dfdt_recursive(disp, new_index, incrementor)

def disp_recursive(disp, peak_index, base_index, incrementor, percentage):
    new_index = incrementor(peak_index)
    if disp[new_index] - disp[peak_index] < percentage * (disp[base_index] - disp[peak_index]):
        return new_index
    return disp_recursive(disp, new_index, base_index, incrementor, percentage)