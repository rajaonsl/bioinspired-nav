# What is this?

This repository contains a bio-inspired navigation model for a range detector. A ROS2 node implementation is provided as an example, for the TurtleBot3

It is inspired by *'A B-spline Mapping Framework for Long-Term Autonomous Operations'* by Rômulo T. Rodrigues. This paper presents an approach to online SLAM
where obstacles in the map are represented with B-splines.

# How do I run things?

The code is divided into several folders, that give one functionnality and a gui program showing it off. For example, in the folder 'bezier_collision', you have:
- 'bezier_curve.py' that defines functions you can use to compute bezier curves and detect intersections between them.
- 'bezier_gui.py', **which you can run**. It uses those functions to plot bezier curves, and changes their color depending on wether they intersect or not.

Other folders follow a similar structure, with a graphical program you can run, and a file defining functions you can reuse.

For imports to work correctly, you *may* need to install the repository as a package using pip install.

# Quick walkthrough

- bezier_collision:
    - compute bezier curves
    - compute bounding boxes for bezier curves
    - split bezier curves in halves
    - detect intersection of two bezier curves

- bspline_fitting_barycenter:
    - compute bspline curves
    - compute a lower degree curve from a set of many points ('global fitting')

- segmentation:
    - segment an acquisition into several clusters

- tracking_pose_estimation:
    - compute pose estimation from two sets of measurements

- utility:
    - Various bits, mostly to handle sensor data.

*Plus the usual boilerplate of Python packages(pycache, setup.py...). Other Python scripts in the root directory are temporary and have yet to be organized.*