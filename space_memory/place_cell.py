# import numpy as np

import numpy as np
from numba import njit

from sensory_system.original_context import OriginalContext, get_theta, get_cue_type, get_d_2 #@TODO: use ContextInterface

class PlaceCell:

    # private static counter used to generate cell id
    __static_counter = 0


    #-------------------------------------------------------------------
    # @TODO: the place cell holding its center x,y indexes is a bad design pattern.
    # it makes the place cell dependant on the grid cluster implementation!
    def __init__(self, context: OriginalContext, center_x: int = 5, center_y: int = 5,
                 global_x = 0, global_y = 0):
        PlaceCell.__static_counter += 1
        self.id: int = PlaceCell.__static_counter
        self.context = context
        self.activity = 0
        self.neighbors: list['PlaceCell'] = []
        self.__neighbors_ids: list[int] = []
        self.center_x = center_x
        self.center_y = center_y


        # Currently only for displaying purposes
        self.global_x, self.global_y = global_x, global_y


    def compute(self, observation):
        self.activity = numba_fast_compute(observation, self.context.context_matrix) #@TODO: bad design pattern, relies on context implementation.
        # better: move compute to originalcontext

    #-------------------------------------------------------------------
    def addNeighbor(self, other: 'PlaceCell'):
        """ Add neighboring place cell """
        if other.id in self.__neighbors_ids:
            return
        
        self.neighbors.append(other)
        other.addNeighbor(self) # Reciprocity
        self.__neighbors_ids.append(other.id)


    #-------------------------------------------------------------------
    def checkNeighbors(self, relative_x, relative_y):
        """
        checks if the given relative position is closer to a neighbor than self
        """
        #@TODO implement


    #-------------------------------------------------------------------
    #@TODO reconsider usefulness
    def addPredecessor(self, other: 'PlaceCell'):
        pass

@njit
def numba_fast_compute(observation: np.ndarray, context_matrix: np.ndarray, minimum_matching_cues: int=3):
    """
    Compute activity for an observed context
    
    Optimized by Numba JIT compilation
    """

    # General idea in JAVA:
    # 1. compute matching of envt w/ PC context
    # 2. get best matching angle & value
    # 3. compute matching of PC context w/ envt context (at best angle)
    # 4. get best activity
    # 5. store (~=return) best activity 1 * best activity 2
    # one question: what ?? why ???

    #1. Compute the matching of the environment context with PC's context
    #2. get best angle & value
    # @TODO: solve disaster of a naming scheme
    max_activity_2, angle_of_max_activity_2 = 0., 0
    for r in range(0, 360):
        sum_: float = 0
        matches_count: int = 0 # Number of observed points that matches

        for ctx_cue in observation:
            
            # angle of the cue if the agent is rotated by r
            theta = int(get_theta(ctx_cue) - r)%360
            
            sum_ += context_matrix[theta, int(get_d_2(ctx_cue)), int(get_cue_type(ctx_cue))]
            matches_count+=1

        if (matches_count > minimum_matching_cues and sum_ > max_activity_2):
            max_activity_2 = sum_
            angle_of_max_activity_2 = r

    # Compute the matching of the PC's context with the envt (for the angle found)
    sum_ = 0
    for ctx_cue in observation:
        theta = int(get_theta(ctx_cue) + angle_of_max_activity_2 + 360) % 360 #@TODO clean up
        sum_ +=  context_matrix[theta, int(get_d_2(ctx_cue)), int(get_cue_type(ctx_cue))] #@TODO: move int cast to occupancy
    
    max_activity_1 = sum_/len(observation) #@TODO check non zero

    print("activity 1, 2:", max_activity_1, max_activity_2)

    return max_activity_1 * max_activity_2