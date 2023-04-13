import unittest

from sensory_system.context_cue import ContextCue, ContextCueType

class TestContextCue(unittest.TestCase):
    def setUp(self):
        self.cue1 = ContextCue(50, 30, ContextCueType.OBSTACLE)
        self.cue2 = ContextCue(50, 60, ContextCueType.CORNER)
        self.cue3 = ContextCue(100, 120, ContextCueType.LANDMARK)

    def test_init(self):
        self.assertEqual(self.cue1.d, 50)
        self.assertEqual(self.cue1.theta, 30)
        self.assertEqual(self.cue1.cue_type, ContextCueType.OBSTACLE)
        # self.assertAlmostEqual(self.cue1.d_2, 45.2516, places=3)

    # @TODO: implement tests
    # def test_compare(self):
    #     similarity1 = self.cue1.compare(self.cue2)
    #     similarity2 = self.cue1.compare(self.cue3)
    #     self.assertLess(similarity1, 1)
    #     self.assertGreater(similarity1, 0)
    #     self.assertAlmostEqual(similarity2, 0, places=3)

    def test_offset(self):
        offset_cue1 = self.cue1.offset(10, 20)
        offset_cue2 = self.cue2.offset(-5, 5)
        x1, y1 = self.cue1.get_cartesian()
        x2, y2 = self.cue2.get_cartesian()
        xo1, yo1 = offset_cue1.get_cartesian()
        xo2, yo2 = offset_cue2.get_cartesian()

        self.assertAlmostEqual(x1 + 10, xo1, places=3)
        self.assertAlmostEqual(y1 + 20, yo1, places=3)
        self.assertAlmostEqual(x2 - 5, xo2, places=3)
        self.assertAlmostEqual(y2 + 5, yo2, places=3)

if __name__ == '__main__':
    unittest.main()