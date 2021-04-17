"""
This file contains a class used for finding peaks
"""

import sys
import peakutils
import numpy as np
from scipy.signal import savgol_filter
from . import calculations
sys.setrecursionlimit(10000)


class TissuePoints:
    """Tissue class for pointfinding"""

    def __init__(self, disp, time):
        """Initalize relevant values"""
        # Initialize with defaults
        self.window = 13
        self.poly = 3
        self.thresh = .5
        self.min_dist = 5
        self.raw_disp = disp
        self.time = time

        # To be defined later, set to None for readability.
        self.peaks = self.basepoints = self.frontpoints = self.smooth_disp = \
            self.contract_points = self.relax_points = None
            
        self.calculated_values = {}

        self.smooth(self.window, self.poly)

    def smooth(self, window=None, poly=None):
        """Applies Savitzky–Golay filter to data"""
        if window is not None:
            self.window = window
        if poly is not None:
            self.poly = poly
        self.smooth_disp = savgol_filter(self.raw_disp, self.window, self.poly)
        self.find_peaks()

    def find_peaks(self, thresh=None, min_dist=None):
        """Finds usable peaks"""
        if thresh is not None:
            self.thresh = thresh
        if min_dist is not None:
            self.min_dist = min_dist

        unformatted = np.array(peakutils.indexes(
            self.smooth_disp, self.thresh, self.min_dist)[1:-1])

        self.peaks = self.format_points(unformatted)

        self.find_basepoints_frontpoints()

    def find_basepoints_frontpoints(self):
        """Use the dfdt_recursive func to find basepoints and frontpointspyl"""
        peak_indicies = self.peaks[2]
        basepoints = [self.dfdt_recursive(
            peak_index, lambda x:x-1) for peak_index in peak_indicies]
        frontpoints = [self.dfdt_recursive(
            peak_index, lambda x:x+1) for peak_index in peak_indicies]

        self.basepoints = self.format_points(basepoints)
        self.frontpoints = self.format_points(frontpoints)

        self.find_analysispoints()

    def find_analysispoints(self):
        """Finds the points for 10, 50, 90% contracted and relaxed"""
        percents = [.1, .2, .5, .8, .9]

        def pnts(p_ind, b_ind, b_disp): return [
            self.get_points(p_ind, b_ind, b_disp, p) for p in percents]

        base_disp = [(basepoint + self.frontpoints[1][i]) /
                     2 for i, basepoint in enumerate(self.basepoints[1])]
        contract = list(
            map(pnts, self.peaks[2], self.basepoints[2], base_disp))
        relax = list(map(pnts, self.peaks[2], self.frontpoints[2], base_disp))

        contract_points = np.transpose(np.array(contract))
        relax_points = np.transpose(np.array(relax))

        # TODO: Figure out what is happening with int --> string situation
        # REVIEW: Why dont you use enumerate
        for i in range(len(contract_points)):
            contract_points[i] = list(map(int, contract_points[i]))
            relax_points[i] = list(map(int, relax_points[i]))

        self.contract_points = [self.format_points(
            point) for point in contract_points]
        self.relax_points = [self.format_points(
            point) for point in relax_points]

        self.calculate_values()

    def dfdt_recursive(self, peak_index, incrementor):
        """Recursively moves along graph until it changes direction"""
        new_index = incrementor(peak_index)
        if self.smooth_disp[new_index] - self.smooth_disp[peak_index] > 0:
            return peak_index
        return self.dfdt_recursive(new_index, incrementor)

    def get_points(self, peak_index, base_index, b_disp, percentage):
        """Returns 90, 50, 10% points between peak and a basepoint"""
        target_val = (
            percentage * (self.smooth_disp[peak_index] - b_disp)) + b_disp

        # TODO: Linear approximation
        def cycle(step):
            for new_index in range(peak_index, base_index, step):
                if self.smooth_disp[new_index] < target_val:
                    return new_index
            return base_index

        return cycle(-1) if peak_index > base_index else cycle(1)

    def format_points(self, indicies):
        """Formats points into a tuple with usable points as well as
        index"""
        x_axis = [self.time[index] for index in indicies]
        y_axis = [self.smooth_disp[index] for index in indicies]
        return (x_axis, y_axis, indicies)

    def calculate_values(self):
        """Creates a dictionary with all calculated values"""
        self.calculated_values["dev_force"], self.calculated_values["dev_force_std"] \
            = (5, 5)

        self.calculated_values["dias_force"], self.calculated_values["dias_force_std"] \
            = (5, 5)

        self.calculated_values["beat_rate_COV"], self.calculated_values["beat_rate_COV_std"] \
            = (5, 5)

        self.calculated_values["beating_freq"], self.calculated_values["beating_freq_std"] \
            = calculations.beating_frequency(self.peaks[0])

        self.calculated_values["t2pk"], self.calculated_values["t2pk_std"] \
            = calculations.time_between(self.peaks[0], self.contract_points[0][0])

        self.calculated_values["t2rel50"], self.calculated_values["t2rel50_std"] \
            = calculations.time_between(self.peaks[0], self.relax_points[2][0])

        self.calculated_values["t2rel80"], self.calculated_values["t2rel80_std"] \
            = calculations.time_between(self.peaks[0], self.relax_points[1][0])

        self.calculated_values["t2rel90"], self.calculated_values["t2rel90_std"] \
            = calculations.time_between(self.peaks[0], self.relax_points[0][0])

        self.calculated_values["t50"], self.calculated_values["t50_std"] \
            = calculations.time_between(self.contract_points[2][0], self.relax_points[2][0])

        self.calculated_values["c50"], self.calculated_values["c50_std"] \
            = calculations.time_between(self.contract_points[2][0], self.peaks[0])

        self.calculated_values["r50"], self.calculated_values["r50_std"] \
            = calculations.time_between(self.relax_points[2][0], self.peaks[0])

        self.calculated_values["dfdt"], self.calculated_values["dfdt_std"] \
            = calculations.dfdt(self.contract_points[0], self.contract_points[4])

        self.calculated_values["negdfdt"], self.calculated_values["negdfdt_std"] \
            = calculations.dfdt(self.relax_points[0], self.relax_points[4])