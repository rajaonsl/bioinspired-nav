import numpy as np

from space_memory.grid_cell import GridCell
from space_memory.place_cell import PlaceCell

class GridCluster:
    """
    """

    #-------------------------------------------------------------------
    def __init__(self, scale: int = 3):
        
        self.scale = scale # Scale of the grid
        self.angle_estimation: float = None # Estimated orientation
        self.estimated_relative_x: float = None # Estimated x (relative to center)
        self.estimated_relative_y: float = None # Estimated y (relative to center)
        self.center_x, self.center_y = None, None

        self.activity = np.zeros((11,11)) # Only for visualizaton purposes

        # @TODO: make grid flexible
        self.grid = np.empty((11, 11), dtype=object)
        for i in range(11):
            for j in range(11):
                self.grid[i][j] = GridCell()

        # @TODO: move this elsewhere, and actually compute them.
        self.gauss=np.zeros(9)
        self.gauss[0]=0.018
        self.gauss[1]=0.1
        self.gauss[2]=0.37
        self.gauss[3]=0.78
        self.gauss[4]=1.
        self.gauss[5]=0.78
        self.gauss[6]=0.37
        self.gauss[7]=0.1
        self.gauss[8]=0.018


    #-------------------------------------------------------------------
    def set_place_cell(self, place_cell: PlaceCell):
        """
        Set the place cell. Uses the new place cell's context
        to compute the offset contexts of the grid cells
        """

        # OLD weird code
        # # # For each grid cell of the module, apply context offset.
        # for i, row in enumerate(self.grid):
        #     _ : GridCell
        #     for j, _ in enumerate(row):  #@TODO: make prettier and use _
        #         # the grid is toroidal, with its center being the place cell's center
        #         cx, cy = place_cell.center_x + i, place_cell.center_y + j
        #         cx, cy = apply_bounds(cx, 11), apply_bounds(cy, 11)
        #         self.grid[cx][cy].set_context(
        #             place_cell.context.offset(i * self.scale, j*self.scale)
        #         )

        # NEW version:

        self.center_x, self.center_y = place_cell.center_x, place_cell.center_y

        for i, row in enumerate(self.grid):
            _ : GridCell
            for j, _ in enumerate(row):
                x_from_center = (i - place_cell.center_x) * self.scale
                y_from_center = (j - place_cell.center_y) * self.scale
                self.grid[i][j].set_context(
                    place_cell.context.offset(x_from_center, y_from_center)
                )


    #-------------------------------------------------------------------
    def compute(self, observation: np.ndarray):
        """
        Compute the activity of all grid cells in the module.
        expects a numpy array of context cues (ContextCue)
        result is stored in self
        """

        # 1. Compute grid cells and fill orientation map
        orientation = np.zeros(360) # @TODO: interchangable angle/index; @TODO make a public attribute ?
        for i,row in enumerate(self.grid):
            cell: GridCell
            for j,cell in enumerate(row):
                #cell.compute(observation)
                cell.compute(observation)
                #@TODO make flexible
                for k in range(-8, 9):
                    d = (cell.max_activity_angle + k) % 360
                    orientation[d]+=(cell.max_activity**2)*self.gauss[(k//2) + 4]

        # 2. Get best matching orientation
        # @TODO: there's probably a std function for this
        max_angle: int = np.argmax(orientation)

        # 3. Compute exact estimated orientation (not bound by grid)
        # Take the average of angles max_angle+-2, weighted by orientation
        # @TODO make flexible
        angle_estimation = 0.
        sum_ = 0.
        for angle in range(-2, 3):
            a2 = (max_angle + angle)%360
            angle_estimation += (max_angle + angle) * orientation[a2]
            sum_+= orientation[a2]

        if sum_ > 0:
            self.angle_estimation = (angle_estimation/sum_) % 360

        # 3.5: Get all cell activities for the estimated angle
        angle_as_index = (round(self.angle_estimation)) % 360
        # @TODO make flexible
        # also, why the square ?
        activity = np.zeros((11,11))
        for i in range(11):
            for j in range(11):
                activity[i][j] = self.grid[i][j].activity[angle_as_index]**2
        
        self.activity = activity#TMP

        # 4. Get best matching cell
        # pylint: disable-next=unbalanced-tuple-unpacking
        cell_x, cell_y = np.unravel_index(activity.argmax(), activity.shape) #cell_x, cell_y are indexes

        # 5. Compute exact estimated position
        # Take the average of position+-1 weighted by corresponding cell activity
        # @TODO make flexible
        # @TODO use better names
        estimated_x, estimated_y, sum_ = 0., 0., 0.
        for i in range(-1, 2):
            for j in range(-1, 2):
                dx = (cell_x + i) % 11
                dy = (cell_y + j) % 11

                estimated_x += (cell_x + i) * activity[dx][dy]
                estimated_y += (cell_y + j) * activity[dx][dy]
                sum_ += activity[dx][dy]

        print("estimated_x", estimated_x)
        print("estimated_y", estimated_y)
        if sum_ > 0:
            self.estimated_relative_x = estimated_x/sum_ - self.center_x
            self.estimated_relative_y = estimated_y/sum_ - self.center_y
        else:
            print("warning: grid failed to estimate position:")
            print(activity)


    #-------------------------------------------------------------------
    # @TODO remove but keep explanation
    def _get_coords_of_cellself(self, cell_i, cell_j, center_x = 5., center_y = 5.):
        """
        Internal method, returns the coordinates represented by
        the cell at index i,j.

        If the center is at 5., 5., then the cell at [0][0] represents
        the agent position x=-5*scale, y=-5*scale. NOTE that this does
        not align with intuition when drawing (you would expect the top
        left corner in negative x and positive y, not negative x and negative y!)
        """
        x = cell_i - center_x
        y = cell_j - center_y
        return (x*self.scale, y*self.scale)


    #-------------------------------------------------------------------
    def test_module_border(self, margin: float = 0.5):
        """
        tests if the estimated position is close to the border.
        (true if close to border)
        """
        return (
            abs(self.estimated_relative_x) > (11//2 - margin) or
            abs(self.estimated_relative_y) > (11//2 - margin)
        )