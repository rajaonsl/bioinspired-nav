"""
This is unit testing of some sort
"""
# %%
import math
import os
import numpy as np
from sensory_system.context_cue import ContextCue
#from sensory_system.original_context import OriginalContext
from sensory_system.turtlebot3_range_sensor import TurtlebotRangeSensor
from space_memory.grid_cell import GridCell
from space_memory.grid_cluster import GridCluster
from space_memory.place_cell import PlaceCell
from unit_tests.utils_for_tests import RangeReader
from utils.misc import polar_to_cartesian
from visualization.grid_cell_visualizer import GridCellVisualizer
from visualization.grid_cluster_visualizer import GridClusterVisualizer

from spline_slam_ros2.sensor_plotter_optimized import FastSensorPlotter
# from utils.misc import polar_to_cartesian


#------------------------------------------------------------------------------
def make_constant_acquisitions(dist, fov=360):
    """
    make acquisitions where all points are same distance
    """
    result = np.full(fov, dist)
    return result

#------------------------------------------------------------------------------
def get_test_ranges_path():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(test_dir)
    data_path = os.path.join(parent_dir, 'unit_tests', 'test_ranges.txt')
    return data_path

#------------------------------------------------------------------------------
# def rotate_acquisitions(ranges, theta):
#     result = np.empty(len(ranges))
#     for a, d in enumerate(ranges):
#         point_x, point_y = polar_to_cartesian(d, a)

#         x = (point_x*math.cos(theta) - point_y*math.sin(theta)) #- relative_x
#         y = (point_x*math.sin(theta) + point_y*math.cos(theta)) #- relative_y

#         d = math.sqrt(x*x + y*y)
#         t = math.degrees(math.atan2(y,x))


#------------------------------------------------------------------------------
def print_matrix_sum(matrix: np.ndarray):
    print("sum = ", matrix.sum())


#------------------------------------------------------------------------------
def print_matrix_layer0(matrix: np.ndarray):
    for row in matrix:
        s = "["
        for col in row:
            s += str(col[0])
        print(s + "]")

# %%
#------------------------------------------------------------------------------
## MAIN FUNCTION
def main():
    # %%
    print(" Starting test program.")


    data_processor = TurtlebotRangeSensor(max_range=10000, field_of_view=180)

    test_ctx_1 = data_processor.process_acquisition(make_constant_acquisitions(20.))
    print(len(test_ctx_1.context_cues))

    # %%
    #-------------------------------------------------------------------
    print("= = = = = = = GRID CELL = = = = = = = ")

    cell = GridCell()
    cell.set_context(test_ctx_1)
    print_matrix_sum(cell.context.context_matrix)
    # EQUIVALENT:
    # print_matrix_sum(test_ctx_1.context_matrix)
    
    range_reader = RangeReader(get_test_ranges_path())
    adjusted_ranges_1 = np.array(range_reader.get_next()) * 50
    adjusted_ranges_2 = np.array(range_reader.get_next()) * 50
    test_ctx_2 = data_processor.process_acquisition(adjusted_ranges_1)
    test_ctx_3 = data_processor.process_acquisition(adjusted_ranges_2 )
    viz = GridCellVisualizer(cell)
    range_viz = FastSensorPlotter()

    cell.set_context(test_ctx_2)
    
    cell.compute(test_ctx_2.context_cues)
    print(" For same context, estimated angle=", cell.max_activity_angle)
    viz.update_activity()
    range_viz.draw_rays(adjusted_ranges_1, maxrange=3.5 * 50)
    input()

    cell.compute(test_ctx_3.context_cues)
    print(" For rotated context, estimated angle=", cell.max_activity_angle)
    viz.update_activity()
    range_viz.draw_rays(adjusted_ranges_2, maxrange=3.5 * 50)
    input()

    # NOTE: While the relative rotation seems to match quite well, and the
    # activity values don't seem totally insane, it is weird that the
    # best angle for the default context is 155

    # %%
    #-------------------------------------------------------------------
    print("= = = = = = = ORIGINAL CONTEXT = = = = = = = ")
    # %%
    offset_ctx_2 = test_ctx_2.offset(5., 4.)
    for i, offset_cue in enumerate(offset_ctx_2.context_cues):
        original_cue: ContextCue = test_ctx_2.context_cues[i]

        original_x, original_y = polar_to_cartesian(original_cue.d, original_cue.theta)
        offset_x, offset_y = polar_to_cartesian(offset_cue.d, offset_cue.theta)

        print("x: ", original_x, " -> ", offset_x)
        print("y: ", original_y, " -> ", offset_y)
    # input()


    # %%
    #-------------------------------------------------------------------
    print("= = = = = = = GRID CLUSTER = = = = = = = ")
    place_cell = PlaceCell(test_ctx_2)
    cluster = GridCluster()
    cluster.set_place_cell(place_cell)

    # %%
    viz_2 = GridClusterVisualizer(cluster)
    cluster.compute(test_ctx_2.context_cues)

    # %%
    print(" for same context, estimations are x:",
          cluster.estimated_relative_x,
          "y:", cluster.estimated_relative_y,
          "angle:", cluster.angle_estimation)
    viz_2.update_activity()
    input()
    

    cluster.compute(test_ctx_3.context_cues)
    print(" for rotated context, estimations are x:",
          cluster.estimated_relative_x,
          "y:", cluster.estimated_relative_y,
          "angle:", cluster.angle_estimation)
    viz_2.update_activity()
    input()
    # %%
    print("= = = = = = = PLACE CELL = = = = = = = ")

    # %%
    print("= = = = = = = SPACE MEMORY = = = = = = = ")

    # %%

if __name__ == "__main__":
    main()
