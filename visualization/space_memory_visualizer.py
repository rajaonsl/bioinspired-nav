import tkinter as tk

from space_memory.space_memory_manager import SpaceMemory
from space_memory.place_cell import PlaceCell

class SpaceMemoryVisualizer:
    """
    Displays the graph of place cells
    """
    def __init__(self, space_memory: SpaceMemory) -> None:
        self.width = 700
        self.height = self.width
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="white")
        self.canvas.grid(row=1, column=1)

        self.scaling = 8 # pixels per distance unit

        self.space_memory = space_memory

    def update(self):
        """
        inefficient. @TODO rewrite better
        """
        self.canvas.delete('all')

        place_cell: PlaceCell
        for place_cell in self.space_memory.place_cells_list:

            print(len(self.space_memory.place_cells_list))
            print("pc activity: ", place_cell.activity)
            print("pc global coords", place_cell.global_x, place_cell.global_y)
            
            place_x, place_y = place_cell.global_x, place_cell.global_y
            plot_x, plot_y = place_x*self.scaling, place_y*self.scaling
            place_activity = place_cell.activity
            color = self._get_color(place_activity)

            self._plot_cell(plot_x, plot_y, color, is_active=(place_cell == self.space_memory.current_place_cell))
            # @TODO draw connections


    def _get_color(self, activity):
        """
        derive a color to display from an activity value
        """
        red = int(activity * 3)
        red = min(255, red)
        green = int(red * 0.4)
        blue = 255 - red
        return f"#{red:02x}{green:02x}{blue:02x}"

    def _plot_cell(self, x, y, color, is_active: bool=False, radius=7):
        center_x, center_y = self.width/2, self.height/2
        outline='red4' if not is_active else 'gold'

        self.canvas.create_oval(x - radius + center_x,
                                y - radius + center_y,
                                x + radius + center_x,
                                y + radius + center_y, fill=color, outline=outline, width=radius/3)
