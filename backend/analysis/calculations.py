"""This file is stricly reserved for direct force and time parameter computations"""
import numpy as np

def force(youngs, radius, l_right, a_right, l_left, a_left, delta_total):
    """Calculates force on left post"""
    force_ratio = ((a_right ** 2) * ((3 * l_right) - a_right)) / \
        ((a_left ** 2) * ((3 * l_right) - a_right))

    left_coef = (3 * np.pi * youngs * (radius ** 4)) / \
        (2 * (a_left ** 2) * ((3 * l_left) - a_left))

    delta_left = lambda delta: (delta / (1 + force_ratio)) * left_coef
    left_force = list(map(delta_left, delta_total))

    std = np.std(left_force)
    avg = sum(left_force) / len(left_force)
    return avg, std

def beating_frequency(peak_times):
    """"Used to calculate the period of contraction"""
    timediff = []
    for i in range(len(peak_times) - 1):
        timediff.append(1 / (peak_times[i + 1] - peak_times[i]))
    std = np.std(timediff)
    avg = sum(timediff) / len(timediff)
    return (avg, std)

def time_between(first_times, second_times):
    """Used for calculating time differences"""
    subtract = lambda f_t, s_t: np.absolute(f_t - s_t)
    list_vals = list(map(subtract, first_times, second_times))

    std = np.std(list_vals)
    avg = sum(list_vals) / len(list_vals)
    return avg, std

# def dfdt(ten_points, nine_points):
    # """Find slope between points"""
    # subtract = lambda f_p, s_p: np.absolute(f_p - s_p)
    # TODO: Implement dfdt
    # rise_list = list(map(subtract, ten_points[1], nine_points[1]))
    # run_list = list(map(subtract, ten_points[0], nine_points[0]))

    # if nine_points[2][0] > ten_points[2][0]:
    #    slope_list = list(map(lambda x, y: x/y, rise_list, run_list))
    # else:
    #    slope_list = list(map(lambda x, y: -1* x/y, rise_list, run_list))

    # std = np.std(slope_list)
    # avg = sum(slope_list) / len(slope_list)
    # return avg, std
    # return 0, 0
