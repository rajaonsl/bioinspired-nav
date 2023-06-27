"""
Generic class defining a range sensor.

The specific implementation deals with the raw sensor measurements,
is responsible for any pre-processing or filtering needed, depending
on sensor specifications.

The specific implementation is also given the IMPORTANT task of converting
raw sensor measurements into a Context. The developper should keep in mind
that Context and Range Sensor are coupled when writing new implementations.
"""
import numpy as np

from sensory_system.context import Context

class RangeSensor:

    def __init__(self, max_range: float, min_range: float = 0., field_of_view: float = 360.):
        """
        field_of_view: in degrees
        """

        self.max_range = max_range
        self.min_range = min_range
        self.field_of_view = field_of_view

    def process_acquisition(self, raw_sensor_data: np.ndarray, spread_size: int=16) -> Context:
        """
        Converts raw sensor data into a context.
        """
