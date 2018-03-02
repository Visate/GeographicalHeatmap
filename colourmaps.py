"""
colourmaps module for heatmap
"""
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from math import floor, ceil, modf

# defines how many colours there are and which colours they are
# must be updated every time a colour is added to _unified_map
COLOURS = ["#5b2b8c", "#004f82", "#00632b", "#a53d00", "#870000",
           "#0a2d66", "#ff00ff", "#ffff00", "#00ffff", "#b23872"]

# the colourmap is as follows:
# purples, blues, greens, oranges, reds, 
# darkblues, pinks, yellows, lightblues, darkpinks
# every two items represents one part of the map
# has a maximum support for len(COLOURS) unique points
# the mapping utility used must have vmin set to 0
# and vmax set to len(COLOURS) in order to preserve how the colors look
_unified_map = {'red': ((0., 0.36, 0.36),
                       (0.10, 0.36, 0.36),
                       (0.101, 0, 0),
                       (0.20, 0, 0),
                       (0.201, 0, 0),
                       (0.30, 0, 0),
                       (0.301, 0.65, 0.65),
                       (0.40, 0.65, 0.65),
                       (0.401, 0.53, 0.53),
                       (0.50, 0.53, 0.53),
                       (0.501, 0.04, 0.04),
                       (0.60, 0.04, 0.04),
                       (0.601, 1, 1),
                       (0.70, 1, 1),
                       (0.701, 1, 1),
                       (0.80, 1, 1),
                       (0.801, 0, 0),
                       (0.90, 0, 0),
                       (0.901, 0.7, 0.7),
                       (1, 0.7, 0.7)),
                
               'green': ((0., 0.17, 0.17),
                         (0.10, 0.17, 0.17),
                         (0.101, 0.31, 0.31),
                         (0.20, 0.31, 0.31),
                         (0.201, 0.39, 0.39),
                         (0.30, 0.39, 0.39),
                         (0.301, 0.24, 0.24),
                         (0.40, 0.24, 0.24),
                         (0.401, 0, 0),
                         (0.50, 0, 0),
                         (0.501, 0.18, 0.18),
                         (0.60, 0.18, 0.18),
                         (0.601, 0, 0),
                         (0.70, 0, 0),
                         (0.701, 1, 1),
                         (0.80, 1, 1),
                         (0.801, 1, 1),
                         (0.90, 1, 1),
                         (0.901, 0.22, 0.22),
                         (1, 0.22, 0.22)),
               
               'blue': ((0., 0.55, 0.55),
                        (0.10, 0.55, 0.55),
                        (0.101, 0.51, 0.51),
                        (0.20, 0.51, 0.51),
                        (0.201, 0.17, 0.17),
                        (0.30, 0.17, 0.17),
                        (0.301, 0, 0),
                        (0.40, 0, 0),
                        (0.401, 0, 0),
                        (0.50, 0, 0),
                        (0.501, 0.4, 0.4),
                        (0.60, 0.4, 0.4),
                        (0.601, 1, 1),
                        (0.70, 1, 1),
                        (0.701, 0, 0),
                        (0.80, 0, 0),
                        (0.801, 1, 1),
                        (0.90, 1, 1),
                        (0.901, 0.45, 0.45),
                        (1, 0.45, 0.45)),
               
               'alpha': ((0., 0, 0),
                         (0.10001, 1, 1),
                         (0.10001, 0, 0),
                         (0.20001, 1, 1),
                         (0.20001, 0, 0),
                         (0.30001, 1, 1),
                         (0.30001, 0, 0),
                         (0.40001, 1, 1),
                         (0.40001, 0, 0),
                         (0.50001, 1, 1),
                         (0.50001, 0, 0),
                         (0.60001, 1, 1),
                         (0.60001, 0, 0),
                         (0.70001, 1, 1),
                         (0.70001, 0, 0),
                         (0.80001, 1, 1),
                         (0.80001, 0, 0),
                         (0.90001, 1, 1),
                         (0.90001, 0, 0),
                         (1, 1, 1))}

def get_unified_colourmap() -> LinearSegmentedColormap:
    """Returns an adjusted version of the unified colourmap
    according to the number provided
    """
    unified_cmap = LinearSegmentedColormap('unified_cmap', _unified_map, N=50000)
    return unified_cmap
