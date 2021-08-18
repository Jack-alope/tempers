"""This file is stricly reserved for direct force and time parameter computations"""
import numpy as np

def force(youngs, radius, l_right, a_right, l_left, a_left, delta_total):
    """Calculates force on left post"""
    force_ratio = ((a_right ** 2) * ((3 * l_right) - a_right)) / \
        ((a_left ** 2) * ((3 * l_left) - a_left))

    left_coef = (3 * np.pi * youngs * (radius ** 4)) / \
        (2 * (a_left ** 2) * ((3 * l_left) - a_left))

    delta_left = lambda delta: (delta / (1 + force_ratio)) * left_coef * 1000
    left_force = list(map(delta_left, delta_total))
    return _averager(left_force)

def force_continuous(youngs, radius, l_right, a_right, l_left, a_left, delta_total):
    """Calculates force on left post at a single value and returns"""
    force_ratio = ((a_right ** 2) * ((3 * l_right) - a_right)) / \
        ((a_left ** 2) * ((3 * l_left) - a_left))

    left_coef = (3 * np.pi * youngs * (radius ** 4)) / \
        (2 * (a_left ** 2) * ((3 * l_left) - a_left))

    delta_left = lambda delta: (delta / (1 + force_ratio)) * left_coef * 1000
    left_force = list(map(delta_left, delta_total))
    return left_force

def dev_force(youngs, radius, l_right, a_right, l_left, a_left, delta_max, delta_min):
    """Calculate the developed force on the left post"""
    force_ratio = ((a_right ** 2) * ((3 * l_right) - a_right)) / \
        ((a_left ** 2) * ((3 * l_left) - a_left))

    left_coef = (3 * np.pi * youngs * (radius ** 4)) / \
        (2 * (a_left ** 2) * ((3 * l_left) - a_left))

    delta_left = lambda delta: (delta / (1 + force_ratio)) * left_coef * 1000
    left_force_max = np.array(list(map(delta_left, delta_max)))
    left_force_min = np.array(list(map(delta_left, delta_min)))

    left_force = left_force_max - left_force_min
    return _averager(left_force)

def beating_frequency(peak_times):
    """"Used to calculate the period of contraction"""
    timediff = []
    for i in range(len(peak_times) - 1):
        timediff.append(1 / (peak_times[i + 1] - peak_times[i]))
    return _averager(timediff)

def time_between(first_times, second_times):
    """Used for calculating time differences"""
    list_vals = list(map(_subtraction, first_times, second_times))
    return _averager(list_vals)

def dfdt_calc(basepoints, frontpoints, dfdt):
    """
    Calculates max and min of dfdt for each peak, then averages
    for all peaks
    """
    dfdt_split = list(map(lambda x,y : dfdt[x:y], basepoints[2], frontpoints[2]))
    maxs = [max(interval) for interval in dfdt_split]
    mins = [min(interval) for interval in dfdt_split]
    return _averager(maxs), _averager(mins)

def _subtraction(first_points, second_points):
    """simple subtraction, primarily used for mapping time diffs"""
    return np.absolute(first_points - second_points)

def _averager(value_list):
    """return the avg and std of a list"""
    return np.average(value_list), np.std(value_list)