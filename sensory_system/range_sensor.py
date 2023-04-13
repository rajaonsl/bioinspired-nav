
import numpy as np

from sensory_system.context_interface import ContextInterface

class RangeSensor:
    
    def __init__(self, max_range: float, min_range: float = 0., field_of_view: float = 360.):
        """
        field_of_view: in degrees
        """

        self.max_range = max_range
        self.min_range = min_range
        self.field_of_view = field_of_view

    def process_acquisition(self, raw_sensor_data: np.ndarray) -> ContextInterface:
        pass
        # cues_list = [] # @TODO: numpy?
        # angle = 0
        # angle_step = self.field_of_view/(len(sensor_measurements) - 1) # degrees
        # for measurement in sensor_measurements:
        #     # Create the cue associated with the measurement 
        #     # @TODO: corner detection, etc.
        #     cue = ContextCue(d = measurement, theta = angle, cue_type = ContextCueType.OBSTACLE)
        #     # Add it to the context
        #     cues_list.append(cue) # TEMP: save measurement polar coordinates and type 0
            
        #     angle += angle_step

    #@TODO remove, move this code in process acquisition
    def acquisition_to_cues_array(self, raw_sensor_data) -> np.ndarray:
        pass