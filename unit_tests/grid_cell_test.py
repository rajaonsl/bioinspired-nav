import unittest
import numpy as np

from sensory_system.original_context import OriginalContext, ContextCueType, create_cue
from space_memory.grid_cell import GridCell

class TestOriginalContext(unittest.TestCase):
    def setUp(self):
        self.cell = GridCell()
        self.cue1 = create_cue(distance=50, theta=10, cue_type=ContextCueType.OBSTACLE)
        self.cue2 = create_cue(distance=51, theta=18, cue_type=ContextCueType.OBSTACLE)

        ctx_array = np.array([self.cue1, self.cue2])
        self.cell.set_context(OriginalContext(ctx_array))

        self.test_observation_identical = ctx_array
        self.test_observation_rot20 = np.array([
            create_cue(distance=50, theta=30, cue_type=ContextCueType.OBSTACLE),
            create_cue(distance=51, theta=38, cue_type=ContextCueType.OBSTACLE)
        ])


    def test_compute(self):
        self.cell.compute(self.test_observation_identical)
        self.assertEqual(0, self.cell.max_activity_angle)
        self.cell.compute(self.test_observation_rot20)
        self.assertEqual(360 - 20, self.cell.max_activity_angle)

if __name__ == '__main__':
    unittest.main()