""" Grid Cell module"""
import numpy as np
from numba import njit

from sensory_system.original_context import OriginalContext

class GridCell:
    """
    A grid cell is active if the observed context corresponds to the
    saved context for some angles of rotation.
    """

    #-------------------------------------------------------------------
    def __init__(self):
        self.max_activity = 0
        self.max_activity_angle = 0
        self.activity = np.zeros(360) # @TODO make resolution flexible
        self.context = None


    #-------------------------------------------------------------------
    # @TODO: reconsider usefulness
    def set_context(self, context: OriginalContext):
        self.context = context

    #-------------------------------------------------------------------
    def compute(self, observation: np.ndarray):
        assert self.context is not None
        # OLD CODE: cue as object
        # obs_as_array = np.array([(int(cue.theta), int(cue.d_2), int(cue.cue_type)) for cue in observation])
        self.activity, self.max_activity, self.max_activity_angle =\
            numba_fast_compute(self.context.context_matrix, observation)


@njit
def numba_fast_compute(context_matrix: np.ndarray, observation: np.ndarray): #@TODO: move in OriginalContext
    """
    Compute the activity of the cell for a given observation using a faster numpy implementation.
    Expects two numpy arrays of int
    Result is returned"""

    max_activity = 0
    max_activity_angle = 0
    activity = np.zeros(360)
    for i, _ in enumerate(activity):

        sum_ = 0.
        
        for ctx_cue in observation:
            # @TODO NOTE: weird stuff in original code, see if it was important
            theta = (int(ctx_cue[1]) + i) % 360
            d_2 = int(ctx_cue[3])
            cue_type = int(ctx_cue[2]) #@TODO: replace manual indexing with getters
            #val = get_occupancy(theta, int(ctx_cue.d_2), ctx_cue.cue_type)
            val = context_matrix[theta][d_2][cue_type]
            sum_ += val

        activity[i] = sum_**2/(len(observation)**2)
        if activity[i] > max_activity:
            max_activity = activity[i]
            max_activity_angle = i
    
    return activity, max_activity, max_activity_angle