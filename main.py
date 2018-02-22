#!/usr/bin/env python
"""
Geographical heatmap module
written by Richard Gan
"""
from typing import List, Dict, Any, Callable, Union
from collections import Counter
from math import sqrt, ceil
import numpy as np
from mpl_toolkits import basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from colourmaps import get_colourmap, SIZE
from utilities import load_from_csv

BORDER_WIDTH = 0.1 # how much space around the smallest & biggest points (deg)
FIGSIZE = (16, 10)

class Heatmap:
    """
    Defines a heatmap

    grid - grid of the heatmap
    _verboseprint - function for debugging purposes
    _scale - scale of the map
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
    _scale: float
    _values: List[str]
    _lats: List[float]
    _lons: List[float]
    _names: List[str]
    _legend: Dict[str, int]
    _lat_min: float
    _lat_max: float
    _lon_min: float
    _lon_max: float

    def __init__(self, filepath: str, scale: float = 0.007, 
                 verbose: bool = False, threshold: float = 0) -> None:
        """
        Initializes a new heatmap
        """
        self._scale, self._threshold = scale, threshold
        self._verboseprint = print if verbose else lambda *a, **k: None

        self._lats, self._lons, self._values, self._names = load_from_csv(filepath)

        self._lat_min = min(self._lats) - BORDER_WIDTH
        self._lat_max = max(self._lats) + BORDER_WIDTH
        self._lon_min = min(self._lons) - BORDER_WIDTH
        self._lon_max = max(self._lons) + BORDER_WIDTH

        # assigning a number to each unique value provided, and map it to the points
        count = Counter(self._values)
        self._legend = {value[0]: i + 1 if i + 1 <= SIZE else SIZE
                        for i, value in enumerate(count.most_common())}
        self._verboseprint(self._legend)

        self.grid = self._calculate_grid()
    
    def _calculate_grid(self) -> np.ndarray:
        """
        Calculates the values of the grid based on current information
        """
        self._verboseprint("Initializing map grid generation...")
        # initial grid
        grid_width = ceil((self._lon_max - self._lon_min) / self._scale)
        grid_height = ceil((self._lat_max - self._lat_min) / self._scale)
        self._verboseprint(("Map Parameters\n"
                            "--------------\n"
                            "Lat Min:         {}\n"
                            "Lat Max:         {}\n"
                            "Lat Grid Height: {}\n"
                            "Lon Min:         {}\n"
                            "Lon Max:         {}\n"
                            "Lon Grid Width:  {}\n"
                            "Grid Dimensions: ({}, {})\n"
                            "Threshold:       {}\n"))

        grid = np.full((grid_height, grid_width), 0.0)

        self._verboseprint("Determining grid coordinates of points...")
        x_coords, y_coords = [], []
        item_count = len(self._lats)
        for i in range(item_count):
            lat, lon = self._lats[i], self._lons[i]
            value, name = self._values[i], self._names[i]
            grid_x = ceil((lon - self._lon_min) / scale)
            grid_y = ceil((lat - self._lat_min) / scale)
            x_coords.append(grid_x)
            y_coords.append(grid_y)
            # y comes first in the way the grid displays the map
            # which is why it is reversed in this fashion.
            # debugging is shown in x y to keep in line with
            # conventional thinking.
            grid[grid_y][grid_x] = self._legend[value]
            self._verboseprint(("{} -> Map Coords: ({}, {}) || "
                                "Grid Coords: ({}, {}) || "
                                "Value: {} ({})").format(
                                name, lat, lon, grid_x, grid_y, 
                                value, self._legend[value]))

        self._verboseprint("Filling in the grid...")
        try:
            import progressbar
            prog_bar = progressbar.ProgressBar()
        except ImportError:
            prog_bar = lambda l: l
        for i in prog_bar(range(grid_height)):
            for j in range(grid_width):
                vicinity = []
                radius = 0
                while not vicinity:
                    radius += 0.05 / scale
                    vicinity = []
    
    def display_map(self) -> None:
        """
        Uses matplotlib to display the map
        """
        plt.figure(figsize=FIGSIZE)

        m = basemap.Basemap(projection="merc", resolution="i",
                            llcrnrlat=self._lat_min, llcrnrlon=self._lon_min,
                            urcrnrlat=self._lat_max, urcrnrlon=self._lon_max)
        
        m.drawcountries()
        m.fillcontinents(color="white", lake_color="#ic9ef7", alpha=.1)
        m.drawcoastlines()
        m.drawrivers(color="#1c9ef7", alpha=.1)

        overlay_cmap = LinearSegmentedColormap.from_list('heatmap_colourmap',
        get_colourmap(len(self._legend)))

        m.imshow(self._grid, cmap=overlay_cmap, alpha=1, 
                 vmin=0, interpolation="bicubic")
        
        plt.show()
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=("Generates a heatmap from "
                                                  "data and displays it"))
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    dataset = None
    while not dataset:
        try:
            dataset = input("Which dataset csv file to use? (enter filepath): ")
            if dataset[-4:] != ".csv":
                raise ValueError("csv file not provided")
            open(dataset)
        except ValueError:
            print("Please provide a csv file.")
            dataset = None
        except Exception as err:
            print("Error: {}. Please provide a valid dataset.".format(err))
    scale = None
    while not scale:
        try:
            scale = input(("What is the scale of the map? "
            "Leave blank for the default value of 0.007 "
            "(smaller = more fidelity but slower, "
            "larger = less accurate but faster): "))
            scale = 0.007 if not scale else float(scale)
        except Exception:
            print("Please input a valid number.")
            scale = None

    heatmap = Heatmap(dataset, scale, args.verbose)
