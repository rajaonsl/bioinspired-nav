from enum import IntEnum  #@TODO: investigate fastenum
from numba.experimental import jitclass

import math

# class ContextCueType(IntEnum):
#     OBSTACLE = 0 # is 0 ok ?
#     CORNER = 1
#     LANDMARK = 2

# # @TODO: reconsider usefulness
# @jitclass
# class ContextCue:
#     """
#     represents an element of a context.
#     """
#     # Type annotation for JIT
#     d: float
#     theta: float
#     cue_type: int
#     d_2: float

#     def __init__(self, d, theta, cue_type: ContextCueType):
#         # Assert that the range sensor did its job correctly
#         assert d != math.inf

#         self.d = d
#         self.theta = theta # degrees
#         self.cue_type: ContextCueType = cue_type
#         self.d_2 = 100*math.tanh(d/100) # used in original_context (@TODO isolate in child class, probably rename!)
        
#         # @TODO: remove int ? maybe
#         # self.d = int(d)
#         # self.theta = int(theta) # degrees
#         # self.cue_type: ContextCueType = cue_type
#         # self.d_2 = int(100*math.tanh(d/100)) # used in original_context (@TODO isolate in child class, probably rename!)
#         #@TODO: add x,y ?

#     def compare(self, other: 'ContextCue') -> float:
#         """
#         returns a float: 1. -> very similar, 0. -> not similar
#         """
#         #@TODO implement or remove

#     def offset(self, x_offset, y_offset) -> 'ContextCue':
#         """
#         shift context cue by cartesian offset
#         """
#         # 1. get cartesian coordinates of self
#         theta_radian = math.radians(self.theta)
#         x = self.d * math.cos(theta_radian)
#         y = self.d * math.sin(theta_radian)

#         # 2. get shifted coordinates
#         new_x, new_y = x + x_offset, y + y_offset
#         new_d = math.sqrt(new_x**2 + new_y**2)
#         new_theta = math.degrees(math.atan2(new_y, new_x))

#         # 3. return shifted cue
#         return ContextCue(new_d, new_theta, self.cue_type)
    
#     def from_cartesian(self, x, y, type_: ContextCueType = ContextCueType.OBSTACLE) -> 'ContextCue':
        
#         d = math.sqrt(x**2 + y**2)
#         theta = math.degrees(math.atan2(y, x))

#         return ContextCue(d, theta, type_)
    
#     def get_cartesian(self):

#         theta_radian = math.radians(self.theta)
#         x = self.d * math.cos(theta_radian)
#         y = self.d * math.sin(theta_radian)
#         return (x,y)
