# Python imports
import math
import tkinter as tk

# Project imports
from space_memory.grid_cell import GridCell

class GridCellVisualizer:
    """
    Displays the activity of a grid cell for each orientation
    """
    def __init__(self, cell: GridCell):

        # Initialize window and canvas
        self.width = 600
        self.height = self.width
        self.radius = 250 
        self.window = tk.Tk()
        self.window.title("Grid cell activation (by orientation)")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="white")
        self.canvas.grid(row=1,column=1)
        
        self.orientations =[]
        
        self.cell = cell
        self.init_cell(len(self.cell.activity))

        self.window.update()

    def init_cell(self, context_length: int):
        angle = 0
        angle_step = 2*math.pi/context_length #@TODO ??
        center_x, center_y = self.width/2, self.height/2
        for _ in range(0, context_length):
            orientation_x = center_x - self.radius*math.sin(angle)
            orientation_y = center_y - self.radius*math.cos(angle)
            self.orientations.append(self._plot_orientation(orientation_x, orientation_y))
            angle+=angle_step

    def update_activity(self):
        for i, orientation in enumerate(self.orientations):
            self.canvas.itemconfig(orientation, fill=self._getcolor(self.cell.activity[i]))
        self.window.update()

    def _plot_orientation(self, x: int, y: int, radius: int = 8):
        return self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius , outline="")

    def _getcolor(self, activity: float) -> str:
        #green = int(activity * 255) # assumes activity between 0. and 1.
        red = int(activity * 360) # Flashier for poster
        red = min(255, red)
        green = int(red * 0.4)
        blue = 255 - red
        return f"#{red:02x}{green:02x}{blue:02x}"
