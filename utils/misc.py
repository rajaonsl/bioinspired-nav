#@TODO: rename module
"""
module regrouping some reocurring operations
"""

import numpy as np

def polar_to_cartesian(d, theta):
    """
    Convert polar coordinates to cartesian (also works on arrays)
    """
    theta = np.radians(theta)
    x = d*np.cos(theta)
    y = d*np.sin(theta)
    return(x,y)