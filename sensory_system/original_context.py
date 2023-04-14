"""
the context used for grid cells in the original (java) implementation
"""

import numpy as np
from numba import njit
from enum import IntEnum  #@TODO: investigate fastenum

from sensory_system.context_interface import ContextInterface

# =========================================================================================================
class ContextCueType(IntEnum):
    OBSTACLE = 0
    CORNER = 1
    LANDMARK = 2

# @TODO find better name
# ========================================================================================================= 
class OriginalContext(ContextInterface):
    """
    This class represents environmental contexts as conceived in the original (java) implementation.
    """

    # ---------------------------------------------------------------------------------------------------------
    #@TODO: reconsider input
    def __init__(self, context_cues: np.ndarray, spread_size):
        """
        context cues are expected as a numpy array of context cues (type ContextCue)
        """
        # An array of all context cues. each cue is represented with [d, theta, type, d_2]
        # with theta angular coordinate,
        #      d radial coordinate,
        #      type of cue (integer),
        #      d_2 radial coordinate scaled by 100*tanh(d/100)
        self.context_cues: np.ndarray = context_cues

        # The higher the spread size is, the further a cue will "impact its surroundings".
        self.spread_size = spread_size

        # Discretization of polar space
        self.context_matrix = _compute_context_matrix(self.context_cues, spread_size=spread_size)


    # MOVED TO RANGE SENSOR IMPLEMENTATION
    # @classmethod
    # def from_sensor_data(cls, sensor_data: np.ndarray, field_of_view = 360) -> 'OriginalContext':
    #     """
    #     returns an instance of OriginalContext, from raw sensor data
    #     """
    #     assert len(sensor_data) >= 2

    #     context_cues = np.empty(len(sensor_data), dtype=object)
    #     angle = 0
    #     angle_step = field_of_view/(len(sensor_data) - 1)
    #     for i, measurement in enumerate(sensor_data):
    #         new_cue = ContextCue(d=measurement, theta=angle, cue_type=ContextCueType.OBSTACLE)
    #         context_cues[i] = new_cue
    #         angle += angle_step
    #     new_context = cls(context_cues)
    #     return new_context

    # ---------------------------------------------------------------------------------------------------------
    def occupancy(self, angle: int, distance: int, cue_type: int = ContextCueType.OBSTACLE):
        """returns a 'likelyness' that the point corresponds to a context cue"""
        return self.context_matrix[angle, distance, int(cue_type)]

    # ---------------------------------------------------------------------------------------------------------
    def offset(self, x_offset: float, y_offset: float, new_spread_size: int = 4) -> 'OriginalContext':
        new_context_cues = _offset_cue_array(self.context_cues, x_offset=x_offset, y_offset=y_offset)
        return OriginalContext(new_context_cues, new_spread_size)


    # ---------------------------------------------------------------------------------------------------------
    # NOTE:looks up the new_cues in the matrix (faster)
    def update(self, new_cues: np.ndarray): # UNUSED BECAUSE 360 FOV @TODO: implement anyway
        """
        """
        new_cues_list = []
        for cue in new_cues:
            if self.context_matrix[round(cue[1]), round(cue[3]), round(cue[2])] != 1.:
                new_cues_list.append(cue)
        
        self.context_cues = np.append(self.context_cues, np.array(new_cues_list))

        self.context_matrix = _compute_context_matrix(self.context_cues, self.spread_size)

    # ---------------------------------------------------------------------------------------------------------
    def rotate(self, angle_in_degrees, spread_size=16): # Used by place cells, hence the default spread size to 16
        """
        Rotates the context by a given angle
        """
        new_cues = self.context_cues.copy()
        new_cues[:, 1] = np.mod(new_cues[:, 1] + angle_in_degrees, 360)

        return OriginalContext(new_cues, spread_size)

# =========================================================================================================
# UTILS
# ---------------------------------------------------------------------------------------------------------
def create_cue(distance, theta, cue_type: int=0):
    """
    Create a proper cue from distance and theta
    """
    return np.array([distance, theta, cue_type, 100*np.tanh(distance/100)])

def cues_array_to_cartesian(array: np.ndarray):
    x = np.cos(np.radians(array[:, 1])) * array[:, 0]
    y = np.sin(np.radians(array[:, 1])) * array[:, 0]

    return x,y

@njit # njit on these? really? lol
def get_d(cue: np.ndarray):
    return cue[0]

@njit
def get_theta(cue: np.ndarray):
    return cue[1]

@njit
def get_cue_type(cue: np.ndarray):
    return cue[2]

@njit
def get_d_2(cue: np.ndarray):
    return cue[3]

# =========================================================================================================
# METHODS OPTIMIZED WITH NUMBA
# =========================================================================================================
# ---------------------------------------------------------------------------------------------------------
@njit
def _compute_context_matrix(context_cues: np.array, spread_size: int=4) -> np.ndarray:
    """
    compute the context matrix from the list of context cues

    spread_size: the size of the "impact" that each cue makes in the matrix
    in original code, this is 16 for place cells and 4 for grid cells
    Also, original code had a bug causing asymetrical "impacts" =, which is fixed in this implementation

    NOTE: converting this method to numba JIT requires it to
    not use object attributes, thus the need for arguments
    and return value
    """

    # The complex matrix is a discretization of polar space
    context_matrix = np.zeros((360,100,2)) #@TODO make resolution flexible @TODO only 2 types?

    

    for cue in context_cues:

        d_int = int(cue[3]) # @TODO: use d' (tanh form)
        angle_int = int(cue[1]) # @TODO not interchange degrees and indexes
        cue_type = int(cue[2]) # @TODO: filter by type

        # modify the values around the point
        # @TODO: numpy-ify
        for i in range(-spread_size, spread_size + 1): #@TODO make bounds flexible (also change /5 in val)
            for j in range(-spread_size, spread_size + 1):
                dist_as_index = d_int + i
                angle_as_index = (angle_int + j) % 360
                    #@TODO: why does angle need to be checked again here ? weird shenanigans
                if dist_as_index >= 0 and dist_as_index < 100 and angle_as_index >=0 and angle_as_index < 360:
                    val = 1 - max(abs(i), abs(j))/(spread_size + 1) # 1 at i=j=0, then lower as i or j increases
                    if val > context_matrix[angle_as_index][dist_as_index][cue_type]:
                        context_matrix[angle_as_index][dist_as_index][cue_type] = val
    return context_matrix

# ---------------------------------------------------------------------------------------------------------
@njit
def _offset_cue_array(cue_array, x_offset, y_offset) -> np.ndarray:
    """
    Shift all context cues by cartesian offset
    """
    x = np.cos(np.radians(cue_array[:, 1])) * cue_array[:, 0] + x_offset
    y = np.sin(np.radians(cue_array[:, 1])) * cue_array[:, 0] + y_offset

    d = np.sqrt(x**2 + y**2)
    theta = np.degrees(np.arctan2(y, x))
    d_2 = 100*np.tanh(d/100)
    return np.column_stack((d, theta,cue_array[:, 2], d_2))