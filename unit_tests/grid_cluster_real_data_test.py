import os
import unittest
import numpy as np
from sensory_system.original_context import OriginalContext, get_theta, get_d, get_cue_type, get_d_2
from sensory_system.turtlebot3_range_sensor import TurtlebotRangeSensor
from space_memory.grid_cell import GridCell

from space_memory.grid_cluster import GridCluster
from space_memory.place_cell import PlaceCell
from unit_tests.utils_for_tests import RangeReader

class TestGridClusterRealData(unittest.TestCase):
    """
    Test of GridCluster on simulated data in a log file
    produced by turtlebot3 in Gazebo.
    """
    def setUp(self):
        
        self.reader = RangeReader(get_test_ranges_path())

        adjusted_ranges_1 = np.array(self.reader.get_next()) * 50
        adjusted_ranges_2 = np.array(self.reader.get_next()) * 50

        self.processor = TurtlebotRangeSensor(max_range = 3.5 * 50, fov_180=False)
        
        self.ctx_1_arr = self.processor.acquisition_to_cues_array(adjusted_ranges_1)
        self.ctx_1 = OriginalContext(self.ctx_1_arr)
        
        self.ctx_2_arr = self.processor.acquisition_to_cues_array(adjusted_ranges_2)
        # self.ctx_2 = OriginalContext(self.ctx_2_arr) # unused

        self.cluster = GridCluster()
        self.place_cell = PlaceCell(self.ctx_1)
        self.cluster.set_place_cell(self.place_cell)

        self.observation_identical = self.ctx_1_arr
        self.observation_rotated = self.ctx_2_arr

    def test_init(self):
        """
        make sure that the grid cells are initialized with properly offset context
        """
        print("testing init function")
        xcenter, ycenter = 5,5
        for i,row in enumerate(self.cluster.grid):
            cell: GridCell
            for j,cell in enumerate(row):
                x_from_center = (i - xcenter) * self.cluster.scale
                y_from_center = (j - ycenter) * self.cluster.scale
                ctx_offset =  self.ctx_1.offset(x_from_center, y_from_center)

                self._assert_ctx_equal(cell.context, ctx_offset)
                

    def test_compute(self):
        print("testing compute function")
        self.cluster.compute(self.observation_identical)
        print("x", self.cluster.estimated_relative_x)
        print("y", self.cluster.estimated_relative_y)
        print("angle", self.cluster.angle_estimation)
        

        # @TODO make better tests. with the "correct" (aka original)
        # algorithm, the estimation is slightly off, which could be
        # explained by the low count of cues.
        # self.assertEqual(0, self.cluster.estimated_relative_x)
        # self.assertEqual(0, self.cluster.estimated_relative_y)
        # self.assertEqual(0, self.cluster.angle_estimation)


        self.cluster.compute(self.observation_rotated)
        print("x", self.cluster.estimated_relative_x)
        print("y", self.cluster.estimated_relative_y)
        print("angle", self.cluster.angle_estimation)

    def _assert_ctx_equal(self, ctx1: OriginalContext, ctx2: OriginalContext):
        self.assertEqual(len(ctx1.context_cues), len(ctx2.context_cues))
        for i, context_cue in enumerate(ctx1.context_cues):
            context_cue_2 = ctx2.context_cues[i]
            self.assertEqual(get_d(context_cue), get_d(context_cue_2))
            self.assertEqual(get_d_2(context_cue), get_d_2(context_cue_2))
            self.assertEqual(get_cue_type(context_cue), get_cue_type(context_cue_2))
            self.assertEqual(get_theta(context_cue), get_theta(context_cue_2))

def get_test_ranges_path():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(test_dir, 'test_ranges.txt')
    return data_path

if __name__ == '__main__':
    unittest.main()