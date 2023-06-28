# Bio-inspired navigation model

This repository contains a bio-inspired navigation model for a system navigating in an unknown environment using a range detector. A ROS2 node implementation is provided as an example for the TurtleBot3 burger, which embarks a 360° LiDAR sensor.

*Author: L. Rajaonson    |    Supervisors: S. Gay, I. Prodan    |    Internship at LCIS (Valence, FR). 2023*
# How do I run it

## Prerequisites

To run the example ROS2 node, you need at least a computer running a compatible version of ROS2 (preferably Humble or Foxy). You can either simulate a TurtleBot (for example with Gazebo) or use a physical robot. 

## Build it

Clone the repository into the sources of your ROS workspace (your_ws/src/bioinspired-nav). Then, simply build the package using colcon:

    colcon build --select-packages bioinspired-nav --symlink-install

## Run it

Assuming you have installed the necessary ROS2 packages to run a TurtleBot simulation, here's an example of use:

In one terminal, run your simulator (here, Gazebo):

    ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py

-IMAGE

In another terminal, run a means to control your robot (here, we will use the basic keyboard control node):

    ros2 run turtlebot3_teleop teleop_keyboard

Finally, in a third terminal, run the bio-inspired node:

    <insert command here>

## What is happening?

The navigation model starts as soon as the node is ran, opening several visualisation windows that give an insight on what the model is doing. For more details on the model itself, see the quick walkthrough, or the referenced papers.

# Quick walkthrough

The project is subdivided into several folders:

- **sensory_system** is used to define classes that process raw sensor data into objects usable by the system:
    - *Context* is an abstract interface. Its implementation defines how the model represents observations and how
    it matches new observations with existing ones.
    - *RangeSensor* is an abstract interface. Its implementation defines how the model constructs Contexts from raw sensor data. It is tasked with filtering incorrect measurements.

- **space_memory** is used to define the bioinspired model itself. All the cells modeled are inspired from real cells discorvered in mammalian brains. In this particular model, the role of the cells are as follows:
    - *GridCell* activate when an observation matches their saved contexts. They also double as head direction cells, providing an estimate of the agent's rotation that best matches the savec context.
    - *GridCluster* represents a module (grid) of grid cells. Its activation provides a local position estimate relative to the active PlaceCell.
    - *PlaceCell* are organized as nodes. Together, they form a navigation graph that encodes a topological representation of the environment. They are responsible for recognizing already explored places.
    - *SpaceMemory* is the main class of the model. It glues together all the elements. It is responsible for the construction of the place cells graph (deciding the creation of new place cells, switching the active place cell, connecting nodes in the graph), as well as managing interactions between the place cells and the grid cluster. It requires an instance of a *RangeSensor*, which it uses to compute contexts and feed them to the cells.

- **unit_tests** contain some simple tests for the model's component.

- **visualization** contains several classes that can visualize individual components of the model as it runs. Each creates its own window upon construction, and provides a method to update the visualization.
    - *GridCellVisualizer* visualizes a single GridCell's activity. The activity is broken down into its 360 orientations, arranged in a circle.
    - *GridClusterVisualizer* visualizes a whole GridCluster. It shows the activity of each cell in the grid. Clicking a cell in the grid opens an individual visualizer for it.
    - *MatrixVisualizer* visualizes a 2D matrix as a grayscale image. Its main purpose is to visualize the context matrices constructed in the original context implementation.
    - *SpaceMemoryVisualizer* visualizes the graph of place cells and their activity. As an option, it can also open a matrix visualizer for the active place cell.

# References

TODO