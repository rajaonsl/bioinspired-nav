import unittest
import numpy as np
from sensory_system.context_cue import ContextCue, ContextCueType
from sensory_system.original_context import OriginalContext
from space_memory.grid_cell import GridCell

class TestOriginalContext(unittest.TestCase):
    def setUp(self):
        self.cell = GridCell()
        self.cue1 = ContextCue(50, 10, ContextCueType.OBSTACLE)
        self.cue2 = ContextCue(51, 18, ContextCueType.OBSTACLE)

        ctx_array = np.array([self.cue1, self.cue2])
        self.cell.set_context(OriginalContext(ctx_array))

        self.test_observation_identical = ctx_array
        self.test_observation_rot20 = np.array([
            ContextCue(50, 30, ContextCueType.OBSTACLE),
            ContextCue(51, 38, ContextCueType.OBSTACLE)
        ])


    def test_compute(self):
        self.cell.fast_compute(self.test_observation_identical)
        self.assertEqual(0, self.cell.max_activity_angle)
        self.cell.compute(self.test_observation_rot20)
        self.assertEqual(360 - 20, self.cell.max_activity_angle)

    # def test_fast_compute(self):
    #     self.cell.fast_compute(self.test_observation_identical)
    #     self.assertEqual(0, self.cell.max_activity_angle)
    #     self.cell.compute(self.test_observation_rot20)
    #     self.assertEqual(360 - 20, self.cell.max_activity_angle)

    # def test_fast_compute_2(self):
    #     self.cell.fast_compute_2(self.test_observation_identical)
    #     self.assertEqual(0, self.cell.max_activity_angle)
    #     self.cell.compute(self.test_observation_rot20)
        # self.assertEqual(360 - 20, self.cell.max_activity_angle)

    # def test_fast_compute_3(self):
    #     self.cell.fast_compute_3(self.test_observation_identical)
    #     self.assertEqual(0, self.cell.max_activity_angle)
    #     self.cell.compute(self.test_observation_rot20)
    #     self.assertEqual(360 - 20, self.cell.max_activity_angle)

if __name__ == '__main__':
    unittest.main()