import tkinter as tk

from space_memory.grid_cell import GridCell
from space_memory.grid_cluster import GridCluster

from visualization.grid_cell_visualizer import GridCellVisualizer

class GridClusterVisualizer:
    """
    Displays the maximum activity of a grid cluster
    """
    def __init__(self, cluster: GridCluster):

        # Initialize window and canvas
        self.cell_size = 50
        self.width = 11*self.cell_size
        self.height = 11*self.cell_size
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="white")
        self.canvas.grid(row=1, column=1)
        
        self.activities = []

        self.cluster = cluster
        self.init_cluster()

        self.window.update()

    def init_cluster(self):
        for i in range(11):
            l = []
            for j in range(11):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = (i + 1) * self.cell_size
                y1 = (j + 1) * self.cell_size
                max_activity = self.cluster.activity[i][j]
                color = self._getcolor(max_activity)
                rectangle_id = self._plot_activity(x0,y0,x1,y1,color)
                l.append(rectangle_id)

                # Bind mouse click to cell display
                # NOTE: Putting arguments with default values in the lambda
                # function to capture loop index looks hacky, but it is
                # the recommended solution in the official Python FAQ:
                # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
                self.canvas.tag_bind(rectangle_id, "<Button-1>",
                                     lambda _, i=i, j=j: _open_cell_window(self.cluster.grid[i][j])
                                     )
            self.activities.append(l)


    def update_activity(self):
        for i in range(11):
            for j in range(11):
                max_activity = self.cluster.activity[i][j]
                color = self._getcolor(max_activity)
                self.canvas.itemconfig(self.activities[i][j], fill=color)
        self.window.update()

    def _plot_activity(self, x0, y0, x1, y1, color):
        # return self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        return self.canvas.create_rectangle(y0, x0, y1, x1, fill=color, outline="")
    
    def _getcolor(self, activity: float) -> str:
        #green = int(activity * 255) # assumes activity between 0. and 1.
        red = int(activity * 360) # Flashier for poster
        red = min(255, red)
        green = int(red * 0.4)
        blue = 255 - red
        return f"#{red:02x}{green:02x}{blue:02x}"
    
def _open_cell_window(cell: GridCell):
    """
    Method used to visualize a cell when clicking on it
    """
    cell_visualizer = GridCellVisualizer(cell)
    cell_visualizer.update_activity()