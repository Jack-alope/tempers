"""This file is stricly reserved for direct force and time parameter computations"""
import numpy as np

def beating_frequency(peaks):
    """"Used to calculate the period of contraction"""
    timediff = []
    peak_times = peaks[0]
    for i in range(len(peaks) - 1):
        timediff.append(1 / (peak_times[i + 1] - peak_times[i]))
    std = np.std(timediff)
    avg = sum(timediff) / len(timediff)
    return avg, std
