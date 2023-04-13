# import numpy as np

import numpy as np
from sensory_system.context_cue import ContextCue

from sensory_system.original_context import OriginalContext #@TODO: use ContextInterface

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


    #-------------------------------------------------------------------
    # @TODO: reconsider input type (currently array of ContextCue)
    # @TODO: move context comparison in the context class
    # @TODO: improve performance
    # @TODO: why 2 activities ???
    def compute(self, observation: np.ndarray):
        """ Compute activity for an observed context """

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
                theta = int(ctx_cue.theta - r + 720)%360 #@TODO clean up, and move int cast to occupancy fct
                
                # NEW CODE (no concern with FOV)
                sum_ += self.context.occupancy(theta, int(ctx_cue.d_2), ctx_cue.cue_type)
                matches_count+=1

                ## OLD CODE
                # if (theta < 180): # if angle not in FOV (@TODO make flexible)
                #     sum_ += self.context.occupancy(theta, int(ctx_cue.d_2), ctx_cue.cue_type)
                #     matches_count += 1

            if (matches_count > 3 and sum_ > max_activity_2): #@TODO make flexible
                max_activity_2 = sum_
                angle_of_max_activity_2 = r

        # Compute the matching of the PC's context with the envt (for the angle found)
        sum_ = 0
        ctx_cue: ContextCue
        for ctx_cue in observation:
            theta = int(ctx_cue.theta + angle_of_max_activity_2 + 360) % 360 #@TODO clean up
            sum_ += self.context.occupancy(theta, int(ctx_cue.d_2), ctx_cue.cue_type) #@TODO: move int cast to occupancy
        
        max_activity_1 = sum_/len(observation) #@TODO check non zero

        print("activity 1, 2:", max_activity_1, max_activity_2)

        self.activity = max_activity_1 * max_activity_2


    #-------------------------------------------------------------------
    def addNeighbor(self, other: 'PlaceCell'):
        """ Add neighboring place cell """
        if other.id in self.__neighbors_ids:
            return
        
        self.neighbors.append(other)
        self.__neighbors_ids.append(other.id)

        # @TODO: should 'self' be added as a neighbor of 'other' ? (i.e. reciprocity)


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

