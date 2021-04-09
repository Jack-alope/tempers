import peakutils

def find_peaks(time, disp):
    """Finds usable peaks"""
    unformatted_peaks = peakutils.indexes(disp, .1, .10)[1:-1]
    peaks = (time[unformatted_peaks], disp[unformatted_peaks], unformatted_peaks)
    return peaks

def find_basepoints(time, disp, peaks):
    peak_x, peak_y, indicies = peaks

    return indicies
