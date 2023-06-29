"""
Displays a 2D matrix as a grayscale image on a canvas.

ASSUMES VALUES BETWEEN 0 AND 1
"""

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class MatrixVisualizer:
    def __init__(self, matrix: np.ndarray, title="Matrix Visualizer"):

        self.matrix = matrix

        # Create a blank image with the same size as the matrix
        self.image = Image.new("L", matrix.T.shape)

        # Create a Tkinter window and canvas
        self.window = tk.Tk()
        self.window.title(title)
        self.canvas = tk.Canvas(self.window, width=self.image.width, height=self.image.height)
        self.canvas.pack()

        # Convert the image to a Tkinter-compatible format
        self.tk_image = ImageTk.PhotoImage(master=self.canvas, image=self.image)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def update(self, new_matrix=None):

        if new_matrix is not None and new_matrix is not self.matrix:
            self.matrix=new_matrix

        # Scale the matrix to integers 0 - 255
        scaled = (self.matrix * 255).astype(np.uint8)

        # IMPORTANT NOTE: using Image.fromarray is at least 60x faster than
        # addressing each pixel individually. When modifying this file, the
        # programmer should try to use vectorized operations and create the
        # image directly from an array, as much as possible.
        self.image = Image.fromarray(scaled, "L")
        self.tk_image.paste(self.image)
        self.canvas.itemconfig(self.image_item, image=self.tk_image)

        self.window.update()
