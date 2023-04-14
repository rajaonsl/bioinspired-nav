import cProfile
import math
import pstats
import numpy as np

# from sensory_system.context_cue import ContextCue
from sensory_system.range_sensor import RangeSensor
from space_memory.place_cell import PlaceCell
from space_memory.grid_cluster import GridCluster 
from sensory_system.original_context import OriginalContext, create_cue, get_d, get_theta, get_cue_type
from utils.misc import polar_to_cartesian

class SpaceMemory:
    """
    This class represents the whole space memory of an agent. It contains a list of place cells,
    that it uses to estimate position. The space memory is updated and expanded based on new sensor data.
    """

    #-------------------------------------------------------------------
    # @TODO: reconsider sensor_data as an argument for construction
    def __init__(self, sensor_data: np.ndarray, sensor_data_processor: RangeSensor,
                 scale: int=3): 
        # with cProfile.Profile() as profile:
            
            # Save sensor info
            #@TODO use this more (especially FOV!)
            self.sensor_data_processor: RangeSensor = sensor_data_processor

            # Initialize the first place cell
            self.place_cells_list: list[PlaceCell] = []
            place_cell_context = sensor_data_processor.process_acquisition(sensor_data) #@TODO, fov_180=False)
            self.place_cells_list.append(PlaceCell(place_cell_context)) #@TODO: specify context interface
            self.current_place_cell = self.place_cells_list[0]

            # Initialize the module (only one, reused when active cell changes)
            self.grid: GridCluster = GridCluster(scale=scale)
            self.grid.set_place_cell(self.current_place_cell)

            # Initialize various parameters
            #   - defines required activity for a place cell to become active
            self.place_cell_activity_floor = 15
            #   - defines the "tolerance" of context comparison for place/grid cells
            self.grid_cell_spread_size = 4
            self.place_cell_spread_size = 16

        # results = pstats.Stats(profile)
        # results.sort_stats(pstats.SortKey.TIME)
        # results.print_stats()
        # results.dump_stats("/home/ubuntu/share/init_profile.prof")
        # results.dump_stats("init_profile.prof")

    #-------------------------------------------------------------------
    def update(self, raw_sensor_data: np.ndarray):
        with cProfile.Profile() as profile:
            # 0.
            # Process raw sensor data as cues
            # @TODO: add landmarks and color system
            sensor_cues = self.sensor_data_processor.acquisition_to_cues_array(raw_sensor_data) #@TODO, fov_180=False)

            # 1.
            # Compute activities
            for place_cell in self.place_cells_list:
                place_cell.compute(sensor_cues)
            self.grid.compute(sensor_cues)

            # 2.
            # Extract estimated pose
            # scale = self.grid.scale
            # estimated_x = self.grid.estimated_relative_x * scale
            # estimated_y = self.grid.estimated_relative_y * scale
            # estimated_theta = self.grid.angle_estimation

            # 3.
            # Update place cell context with potentially new information
            # @TODO/NOTE: was -x, -y and 180-theta in original impl ?
            # NOTE: currently bugged (angle goes negative?), and DEEMED NOT
            # NECESSARY BECAUSE OF 360 VISION
            # self.__update_context(sensor_cues, estimated_x, estimated_y, estimated_theta)

            # 4.
            # Change active place cell or creates a new one as needed.
            self.__update_active_cell(sensor_cues)

        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.TIME)
        results.print_stats()
        results.dump_stats("/home/ubuntu/share/update_profile.prof")
        results.dump_stats("update_profile.prof")


    #-------------------------------------------------------------------
    # @TODO: reconsider type of sensor_data 
    # WARNING: CURRENTLY DOESN'T WORK !!!! assumed to be array of ctx clues, but called with raw sensor data ! )
    # @TODO-2: most of this code should really be in PlaceCell and Context instead of here
    # @TODO-3: numpy-ify
    def __update_context(self, sensor_data: np.ndarray, relative_x: float, relative_y: float, theta: float):
        """
        updates the context of the current place cell
        """
        # NOTE/WARNING:
        # The following portion of code is ported "as is" from the original implementation
        # in order to get the *exact* same behavior. However, the way that this method works
        # is questionnable style-wise, perfomance-wise AND on a higher conceptual level. 
        # @TODO: Reconsider implementation
        relative_x *= -1 # sure about double minus??? huh
        relative_y *= -1
        theta *= -1
        print("translating x", relative_x, "y", relative_y, "rotating", theta)

        #theta = math.radians(180 - theta) # @TODO: this looks to be FOV dependant, update
        theta = math.radians(theta)#math.radians(180 - theta)

        centered_sensor_data: np.ndarray = np.zeros((len(sensor_data),4)) #@TODO BAD DESIGN PATTERN don't hardcode cue array type here
        for i,point in enumerate(sensor_data): # Point is represented as cues in original context (numeric ndarray)
            # @TODO rotation using matrix multiplication by hand, use numpy instead
            point_x, point_y = polar_to_cartesian(d=get_d(point),theta=get_theta(point))

            x = (point_x*math.cos(theta) - point_y*math.sin(theta)) - relative_x
            y = (point_x*math.sin(theta) + point_y*math.cos(theta)) - relative_y
            d = math.sqrt(x*x + y*y)
            t = math.degrees(math.atan2(y, x))

            print("x", x, "y", y, " -> theta", t%360)
            centered_sensor_data[i] = create_cue(distance=d, theta=t, cue_type=get_cue_type(point))
        
        print(sensor_data)
        print("================")
        print(centered_sensor_data)

        self.current_place_cell.context.update(centered_sensor_data)
        self.grid.set_place_cell(self.current_place_cell) # update context of all grid cells in module


    #-------------------------------------------------------------------
    # @TODO: reconsider input type
    # @TODO/WARNING: Doesn't work right now, is fed raw sensor data but expects an array of context cues! (see below)
    def __update_active_cell(self, sensor_data: np.ndarray):
        """
        decides when the active place cell should change, and makes the necessary changes.
        """
        estimated_x, estimated_y = self.grid.estimated_relative_x, self.grid.estimated_relative_y
        estimated_theta = self.grid.angle_estimation

        # If there is a neighbor closer than the current cell, switch to it
        neighbor = self.current_place_cell.checkNeighbors(estimated_x, estimated_y) #@TODO implement
        if neighbor is not None:
            self.current_place_cell = neighbor
            self.grid.set_place_cell(self.current_place_cell)

        # If no good neighbor and at the edge of the current module
        elif self.grid.test_module_border(margin=0.5):

            #First, check for a (different) active place cell
            max_activity = 0. # activity of the most active place cell
            best_cell: PlaceCell = None
            for place_cell in self.place_cells_list:
                if place_cell.id == self.current_place_cell.id:
                    continue
                elif place_cell.activity > max_activity and place_cell.activity > self.place_cell_activity_floor:
                    max_activity = place_cell.activity
                    best_cell = place_cell

            # If there is an active existing place cell, switch to it, and connect neighbors
            if best_cell is not None:
                self.current_place_cell.addNeighbor(best_cell)
                self.current_place_cell = best_cell
                self.grid.set_place_cell(best_cell)
                self.grid.compute(sensor_data)

            # Finally, if all else fails, make a new place cell
            else:
                current_x = self.current_place_cell.global_x + estimated_x 
                current_y = self.current_place_cell.global_y + estimated_y
                current_context = OriginalContext(sensor_data).rotate(-1*estimated_theta) # Reset angle @TODO slight inefficiency (should rotate sensor_data instead)
                new_cell = PlaceCell(current_context, global_x=current_x, global_y=current_y) # @TODO/WARNING DOESNT WORK !!!!!!! IMPLEMENT CREATION OF CONTEXT FROM RAW SENSOR DATA !!!!

                self.current_place_cell.addNeighbor(new_cell)
                self.place_cells_list.append(new_cell)

                self.grid.set_place_cell(new_cell)
                self.current_place_cell = new_cell
        else:
            pass
    
    # @TODO: add shortcut detection, but probably not here!
