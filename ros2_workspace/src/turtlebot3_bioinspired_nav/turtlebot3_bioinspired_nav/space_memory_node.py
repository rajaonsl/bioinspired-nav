#!/usr/bin/env python3

# ROS libraries
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from sensor_msgs.msg import LaserScan

# Bio-Inspired model imports
from sensory_system.turtlebot3_range_sensor import TurtlebotRangeSensor
from space_memory.space_memory_manager import SpaceMemory
from visualization.grid_cluster_visualizer import GridClusterVisualizer
from visualization.space_memory_visualizer import SpaceMemoryVisualizer

# Profiling imports
# import cProfile
# import pstats


class SpaceMemoryNode(Node):

    def __init__(self):
        super().__init__("space_memory_node")

        self.get_logger().info("BioInspired node has been started")

        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        self.scan_subscriber_ = self.create_subscription(
            msg_type=LaserScan, topic="/scan", callback=self.scan_callback, qos_profile=qos_profile)

        # Initialize space memory
        self.sensor_processor = None
        self.space_memory = None
        self.viz_gc = None
        self.viz_spacemem = None

    def scan_callback(self, msg: LaserScan):

        # Print a bunch of stuff
        # self.get_logger().info("number of range measurements: " + str(len(msg.ranges)))
        # self.get_logger().info("range bounds: min = " + str(msg.range_min) + ", max = " + str(msg.range_max))
        # self.get_logger().info("angle bounds: min = " + str(msg.angle_min) + ", max = " + str(msg.angle_max))

        # Scale things up #@TODO fix
        # range_max = 3.5*50# REAL TURTLEBOT HAS STUPID RANGE MAX LOL msg.range_max * 50
        # ranges = np.array(msg.ranges) * 50

        
        range_max = 3.5 # Set manually because physical turtlebot can't be trusted lol
        ranges = np.array(msg.ranges)

        # Initialize sensor data processor and space memory
        if self.sensor_processor is None:
            self.get_logger().info("initializing sensor data processor")
            self.sensor_processor = TurtlebotRangeSensor(
                max_range=range_max,
                min_range=msg.range_min,
                fov_180=False)

        if self.space_memory is None:
            self.get_logger().info("initializing space memory and visuals")
            self.space_memory = SpaceMemory(ranges, self.sensor_processor, scale=6)
            self.viz_gc = GridClusterVisualizer(self.space_memory.grid)
            self.viz_spacemem = SpaceMemoryVisualizer(self.space_memory)
            # self.space_memory.debug()
            # self.get_logger().info(self.space_memory.grid)

        # Update spatial memory
        else:
            self.get_logger().info("Computing update...")
            self.space_memory.update(ranges)
            self.viz_gc.update_activity()
            self.viz_spacemem.update()

        # @TODO: visualize result


def main(args=None):
    rclpy.init(args=args)
    node = SpaceMemoryNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
