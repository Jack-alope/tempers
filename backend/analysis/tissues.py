"""
This file contains a class used for finding peaks
"""

import sys
import numpy as np
import scipy.signal as signal
from . import calculations
sys.setrecursionlimit(10000)


class TissuePoints:
    """Tissue class for pointfinding"""

    def __init__(self, disp, time, tissue_object):
        """Initalize relevant values"""
        self.window = 13
        self.poly = 3
        self.thresh = 0.5
        self.min_dist = 10
        self.buffer = 15
        self.raw_disp = disp
        self.time = time
        self.post_dist = 6
        self.youngs = 1.33
        self.tissue = tissue_object
        self.raw_disp_norm = self.post_dist - np.array(disp)

        # To be defined later, set to None for readability.
        self.peaks = self.basepoints = self.frontpoints = self.smooth_disp = \
            self.smooth_force = self.contract_points = self.relax_points = \
            self.raw_force = None

        self.calculated_values = {}

        self.smooth(self.window, self.poly)

    def smooth(self, window=None, poly=None, inverse=False, baseline=False):
        """Applies Savitzky–Golay filter to data"""
        if window is not None:
            self.window = window
        if poly is not None:
            self.poly = poly

        smoothed = signal.savgol_filter(self.raw_disp, self.window, self.poly)

        if inverse:
            self.smooth_disp = -1*(self.post_dist - smoothed) 
            self.raw_force = np.array(self.continuous_df(-1*self.raw_disp_norm))
        else:#
            self.smooth_disp = self.post_dist - smoothed
            self.raw_force = np.array(self.continuous_df(self.raw_disp_norm))

        self.smooth_force = np.array(self.continuous_df(self.smooth_disp))

        if baseline:
            signal.detrend(self.smooth_force, overwrite_data=True)

        self.dfdt = signal.savgol_filter(self.raw_force, self.window, self.poly, deriv=1, delta= np.average(np.diff(self.time)))

        self.find_peaks()

    def find_peaks(self, thresh=None, min_dist=None, x_range=None, buffer=None):
        """Finds usable peaks"""
        if thresh is not None:
            self.thresh = thresh
        if min_dist is not None:
            self.min_dist = min_dist
        if buffer is not None:
            self.buffer = buffer

        rel_thresh = self.thresh * (max(self.smooth_force) - min(self.smooth_force))
        peaks = signal.find_peaks(self.smooth_force, distance=self.min_dist, prominence=rel_thresh)[0]

        if not list(peaks):
            print('No Peaks')
        else:
            unformatted = peaks[1:-1]

            if not (x_range is None) | (x_range == [0, 0]):
                unformatted = self.crop_peaks(unformatted, x_range[0], x_range[1])

            self.peaks = self.format_points(unformatted, self.smooth_force)

            self.find_basepoints_frontpoints()

    def crop_peaks(self, peak_list, start, end):
        """crops peaks to allow for time region selection"""
        def mins(lists, ind): return np.abs(np.array(lists) - ind).argmin()
        start_ind = mins(self.time, start)
        end_ind = mins(self.time, end)
        peak_start = mins(peak_list, start_ind) + 2
        peak_end = mins(peak_list, end_ind) - 1
        return peak_list[peak_start:peak_end]

    def find_basepoints_frontpoints(self):
        """Use the dfdt_recursive func to f    buffers: int
            Ond basepoints and frontpointspyl"""
        peak_indicies = self.peaks[2]
        basepoints = [self.dfdt_recursive(
            peak_index - self.buffer, lambda x:x-1) for peak_index in peak_indicies]
        frontpoints = [self.dfdt_recursive(
            peak_index + self.buffer, lambda x:x+1) for peak_index in peak_indicies]

        self.basepoints = self.format_points(basepoints, self.smooth_force)
        self.frontpoints = self.format_points(frontpoints, self.smooth_force)

        self.find_analysispoints()

    def find_analysispoints(self):
        """Finds the points for 10, 50, 90% contracted and relaxed"""
        percents = [.1, .2, .5, .8, .9]

        def pnt(p_i, b_i, b_d): return [
            self.get_points(p_i, b_i, b_d, p) for p in percents]

        base_disp = [(basepoint + self.frontpoints[1][i]) /
                     2 for i, basepoint in enumerate(self.basepoints[1])]

        contract = map(pnt, self.peaks[2], self.basepoints[2], base_disp)
        relax = map(pnt, self.peaks[2], self.frontpoints[2], base_disp)

        self.contract_points = np.transpose(list(contract), axes=[1, 2, 0])
        self.relax_points = np.transpose(list(relax), axes=[1, 2, 0])

        self.calculate_values(base_disp)

    def dfdt_recursive(self, peak_index, incrementor):
        """Recursively moves along graph until it changes direction"""
        new_index = incrementor(peak_index)
        if self.smooth_force[new_index] - self.smooth_force[peak_index] > 0:
            return peak_index
        return self.dfdt_recursive(new_index, incrementor)

    def get_points(self, peak_index, base_index, b_disp, percentage):
        """
        Returns 90, 50, 10% points between peak and a basepoint.
        Using linear approximation.
        """
        target_val = (
            percentage * (self.smooth_force[peak_index] - b_disp)) + b_disp

        def cycle(step):
            for new_index in range(peak_index, base_index, step):
                if self.smooth_force[new_index] < target_val:
                    y_diff = np.absolute(
                        self.smooth_force[new_index]-self.smooth_force[new_index-step])
                    x_diff = np.absolute(
                        self.time[new_index]-self.time[new_index-step])
                    slope = (y_diff / x_diff) * -1 * step
                    target_x = (
                        (target_val-self.smooth_force[new_index])/slope)+self.time[new_index]
                    return [target_x, target_val]
            return [self.time[base_index], self.smooth_force[base_index]]

        return cycle(-1) if peak_index > base_index else cycle(1)

    def format_points(self, indicies, points):
        """Formats points into a tuple with usable points as well as
        index"""
        x_axis = [self.time[index] for index in indicies]
        y_axis = [points[index] for index in indicies]
        return (x_axis, y_axis, indicies)

    def continuous_df(self, disps):
        return calculations.force_continuous(self.youngs, self.tissue.post.radius,
                                 self.tissue.post.left_post_height, self.tissue.post.left_tissue_height,
                                 self.tissue.post.right_post_height, self.tissue.post.right_tissue_height,
                                 disps)

    def calculate_values(self, base_disp):
        """Creates a dictionary with all calculated values"""
        self.calculated_values["dev_force"], self.calculated_values["dev_force_std"] \
            = _averager(np.array(self.peaks[1]) - np.array(base_disp))

        self.calculated_values["dias_force"], self.calculated_values["dias_force_std"] \
            = _averager(base_disp)

        self.calculated_values["sys_force"], self.calculated_values["sys_force_std"] \
            = _averager(self.peaks[1])

        self.calculated_values["beating_freq"], self.calculated_values["beating_freq_std"] \
            = calculations.beating_frequency(self.peaks[0])

        self.calculated_values["beat_rate_cov"] \
            = self.calculated_values["beating_freq_std"] / self.calculated_values["beating_freq"]

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

        (self.calculated_values["dfdt"], self.calculated_values["dfdt_std"]), \
            (self.calculated_values["negdfdt"], self.calculated_values["negdfdt_std"]) \
            = calculations.dfdt_calc(self.basepoints, self.frontpoints, self.dfdt)


def _averager(value_list):
    """return the avg and std of a list"""
    return np.average(value_list), np.std(value_list)
