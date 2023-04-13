"""
Main module

This will later be replaced by a ROS node that receives sensor data
from a (probably simulated) robot.
"""
import time
import numpy as np

from space_memory.space_memory_manager import SpaceMemory
from visualization.space_memory_visualizer import SpaceMemoryVisualizer


def main():

    full_logs = np.array([
        [1., 1., 1.1, 1.2, 1.3, 1.3, 1.3, 1.2, 1., 0, 0, 0],
        [1., 1., 1.1, 1.2, 1.3, 1.3, 1.3, 1.2, 1., 0, 0, 0],
        [1., 1., 1.1, 1.2, 1.3, 1.3, 1.3, 1.2, 1., 0, 0, 0],
        [1., 1., 1.1, 1.2, 1.3, 1.3, 1.3, 1.2, 1., 0, 0, 0],
        [1., 1., 1.1, 1.2, 1.3, 1.3, 1.3, 1.2, 1., 0, 0, 0]])

    n_ranges = len(full_logs[0])
    min_range, max_range = 0, 5

    memory = SpaceMemory(n_ranges, max_range, min_range) #@TODO other option: add initial measurement

    visualiser = SpaceMemoryVisualizer() #@TODO what does it do ? how does it get real position for comparison ?

    # @TODO: this loop will be replaced by ROS callbacks
    for sensor_data in full_logs:
        memory.update(sensor_data)
        visualiser.update()
        time.sleep(1.)


    # """
    # Main function
    # """

    # my_cell = GridCell()
    # # my_cell.set_context()

    # visual = GridCellVisualizer(my_cell)

    # @TODO get good (lmao)

    # #each point is in the form: [distance, theta, type of obstacle]
    # context = [[

    # ]]



    # my_cell.set_context([1, 2, 2, 2, 1], x_offset=0, y_offset=0)

    # my_cell.compute_activity([1])

    # time.sleep(2.4)

if __name__ == "__main__":
    main()
