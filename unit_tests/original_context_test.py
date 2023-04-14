import unittest
import numpy as np

# from sensory_system.context_cue import ContextCue, ContextCueType
from sensory_system.original_context import OriginalContext, ContextCueType, create_cue, cues_array_to_cartesian, get_theta, get_d_2

class TestOriginalContext(unittest.TestCase):
    def setUp(self):
        
        #self.cue1 = ContextCue(50, 30, ContextCueType.OBSTACLE)
        #self.cue2 = ContextCue(55, 35, ContextCueType.OBSTACLE)
        # self.cue1 = ContextCue(0, 0, ContextCueType.OBSTACLE)
        # self.cue2 = ContextCue(20, 250, ContextCueType.OBSTACLE)
        self.cue1 = create_cue(distance=0, theta=0, cue_type=ContextCueType.OBSTACLE)
        self.cue2 = create_cue(distance=20, theta=250, cue_type=ContextCueType.OBSTACLE)

        self.ctx1array = np.array([self.cue1, self.cue2])
        #ctx2arrat = np.array([self.cue1, self.cue2 ])

        self.context1 = OriginalContext(self.ctx1array)
        self.x_offset, self.y_offset = 4.2, -7.9
        self.off_context1 = self.context1.offset(self.x_offset, self.y_offset)

    def test_occupancy(self):
        
        theta = int(get_theta(self.cue1))
        d = int(get_d_2(self.cue1))

        self.assertEqual(
            1, self.context1.occupancy(theta,d))

        spread_size = 4
        for i in range(-spread_size, spread_size + 1):
            for j in range(-spread_size, spread_size + 1):
                if j < 0:
                    self.assertEqual(
                        0, self.context1.occupancy(theta+i, d+j))
                else:
                    self.assertNotEqual(
                        0, self.context1.occupancy(theta+i, d+j))
        
        self.assertEqual(0, self.context1.occupancy(34,0))
        self.assertEqual(0, self.context1.occupancy(4,7))


    # def test_fast_occupancy(self):
        
    #     # self.context1.blazing_fast_compute_context_matrix()

    #     theta = int(self.cue1.theta)
    #     d = int(self.cue1.d_2)

    #     self.assertEqual(
    #         1, self.context1.occupancy(theta,d))

    #     spread_size = 4
    #     for i in range(-spread_size, spread_size + 1):
    #         for j in range(-spread_size, spread_size + 1):
    #             self.assertNotEqual(
    #                 0, self.context1.occupancy(theta+i, d+j))
        
    #     self.assertEqual(0, self.context1.occupancy(0,0))
    #     self.assertEqual(0, self.context1.occupancy(4,7))

    def test_offset(self):
        xs, ys = cues_array_to_cartesian(self.context1.context_cues)
        xos, yos = cues_array_to_cartesian(self.off_context1.context_cues)
        
        
        for x, y, xo, yo in zip(xs, ys, xos, yos):
            self.assertAlmostEqual(self.x_offset, xo - x)
            self.assertAlmostEqual(self.y_offset, yo - y)
    
if __name__ == '__main__':
    unittest.main()
