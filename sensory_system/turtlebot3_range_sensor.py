
import numpy as np

from sensory_system.original_context import OriginalContext
from sensory_system.range_sensor import RangeSensor


class TurtlebotRangeSensor(RangeSensor):
    """
    Implementation of a range sensor specific to the turtlebot3 LiDAR
    in the Gazebo ROS simulation.
    """
    SCALING = 1 #@TODO remove

    def __init__(self, max_range = 3.5, min_range = 0., fov_180: bool = True):
        """
        Initialize sensor with default data.
        The robot's sensor has a field of view of 360°
        and gives 360 range measurements (1 per degree)
        """
        super().__init__(max_range * TurtlebotRangeSensor.SCALING, min_range)
        self.is_fov_180 = fov_180 #@TODO: ugly solution, support all FOVs
    
    #@TODO: go from OriginalCOntext -> ContextInterface
    def process_acquisition(self, raw_sensor_data: np.ndarray, spread_size: int=16) -> OriginalContext:
        """
        Return a context from turtlebot3 raw sensor data
        (WARNING: currently only retains 180 degrees)
        """
        
        # NEW CODE (cue as array)
        cues = self.acquisition_to_cues_array(raw_sensor_data)
        return OriginalContext(cues, spread_size=spread_size)

        # # OLD CODE (cues as objects)
        # cues = self.acquisition_to_cues_array(raw_sensor_data * TurtlebotRangeSensor.SCALING, self.min_range, self.max_range)
        # return OriginalContext(cues)
    
    # NEW CODE REPRESENTING CUES
    def acquisition_to_cues_array(self, raw_sensor_data) -> np.ndarray:
        return self.__acquisition_to_cues_array(raw_sensor_data=raw_sensor_data,
                                                min_range=self.min_range*TurtlebotRangeSensor.SCALING,
                                                max_range=self.max_range*TurtlebotRangeSensor.SCALING) 

    # @njit @TODO: OPTIMIZE WITH NUMBA
    def __acquisition_to_cues_array(self, raw_sensor_data: np.ndarray, min_range=0, max_range=3.5) -> np.ndarray:

        valid_distances_index = np.logical_and(raw_sensor_data > min_range, raw_sensor_data < max_range).nonzero()[0]
        raw_sensor_data = _scale_values(raw_sensor_data, self.min_range, self.max_range) #Scale values

        print("valid distances: ", len(valid_distances_index))

        valid_distances = raw_sensor_data[valid_distances_index]
        types_arr = np.zeros((len(valid_distances)))
        tanh_arr = 100*np.tanh(valid_distances/100)

        return np.vstack((valid_distances, valid_distances_index, types_arr, tanh_arr)).transpose()

    # # OLD CODE REPRESENTING CUES AS OBJECTS
    # #@TODO remove, move this code in process acquisition
    # def acquisition_to_cues_array_OLD(self, raw_sensor_data) -> np.ndarray:
    #     """
    #     In this specific instance, we restrain the field of view to 180 degrees
    #     so it plays nicely with the original algorithm.
    #     @TODO: make field of view flexible!
    #     """
    #     cues: list[ContextCue] = []
    #     if self.is_fov_180:
    #         distances = np.concatenate((raw_sensor_data[270:], raw_sensor_data[:90]))
    #     else:
    #         distances = raw_sensor_data
    #     for i, measurement in enumerate(distances):
    #         if measurement < self.max_range and measurement > self.min_range:
    #             cues.append(
    #                 ContextCue(d=measurement, theta=i, cue_type=ContextCueType.OBSTACLE)
    #             )
    #     return np.array(cues)
    
    # #@TODO remove, TMP test function
    # def process_acquisitions_to_int(self, raw_sensor_data) -> OriginalContext:
    #     """
    #     In this specific instance, we restrain the field of view to 180 degrees
    #     so it plays nicely with the original algorithm.
    #     @TODO: make field of view flexible!
    #     """
    #     cues: list[ContextCue] = []
    #     distances = raw_sensor_data[270:] + raw_sensor_data[:90]
    #     for i, measurement in enumerate(distances):
    #         if measurement < self.max_range and measurement > self.min_range:
    #             cues.append(
    #                 ContextCue(d=measurement, theta=i, cue_type=ContextCueType.OBSTACLE)
    #             )
    #     return np.array(cues)


def _scale_values(values: np.ndarray, min_, max_, new_min=0, new_max=120):
    """ Scales values proportionnaly to the desired interval"""
    return (values - min_)*(new_max - new_min)/(max_ - min_) + new_min