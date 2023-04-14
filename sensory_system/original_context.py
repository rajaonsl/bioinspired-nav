"""
the context used for grid cells in the original (java) implementation
"""

import numpy as np
from numba import njit
from enum import IntEnum  #@TODO: investigate fastenum

from sensory_system.context_interface import ContextInterface

# @TODO find better name
# =========================================================================================================
class ContextCueType(IntEnum):
    OBSTACLE = 0 # is 0 ok ?
    CORNER = 1
    LANDMARK = 2

# ========================================================================================================= 
class OriginalContext(ContextInterface):
    """
    This class represents environmental contexts as conceived in the original (java) implementation.
    """

    # ---------------------------------------------------------------------------------------------------------
    #@TODO: reconsider input
    def __init__(self, context_cues: np.ndarray):
        """
        context cues are expected as a numpy array of context cues (type ContextCue)
        """
        # An array of all context cues. each cue is represented with [d, theta, type, d_2]
        # where theta: angular coordinate
        #       d radial coordinate
        #       type of cue (integer)
        #       d_2 radial coordinate scaled by 100*tanh(d/100)
        self.context_cues: np.ndarray = context_cues

        # Discretization of polar space
        self.context_matrix = _compute_context_matrix(self.context_cues)
        # self.context_matrix: np.ndarray = _compute_context_matrix(self.__get_cues_as_array()) #@TODO make resolution flexible @TODO only 2 types? idk


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
        #print("occupancy returned", self.context_matrix[angle][distance][int(type_)] )
        #print("in:", self.context_matrix)
        return self.context_matrix[angle, distance, int(cue_type)]

    # ---------------------------------------------------------------------------------------------------------
    def offset(self, x_offset: float, y_offset: float) -> 'OriginalContext':
        new_context_cues = _offset_cue_array(self.context_cues, x_offset=x_offset, y_offset=y_offset)
        return OriginalContext(new_context_cues)


    # ---------------------------------------------------------------------------------------------------------
    # NOTE: better implementation: look up cue in the matrix
    def update(self, new_cues: np.ndarray):
        """
        """
        new_cues_list = []
        for cue in new_cues:
            if self.context_matrix[round(cue[1]), round(cue[3]), round(cue[2])] != 1.:
                new_cues_list.append(cue)
        
        self.context_cues = np.append(self.context_cues, np.array(new_cues_list))

        self.context_matrix = _compute_context_matrix(self.context_cues)


    # ---------------------------------------------------------------------------------------------------------
    # NOTE: naive implementation: compare each new cue with each existing cue
    def update_naive(self, new_cues: np.ndarray):
        """
        updates the context by taking the new markers into account

        new markers (new_cues) are expected as an array where each cue is 
        represented by [d, theta, cue_typen d_2] (as defined in cue_array_utility)
        """
        new_cues_list = new_cues.tolist()
        i = 0
        while i < len(new_cues_list):
            new_cue = new_cues_list[i]

            d, theta = round(new_cue[0]), round(new_cue[1])
            for cue in self.context_cues:
                if (new_cue[3] == cue[3] and # cues are the same type 
                    d == round(cue[0]) and   # cues have same radial coordinate 
                    theta == round(cue[1])): # cues have same angular coordinate
                    del new_cues_list[i]
                    i -= 1
                    break

            i += 1

        if len(new_cues_list) == 0:
            return
        # 2. Add the points that 'survived'
        self.context_cues: np.ndarray = np.append(self.context_cues, new_cues_list)

        # 3. Update the context matrix (@TODO/WARNING: not same behavior as original impl in place cell)
        # self.__compute_context_matrix()
        self.context_matrix = _compute_context_matrix(self.context_cues)


    # ---------------------------------------------------------------------------------------------------------
    def update_OLD(self, new_cues: np.ndarray):
        """
        updates the context by taking the new markers into account.

        new markers (cues) are expect ad a numpy array of context cues (type ContextCue)
        NOTE/WARNING/@TODO: This is not 100% the same behavior as place cells, because
        place cells context matrixes make "impacts" of radius 15 around each cue, while
        grid cells only make "impacts" of radius 4
        """
        # NOTE/WARNING:
        # The following portion of code is ported "as is" from the original implementation
        # in order to replicate the *exact* same behavior. However, the way that this method
        # works is questionnable perfomance-wise AND on a higher conceptual level. Comments
        # are my own. @TODO: Reconsider implementation

        # 1. Verify if the cue already exists and if so, remove it
        # remark: this mechanism relies ENTIRELY on rounding to find matches(redundant data),
        # in turn avoiding infinite growth of the list of cues and memory overflow. That is
        # very janky and probably relatively inefficient as well...

        # NOTE: this needs to be a while loop, as python doesn't allow removing elements
        # as the list is being iterated through
        new_cues_list = new_cues.tolist()
        i = 0
        while i < len(new_cues_list):
            new_cue = new_cues_list[i]

            d, theta = round(new_cue.d), round(new_cue.theta)
            for cue in self.context_cues:
                if (new_cue.cue_type == cue.cue_type and 
                    d == round(cue.d) and
                    theta == round(cue.theta)):
                    del new_cues_list[i]
                    i -= 1
                    break

            i += 1

        if len(new_cues_list) == 0:
            return
        # 2. Add the points that 'survived'
        self.context_cues: np.ndarray = np.append(self.context_cues, new_cues_list)

        # 3. Update the context matrix (@TODO/WARNING: not same behavior as original impl in place cell)
        # self.__compute_context_matrix()
        self.context_matrix = _compute_context_matrix(self.context_cues)

    # OLD METHOD for converting array of ContextCue to numeric array
    # def __get_cues_as_array(self):

    #     # @TODO: put this in an njit function to avoid boxing overhead (as context_cues are a jitclass)
    #     return np.array([(int(cue.theta) % 360, int(cue.d_2), int(cue.cue_type)) for cue in self.context_cues])
    #     #return self.context_cues.tolist()   

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
def _compute_context_matrix(context_cues: np.array) -> np.ndarray:
    """
    compute the context matrix from the list of context cues
    NOTE: converting this method to numba JIT requires it to
    not use object attributes, thus the need for arguments
    and return value
    """

    # The complex matrix is a discretization of polar space
    context_matrix = np.zeros((360,100,2)) #@TODO make resolution flexible @TODO only 2 types?

    # Spread size: the size of the "impact" that each cue makes in the matrix
    spread_size = 4 # in original code, this is 16 for place cells and 4 for grid cells
    # Also, original code had a bug causing asymetrical "impacts" =, which is fixed in this implementation

    for cue in context_cues:

        d_int = int(cue[3]) # @TODO: use d' (tanh form)
        angle_int = int(cue[1]) # @TODO not interchange degrees and indexes
        cue_type = int(cue[2]) # @TODO: filter by type

        #print(angle_int, d_int, cue_type)

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

    # =========================================================================================================
    # NAIVE IMPLEMENTATION.
    # OBSOLETE BECAUSE OUTPERFORMED BY NUMBA
    # def _compute_context_matrix(self):
    #     """
    #     compute the context matrix from the list of context cues
    #     NOTE: converting this method to numba JIT requires it to
    #     not use object attributes, thus the need for arguments
    #     and return value
    #     """

    #     # The complex matrix is a discretization of polar space
    #     self.context_matrix = np.zeros((360,100,2)) #@TODO make resolution flexible @TODO only 2 types?

    #     # Spread size: the size of the "impact" that each cue makes in the matrix
    #     spread_size = 4 # in original code, this is 16 for place cells and 4 for grid cells
    #     # Also, original code had a bug causing asymetrical "impacts" =, which is fixed in this implementation

    #     for cue in self.context_cues:

    #         angle_int = int(cue.theta) % 360 # @TODO not interchange degrees and indexes
    #         d_int = int(cue.d_2) # @TODO: use d' (tanh form)
    #         cue_type = int(cue.cue_type) # @TODO: filter by type

    #         #print(angle_int, d_int, cue_type)

    #         # modify the values around the point
    #         # @TODO: numpy-ify
    #         for i in range(-spread_size, spread_size + 1): #@TODO make bounds flexible (also change /5 in val)
    #             for j in range(-spread_size, spread_size + 1):
    #                 dist_as_index = d_int + i
    #                 angle_as_index = (angle_int + j) % 360
    #                     #@TODO: why does angle need to be checked again here ? weird shenanigans
    #                 if dist_as_index >= 0 and dist_as_index < 100 and angle_as_index >=0 and angle_as_index < 360:
    #                     val = 1 - max(abs(i), abs(j))/(spread_size + 1) # 1 at i=j=0, then lower as i or j increases
    #                     if val > self.context_matrix[angle_as_index][dist_as_index][cue_type]:
    #                         self.context_matrix[angle_as_index][dist_as_index][cue_type] = val

    # =========================================================================================================
    # NUMPY-IFIED CODE.
    # OBSOLETE BECAUSE OUTPERFORMED BY NUMBA
    # def __fast_compute_context_matrix(self):
    #     # Set up the context matrix with dimensions (360, 100, 2)
    #     context_matrix = np.zeros((360, 100, 2))

    #     # Define the size of the impact matrix
    #     spread_size = 4
    #     impact_size = spread_size*2 + 1

    #     # Compute the impact matrix
    #     # impact_matrix = np.zeros((impact_size, impact_size))
    #     # for i in range(impact_size):
    #     #     for j in range(impact_size):
    #     #         impact_matrix[i, j] = 1 - max(abs(i - 4), abs(j - 4)) / (spread_size + 1)
    #     row_indices, col_indices = np.indices((impact_size, impact_size))
    #     impact_matrix = 1 - np.maximum(np.abs(row_indices - spread_size), np.abs(col_indices - spread_size))/(spread_size + 1)


    #     points = np.array([(int(cue.theta) % 360, int(cue.d_2), int(cue.cue_type)) for cue in self.context_cues])
    #     # Iterate over each cue/point
    #     for point in points:
    #         # Get the indices of the point in the context matrix
    #         theta_idx, d_2_idx, cue_idx = point

    #         # Compute the indices of the slice that will be updated
    #         theta_indices = np.arange(theta_idx - spread_size, theta_idx + spread_size + 1) % 360
    #         d_2_indices = np.clip(np.arange(d_2_idx - spread_size, d_2_idx + spread_size + 1), 0, 99)
    #         cue_indices = np.array([cue_idx])

    #         # Create a 3D slice of the context matrix around the point
    #         slice_3D = context_matrix[theta_indices[:, None], d_2_indices, cue_indices]

    #         # # Create a 2D slice of the impact matrix that matches the shape of the 3D slice
    #         # slice_2D = impact_matrix[(theta_indices - theta_idx + spread_size)[:, None],
    #         #                         (d_2_indices - d_2_idx + spread_size)]
    #         # Create a 2D slice of the impact matrix that matches the shape of the 3D slice
    #         slice_2D = impact_matrix[:, (d_2_indices - d_2_idx + spread_size)]

    #         # Update the 3D slice with the values from the impact matrix
    #         slice_3D = np.maximum(slice_3D, slice_2D)

    #         # Assign the updated 3D slice back to the context matrix
    #         context_matrix[theta_indices[:, None], d_2_indices, cue_indices] = slice_3D


    #     self.context_matrix = context_matrix


