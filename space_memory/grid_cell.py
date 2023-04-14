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
    # @TODO: reconsider input (type of 'observation')
    # @TODO 2: reconsider position: should comparing contexts be
    # defined in the grid cell itself ??
    # ATTOW: np array of context cues
    def compute(self, observation: np.ndarray):
        """ Compute the activity of the cell for a given observation.
        expects a numpy array of context cues (ContextCue)
        result is stored in self.activity, self.max_activity
        and self.max_activity_angle"""

        assert self.context is not None

        self.max_activity = 0
        for i, _ in enumerate(self.activity):

            sum_ = 0.

            # performance hack to avoid method lookup in loop
            # get_occupancy = self.context.occupancy
            mat = self.context.context_matrix
            
            # @TODO
            # This should work in my head, however it appears that I am victim
            # of a skill issue 
            for ctx_cue in observation:
                # @TODO NOTE: weird stuff in original code, see if it was important
                theta = int(ctx_cue.theta + i) % 360
                #val = get_occupancy(theta, int(ctx_cue.d_2), ctx_cue.cue_type)
                val = mat[theta][int(ctx_cue.d_2)][ctx_cue.cue_type]
                sum_ += val

            # @TODO
            # Temporary code that *definitely works* but is uglier than what's above :/
            # <nothing> lol

            self.activity[i] = sum_**2/(len(observation)**2)
            if self.activity[i] > self.max_activity:
                self.max_activity = self.activity[i]
                self.max_activity_angle = i


    #-------------------------------------------------------------------
    # Sypposedly faster thanks to numpy. Not really clear if that's the case.
    # @TODO 2: reconsider position: should comparing contexts be
    # defined in the grid cell itself ??
    def fast_compute(self, observation: np.ndarray):
        """Compute the activity of the cell for a given observation using a faster numpy implementation.
        Expects a numpy array of context cues (ContextCue).
        Result is stored in self.activity, self.max_activity, and self.max_activity_angle."""
        assert self.context is not None

        # Extract theta, d_2, and cue_type from observation
        observation = np.array([(int(cue.theta) % 360, int(cue.d_2), int(cue.cue_type)) for cue in observation])

        # Retrieve context matrix
        mat = self.context.context_matrix

        # Compute values for all orientations
        vals = np.zeros(360)
        for i, _ in enumerate(self.activity):
            # Fetch values for the current orientation
            indices = ((observation[:,0] + i) % 360, observation[:,1], observation[:,2])
            vals[i] = np.sum(mat[indices])

        self.activity = (vals/len(observation))**2
        self.max_activity_angle = np.argmax(self.activity)
        self.max_activity = self.activity[self.max_activity_angle]


    #-------------------------------------------------------------------
    def faster_compute(self, observation: np.ndarray):
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

        # performance hack to avoid method lookup in loop
        # get_occupancy = self.context.occupancy
        
        # @TODO
        # This should work in my head, however it appears that I am victim
        # of a skill issue 
        for ctx_cue in observation:
            # @TODO NOTE: weird stuff in original code, see if it was important
            theta = (int(ctx_cue[1]) + i) % 360
            d_2 = int(ctx_cue[3])
            cue_type = int(ctx_cue[2]) #@TODO: replace manual indexing with getters
            #val = get_occupancy(theta, int(ctx_cue.d_2), ctx_cue.cue_type)
            val = context_matrix[theta][d_2][cue_type]
            sum_ += val

        # @TODO
        # Temporary code that *definitely works* but is uglier than what's above :/
        # <nothing> lol

        activity[i] = sum_**2/(len(observation)**2)
        if activity[i] > max_activity:
            max_activity = activity[i]
            max_activity_angle = i
    
    return activity, max_activity, max_activity_angle