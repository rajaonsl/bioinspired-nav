"""
This module includes utility functions for manipulating arrays of cues.

For performance reasons, cues are not represented as their own objects, but
rather as a 1D array.

cue: [d, theta, cue_type, d_2]
"""

import numpy as np
from numba import njit
from enum import IntEnum  #@TODO: investigate fastenum

class ContextCueType(IntEnum):
    OBSTACLE = 0 # is 0 ok ?
    CORNER = 1
    LANDMARK = 2

@njit
def offset(cue_array, x_offset, y_offset) -> np.ndarray:
    """
    shift all context cues by cartesian offset
    """
    x = np.cos(np.radians(cue_array[:, 1])) * cue_array[:, 0] + x_offset
    y = np.sin(np.radians(cue_array[:, 1])) * cue_array[:, 0] + y_offset

    d = np.sqrt(x**2 + y**2)
    theta = np.degrees(np.arctan2(y, x))
    d_2 = 100*np.tanh(d/100)
    return np.column_stack((d, theta,cue_array[:, 2], d_2))

def create_cue(distance, theta, cue_type: int=0):
    """
    Create a proper cue from distance and theta
    """
    return np.array(distance, theta, cue_type, 100*np.tanh(distance/100))