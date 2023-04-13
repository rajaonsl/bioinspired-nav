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

import numpy as np

from sensory_system.context_interface import ContextInterface

class Context(ContextInterface): # @TODO: reconsider usefulness lol
    """ This is an implementation of ContextInterface for range measurements
    NOTE: not the original implementation
    NOTE: unfinished
    """

    def __init__(self, context_cues: np.ndarray):
        """
        context cues are expected as a numpy array of context cues (type ContextCue)
        """
        self.context_cues = context_cues

    def compare(self, other: 'Context') -> float:
        sum_ = 0
        for cue in self.context_cues:

            # performance hack to avoid method lookup in loop, see:
            # https://stackoverflow.com/questions/41781048/overhead-of-creating-classes-in-python-exact-same-code-using-class-twice-as-slo
            compare = cue.compare

            for other_cue in other.context_cues:
                sum_ += compare(other_cue)
        # @TODO: do something with the sum and return a result
