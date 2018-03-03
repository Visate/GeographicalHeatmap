"""
Geographical heatmap module
written by Richard Gan
"""
from typing import List, Dict, Any, Callable, Union
from collections import Counter as IterCounter
from math import sqrt, ceil
import numpy as np
from matplotlib.colors import Colormap
from colourmaps import get_unified_colourmap, COLOURS
from utilities import Counter, load_from_csv, verify_dataset

DEFAULT_NAME_COL = 0
DEFAULT_LAT_COL = 1
DEFAULT_LON_COL = 2
DEFAULT_VALUE_COL = 3
DEFAULT_SCALE = 0.007
DEFAULT_RADIUS = 0.2
FIGSIZE = (16, 10)
MODES = ["influence", "weighted"]
LEGEND_LOCATIONS = ["best", "upper right", "upper left", "lower left", 
                    "lower right", "right", "center left", "center right", 
                    "lower center", "upper center", "center"]

class Heatmap:
    """
    Defines a heatmap

    grid - grid of the heatmap
    _verboseprint - function for debugging purposes
    _filepath - current source dataset
    _mode - data parsing mode for the map
    name_col - column to pull names from
    lat_col - column to pull lats from
    lon_col - column to pull lons from
    value_col - column to pull values from
    scale - scale of the map
    radius - search radius for grid generation (in degrees)
    border_offset - area of blank space around the map (in degrees)
    _values - values of points being plotted
    _lats - latitudes of points being plotted
    _lons - longitudes of points being plotted
    _names - names of points being plotted
    _legend - value to number mapping for the points
    _lat_min - smallest lat subtracted by border_width
    _lat_max - biggest lat added by border_width
    _lon_min - smallest lon subtracted by border_width
    _lon_max - biggest lon added by border_width
    """
    grid: np.ndarray
    _verboseprint: Callable[..., Union[str, None]]
    _filepath: str
    _mode: str
    name_col: int
    lat_col: int
    lon_col: int
    value_col: int
    scale: float
    radius: float
    border_offset: float
    north_offset: float
    south_offset: float
    east_offset: float
    west_offset: float
    _values: List[str]
    _lats: List[float]
    _lons: List[float]
    _names: List[str]
    _legend: Dict[str, int]
    _lat_min: float
    _lat_max: float
    _lon_min: float
    _lon_max: float

    def __init__(self, filepath: str, mode: str = MODES[0],
                 name_col: int = DEFAULT_NAME_COL, lat_col: int = DEFAULT_LAT_COL,
                 lon_col: int = DEFAULT_LON_COL, value_col: int = DEFAULT_VALUE_COL,
                 scale: float = DEFAULT_SCALE, radius: float = DEFAULT_RADIUS,
                 border_offset: float = 0, north_offset: float = 0,
                 south_offset: float = 0, east_offset: float = 0,
                 west_offset: float = 0, verbose: bool = False) -> None:
        """
        Initializes a new heatmap
        """
        self._filepath, self._mode, self.name_col = filepath, mode, name_col
        self.lat_col, self.lon_col, self.value_col = lat_col, lon_col, value_col
        self.scale, self.radius, self.border_offset = scale, radius, border_offset
        self.north_offset, self.south_offset = north_offset, south_offset
        self.east_offset, self.west_offset = east_offset, west_offset
        self._verboseprint = print if verbose else lambda *a, **k: None

    @property
    def filepath(self) -> str:
        """
        Get current source filepath
        """
        return self._filepath
    
    @filepath.setter
    def filepath(self, value: str) -> None:
        verify_dataset(value)
        self._filepath = value

    @property
    def mode(self) -> str:
        """
        Get current map mode
        """
        return self._mode

    @mode.setter
    def mode(self, value: str) -> None:
        value = value.lower()
        assert value in MODES
        self._mode = value

    def change_dataset(self, filepath: str,
                       name_col: int = 0, lat_col: int = 1,
                       lon_col: int = 2, value_col: int = 3):
        """
        Set a different dataset to be read
        """
        verify_dataset(self._filepath)
        self._filepath, self.name_col = filepath, name_col
        self.lat_col, self.lon_col, self.value_col = lat_col, lon_col, value_col

    
    def _initialize_data(self) -> None:
        """
        Loads the dataset and prepares for it to be generated
        """
        data = load_from_csv(self._filepath, self.name_col, self.lat_col,
                             self.lon_col, self.value_col)
        value_label = data.pop()
        self._names, self._lats, self._lons, self._values = data

        self._lat_max = max(self._lats) + self.border_offset + self.north_offset
        self._lat_min = min(self._lats) - self.border_offset - self.south_offset
        self._lon_max = max(self._lons) + self.border_offset + self.east_offset
        self._lon_min = min(self._lons) - self.border_offset - self.west_offset

        # assigning a number to each unique value provided, and map it to the points
        count = IterCounter(self._values)
        # value[0] because value from a enumerate(IterCounter) gives a 
        # tuple of the name of the item and how many of that item 
        # are contained within the count.
        if self._mode == MODES[0]:
            self._legend = {value[0]: i + 1 if i + 1 <= len(COLOURS) else len(COLOURS)
                            for i, value in enumerate(count.most_common())}
            self._verboseprint(self._legend)

        elif self._mode == MODES[1]:
            self._legend = {value_label: 1}
            self._values = [float(v) for v in self._values]

    
    def calculate_grid(self) -> None:
        """
        Calculates the values of the grid based on current information
        """
        self._verboseprint("Reading data...")

        self._initialize_data()
        self._verboseprint("Initializing map grid generation...")
        # initial grid
        grid_width = ceil((self._lon_max - self._lon_min) / self.scale)
        grid_height = ceil((self._lat_max - self._lat_min) / self.scale)
        self._verboseprint(("Map Parameters\n"
                            "--------------\n"
                            "Lat Min:         {}\n"
                            "Lat Max:         {}\n"
                            "Lat Grid Height: {}\n"
                            "Lon Min:         {}\n"
                            "Lon Max:         {}\n"
                            "Lon Grid Width:  {}\n"
                            "Grid Dimensions: ({}, {})\n").format(
                            self._lat_min, self._lat_max, grid_height,
                            self._lon_min, self._lon_max, grid_width,
                            grid_width, grid_height))

        grid = np.full((grid_height, grid_width), 0.0)

        self._verboseprint("Determining grid coordinates of points...")
        x_coords, y_coords, remove = [], [], []
        item_count = len(self._names)
        for i in range(item_count):
            lat, lon = self._lats[i], self._lons[i]
            value, name = self._values[i], self._names[i]
            if (lon < self._lon_min - self.radius or
                lon > self._lon_max + self.radius or
                lat < self._lat_min - self.radius or
                lat > self._lat_max + self.radius):
                remove.append(i)
                continue
            grid_x = ceil((lon - self._lon_min) / self.scale)
            grid_y = ceil((lat - self._lat_min) / self.scale)
            x_coords.append(grid_x)
            y_coords.append(grid_y)
            # y comes first in the way the grid displays the map
            # which is why it is reversed in this fashion.
            # debugging is shown in x y to keep in line with
            # conventional thinking, since if you think of them
            # in the x y convention then it still makes sense 
            # on the actual map.
            value_text = ("{} ({})".format(value, self._legend[value])
                          if self._mode == MODES[0] else value)
            self._verboseprint(("{} -> Map Coords: ({}, {}) || "
                                "Grid Coords: ({}, {}) || "
                                "Value: {}").format(
                                name, lat, lon, grid_x, grid_y, value_text))
        remove.sort(reverse=True)
        for i in remove:
            self._lats.pop(i)
            self._lons.pop(i)
            self._values.pop(i)
            self._names.pop(i)
        self._verboseprint("Filling in the grid...")
        try:
            import progressbar # displays progress nicely if installed
            prog_bar = progressbar.ProgressBar()
        except ImportError:
            prog_bar = lambda l: l
        for i in prog_bar(range(grid_height)):
            for j in range(grid_width):
                radius = self.radius / self.scale
                vicinity = [[point_i, 
                            sqrt((x_coords[point_i] - j) ** 2 +
                            (y_coords[point_i] - i) ** 2)] 
                            for point_i in range(item_count)]
                if [item for item in vicinity if item[1] <= radius]:
                    vicinity = [[point_i, 0.999 - point_dist / radius]
                                for point_i, point_dist in vicinity
                                if point_dist <= radius]
                    # influence mode
                    if self._mode == MODES[0]:
                        weights = Counter()
                        for point_i, weighted_dist in vicinity:
                            weights[self._values[point_i]] += weighted_dist
                        weights = list(weights.items())
                        weights.sort(key=lambda item: item[1], reverse=True)
                        dominant = weights[0]
                        d_value = dominant[0]
                        d_weight = dominant[1]
                        # sum of the other weights
                        rest = sum([weight for value, weight in weights[1:]])
                        if not d_weight < rest:
                            total_weight = d_weight - rest
                            grid[i][j] = (self._legend[d_value]
                                          if total_weight >= 0.999
                                          else self._legend[d_value] - (0.999 - total_weight))
                    # weighted mode
                    elif self._mode == MODES[1]:
                        total_count = 0
                        for point_i, weighted_dist in vicinity:
                            total_count += weighted_dist * self._values[point_i]
                        grid[i][j] = total_count
        
        self.grid = grid
    
    def display_map(self, colourmap: Union[str, Colormap, None] = None,
                    legend_loc: Union[str, int, None] = None,
                    legend_fontsize: int = 14) -> None:
        """
        Uses matplotlib to display the map
        Requires matplotlib and basemap to be installed basemap.in order to function
        """
        from mpl_toolkits.basemap import Basemap
        from matplotlib.patches import Patch
        import matplotlib.pyplot as plt

        colourmap = "viridis_r" if colourmap == None else colourmap
        legend_loc = "best" if legend_loc == None else legend_loc
        assert legend_loc in LEGEND_LOCATIONS

        plt.figure(figsize=FIGSIZE)

        m = Basemap(projection="merc", resolution="i",
                            llcrnrlat=self._lat_min, llcrnrlon=self._lon_min,
                            urcrnrlat=self._lat_max, urcrnrlon=self._lon_max)
        
        m.drawcountries()
        m.fillcontinents(color="white", lake_color="#1c9ef7", alpha=.1)
        m.drawcoastlines()
        m.drawrivers(color="#1c9ef7")

        if self._mode == MODES[0]:
            m.imshow(self.grid, alpha=1, vmin=0, vmax=len(COLOURS),
                     cmap=get_unified_colourmap())

            legend_items = []
            for name, value in self._legend.items():
                legend_items.append(Patch(color=COLOURS[value - 1], label=name))
            plt.legend(handles=legend_items, loc=legend_loc, fontsize=legend_fontsize)

        elif self._mode == MODES[1]:
            img = m.imshow(self.grid, alpha=1, cmap=colourmap)
            plt.colorbar(img)
            plt.title(list(self._legend.keys())[0], size=30)

        plt.show()
        
if __name__ == "__main__":
    from main import main
    main()
