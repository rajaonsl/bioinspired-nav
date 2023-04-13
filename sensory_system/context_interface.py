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
"""

class ContextInterface:
    """ This is a generic interface that can be used to define contexts """

    def __init__(self, sensor_data):
        pass

    # def offset_context(self, displacement) -> 'ContextInterface':
    #     """Compute the offset of the context by a displacement"""

    def update_context(self, new_information):
        pass

    def compare(self, other: 'ContextInterface'):
        pass