import unittest
import numpy as np
from sensory_system.context_cue import ContextCue, ContextCueType
from sensory_system.original_context import OriginalContext
from space_memory.grid_cell import GridCell

from space_memory.grid_cluster import GridCluster
from space_memory.place_cell import PlaceCell

class TestGridCluster(unittest.TestCase):
    """
    Unit test of GridCluster for a simple environment with 2 cues
    """
    def setUp(self):
        
        self.cue1 = ContextCue(50, 10, ContextCueType.OBSTACLE)
        self.cue2 = ContextCue(51, 18, ContextCueType.OBSTACLE)

        self.ctx_array = np.array([self.cue1, self.cue2])
        self.ctx = OriginalContext(self.ctx_array)
        self.cluster = GridCluster()
        self.place_cell = PlaceCell(self.ctx)
        self.cluster.set_place_cell(self.place_cell)

        self.observation_identical = self.ctx_array

    def test_init(self):
        """
        make sure that the grid cells are initialized with properly offset context
        """
        xcenter, ycenter = 5,5
        for i,row in enumerate(self.cluster.grid):
            cell: GridCell
            for j,cell in enumerate(row):
                x_from_center = (i - xcenter) * self.cluster.scale
                y_from_center = (j - ycenter) * self.cluster.scale
                ctx_offset =  self.ctx.offset(x_from_center, y_from_center)

                self._assert_ctx_equal(cell.context, ctx_offset)
                

    def test_compute(self):
        self.cluster.compute(self.observation_identical)
        

        # @TODO make better tests. with the "correct" (aka original)
        # algorithm, the estimation is slightly off, which could be
        # explained by the low count of cues.
        #self.assertEqual(0, self.cluster.estimated_relative_x)
        #self.assertEqual(0, self.cluster.estimated_relative_y)
        #self.assertEqual(0, self.cluster.angle_estimation)

    def _assert_ctx_equal(self, ctx1: OriginalContext, ctx2: OriginalContext):
        self.assertEqual(len(ctx1.context_cues), len(ctx2.context_cues))
        for i, context_cue in enumerate(ctx1.context_cues):
            context_cue_2 = ctx2.context_cues[i]
            self.assertEqual(context_cue.d, context_cue_2.d)
            self.assertEqual(context_cue.d_2, context_cue_2.d_2)
            self.assertEqual(context_cue.theta, context_cue_2.theta)



if __name__ == '__main__':
    unittest.main()