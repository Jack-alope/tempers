"""
This file contains a class used for finding peaks
"""

import sys
import peakutils
import numpy as np
from scipy.signal import savgol_filter
sys.setrecursionlimit(10000)

class TissuePoints:
    """Tissue class for pointfinding"""
    def __init__(self, window, poly, thresh, min_dist, disp, time):
        """Initalize relevant values"""
        self.raw_disp = disp
        self.time = time
        self.smooth_disp = self.smooth(window, poly)
        self.peaks = self.find_peaks(thresh, min_dist)
        self.basepoints, self.frontpoints = self.find_basepoints_frontpoints()
        self.contract_points, self.relax_points = self.find_analysispoints()

    def smooth(self, window, poly):
        """Applies Savitzky–Golay filter to data"""
        return savgol_filter(self.raw_disp, window, poly)

    def find_peaks(self, thresh, min_dist):
        """Finds usable peaks"""
        unformatted = peakutils.indexes(self.smooth_disp, thresh, min_dist)[1:-1]
        return self.format_points(unformatted)

    def find_basepoints_frontpoints(self):
        """Use the dfdt_recursive func to find basepoints and frontpointspyl"""
        peak_indicies = self.peaks[2]
        basepoints = [self.dfdt_recursive(peak_index,lambda x:x-1) for peak_index in peak_indicies]
        frontpoints = [self.dfdt_recursive(peak_index,lambda x:x+1) for peak_index in peak_indicies]
        return self.format_points(basepoints), self.format_points(frontpoints)

    def find_analysispoints(self):
        """Finds the points for 10, 50, 90% contracted and relaxed"""
        percents = [.1, .5, .9]

        pnts = lambda p_ind,b_ind,b_disp:[self.get_points(p_ind,b_ind,b_disp,p) for p in percents]

        base_disp = (self.basepoints[1] + self.frontpoints[1]) / 2
        contract = list(map(pnts, self.peaks[2], self.basepoints[2], base_disp))
        relax = list(map(pnts, self.peaks[2], self.frontpoints[2], base_disp))

        contract_points = np.transpose(np.array(contract))
        relax_points = np.transpose(np.array(relax))

        return ([self.format_points(point) for point in contract_points],
                    [self.format_points(point) for point in relax_points])

    def dfdt_recursive(self, peak_index, incrementor):
        """Recursively moves along graph until it changes direction"""
        new_index = incrementor(peak_index)
        if self.smooth_disp[new_index] - self.smooth_disp[peak_index] > 0:
            return peak_index
        return self.dfdt_recursive(new_index, incrementor)

    def get_points(self, peak_index, base_index, b_disp, percentage):
        """Returns 90, 50, 10% points between peak and a basepoint"""
        target_val = (percentage * (self.smooth_disp[peak_index] - b_disp)) + b_disp

        def cycle(step):
            for new_index in range(peak_index, base_index, step):
                if self.smooth_disp[new_index] < target_val:
                    return new_index
            return "ERROR"

        if target_val < self.smooth_disp[base_index]:
            return base_index

        return cycle(-1) if peak_index > base_index else cycle(1)

    def format_points(self, indicies):
        """Formats points into a tuple with usable points as well as index"""
        return (self.time[indicies], self.smooth_disp[indicies], indicies)
