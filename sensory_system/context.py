"""
Defines a context.

A context is a representation of the environment. More
specifically, it represents the way that an agent (robot)
perceives its environment.

A context can be derived from raw sensor data. 
A context can also be predicted (for example, from another
context and a displacement).

A context can be modified or updated.

Two contexts can be compared to each other to determine
their similarity.

NOTE:
This is only a generic interface. The default implementation for
contexts is OriginalContext. New contexts can be defined and used,
as long as the given functions are defined.
"""

class Context:
    """ This is a generic interface that can be used to define contexts """

    def __init__(self, sensor_data):
        pass

    # def offset_context(self, displacement) -> 'ContextInterface':
    #     """Compute the offset of the context by a displacement"""

    def update(self, new_information):
        """
        Update the context with a new reading. Currently unused,
        as FOV is 360 so not much new information should be received
        """

    def offset(self, x_offset: float, y_offset: float) -> 'Context':
        """
        Offsets the context by a given displacement. Used in grid cell module
        to predict observable contexts after a displacement.
        """

    def rotate(self, angle_in_degrees) -> 'Context':
        """
        Rotates the context by a given angle.
        """

    def compare(self, observation):
        """
        Compares context to an observation. Used in
        place and grid cells to compute activity.
        """