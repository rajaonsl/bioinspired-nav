# import math
# import numpy as np 

# class GridCell:
#     """
#     @TODO
#     Grid Cells have a context that represents their environment.
#     ...
#     This context is comprised of a fixed number of points, depending on the
#     sensors used. 
#     """
#     def __init__(self):
#         """
#         Initialize a GridCell

#         attributes:
#         - points_list: list of points. Each point is in the following format:
#             [d, d2, theta, x, y, x2, y2, ????]
#         """
#         #self.points_list = np.array([]) # context as a list of points
#         self.context = np.zeros((360, 100, 2)) #@TODO set parameters globally
#         self.activity = np.zeros((360)) #@TODO set parameters globally

#         self.max_activity = 0.
#         self.max_activity_angle = 0.


#     #def set_context(self, points: np.array, x_offset: int, y_offset: int):
#     def set_context(self, points: np.array, x_offset: int, y_offset: int):
#         """
#         Compute the predicted context of the grid cell (self), based a given
#         context (envt as a list of points) and offset.
#         input:
#             > points:   a list of points, where each point is represented as
#             an array of the following form: [d, d2, theta, x, y, x2, y2, ????]
#             the last value seems to be binary and indicate the type of point
#             (normal obstacle vs orange landmark)
            
#             > x_offset: int
            
#             > y_offset: int
#         """

#         # # @TODO: replace for loop with numpy operation
#         # # @TODO actually just remove this ig
#         # # For each point:
#         # for i, point in enumerate(points):

#         #     # compute their x and y according to the offset
#         #     x = point[3] + x_offset
#         #     y = point[4] + y_offset

#         #     # compute polar coordinates
#         #     d = math.sqrt(x**2 + y**2)  # pythagoras
#         #     theta = math.atan2(x,y)   # in radians

#         #     # @TODO understand this ("polar atan coordinates")
#         #     d2 = 100*math.tanh(d/100)

#         #     x2 = d2 * math.cos(theta) #@TODO understand
#         #     y2 = d2 * math.sin(theta) #@TODO understand

#         #     self.points_list[i] = np.array([d2, theta, x, y, x2, y2, point[7], d])

#         # @TODO: initialize "context"
#         for point_index, point in enumerate(points):
#             dist: int = 0 #
#             a: int = 0 # @TODO: angle and index are used interchangably (convenient
#             # if each measurement is a egree apart.). This needs to change and be more flexible
#             c: int = 0 # type of obstacle
#             val: float = 0 #

#             # @TODO: make sure a is between 0 and 360
#             # @TODO: take c into account
#             for i in range (-4, 4):
#                 for j in range (-4, 4):
#                     if (dist + i > 0 and dist + 1 < 100 and a + j < 360):
#                         # speculation: the /5 has to do with the bounds of the for i,j loops
#                         val = 1 - max(abs(i), abs(j))/5 # @TODO wtf? undestand dis
#                         if (val > self.context[a+j][dist+i][c]):
#                             self.context[a+j][dist+i][c] = val



#     def compute_activity(self, environment: np.array):
#         """
#         Compute the Grid Cell's activity, for all possible orientations.
#         """

#         n = 360 #@TODO sort out the degree/radian problem
#         fov = 180 #@TODO: same

#         # Rewrote computation according to the paper:
#         for r in range(0, n): #for each point in the context
#             sum_ = 0.
#             context_point: np.array = self.context[r]
#             for a in range(0, fov): #for each point in the FoV
#                 environment_point = environment[a]
#                 sum_ += self.__f(self.__distance(context_point, environment_point))

#             if sum_ > self.max_activity:
#                 self.max_activity = sum_
#                 self.max_activity_angle = r

#         # """
#         # # NOTE: Simon's java code
#         # for r in range(0, n):

#         #     sum: float = 0.

#         #     for a in range(0, fov):

#         #         # @TODO is this second index to distinguish landmarks from obstacles ?
#         #         # If so, might want to remove or generalize
#         #         if environment[a][0] >= 0:
#         #             if environment[a][7] == 0:
#         #                 pass...
#         #             elif environment[a][7] == 1:
#         #                 pass...

#         #     self.activity[r] = sum**2 / (180**2) # @TODO check if float division
#         #     if self.activity[r] > max:
#         #         self.max_activity = self.activity[r]
#         #         self.max_activity_angle = r
#         # """



#     #@TODO: define
#     def __distance(self, point_a, point_b):
#         x_a, y_a = point_a[3], point_a[4]
#         x_b, y_b = point_b[3], point_b[4]
#         return math.sqrt((x_a - x_b)**2 + (y_a - y_b)**2)

#     #@TODO: define
#     def __f(self, x):
#         return 1/x if x != 0. else np.inf
