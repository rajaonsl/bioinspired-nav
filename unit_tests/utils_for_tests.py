import numpy as np


#------------------------------------------------------------------------------
def make_constant_acquisitions(dist, fov=360):
    """
    make acquisitions where all points are same distance
    """
    result = np.full(fov, dist)
    return result


#------------------------------------------------------------------------------
## UTILITY LOG READER
PATH = '/home/ubuntu/share/ranges.txt'
class RangeReader:

    def __init__(self, path: str = PATH):
        self.ranges = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                ranges = []
                while i < len(lines) and lines[i] != '\n':
                    ranges += [float(x) for x in lines[i].split()]
                    i += 1
                self.ranges.append(ranges)
                i += 1
        self.index = 0

    def get_next(self) -> list:
        if self.index >= len(self.ranges):
            self.index = 0
        ranges = self.ranges[self.index]
        self.index += 1
        return ranges