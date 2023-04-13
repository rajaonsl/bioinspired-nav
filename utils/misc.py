#@TODO: rename module
"""
module regrouping some reocurring operations
"""

import numpy as np

# Applying bounds manually is slower than modulo
# def apply_bounds(x, sup):
#     """ convert a value (usually an index) to a value bound between 0 and sup.
#     useful for making valid indexes in a torroidal array"""
#     if x >= sup:
#         return x - sup
#     elif x <0:
#         return x + sup
#     else:
#         return x

# def apply_angle_bounds(angle):
#     """convert an angle (from -360 to +719) to an angle in valid bounds (int from 0 to 359)
#     type insensitive (int -> int or float -> float)"""
#     return apply_bounds(angle, 360)


# def apply_bounds_arr(x_arr, sup):
#     """ convert a value (usually an index) to a value bound between 0 and sup.
#     useful for making valid indexes in a torroidal array"""
#     return np.where(x_arr >= sup, x_arr - sup, np.where(x_arr < 0, x_arr + sup, x_arr)).astype(int)
# #@TODO: is np.mod faster ? gotta try

# def apply_angle_bounds_arr(angle_arr):
#     """convert an angle (from -360 to +719) to an angle in valid bounds (int from 0 to 359)
#     type insensitive (int -> int or float -> float)"""
#     return apply_bounds_arr(angle_arr, 360)

def polar_to_cartesian(d, theta):
    """
    Convert polar coordinates to cartesian (also works on arrays)
    """
    theta = np.radians(theta)
    x = d*np.cos(theta)
    y = d*np.sin(theta)
    return(x,y)