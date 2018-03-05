#!/usr/bin/env python
"""
entry point for heatmap program
"""
import argparse
from matplotlib.cm import get_cmap
from utilities import verify_dataset
from heatmap import (Heatmap, DEFAULT_NAME_COL, 
                     DEFAULT_LAT_COL, DEFAULT_LON_COL, DEFAULT_VALUE_COL,
                     DEFAULT_SCALE, DEFAULT_RADIUS, MODES, LEGEND_LOCATIONS)

BORDER_MODES = ["entire", "specific", "both"]

def main():
    parser = argparse.ArgumentParser(description=("Generates a heatmap from "
                                                  "data and displays it"))
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-d", "--dataset")
    parser.add_argument("-m", "--mode")
    parser.add_argument("-nc", "--name_col")
    parser.add_argument("-latc", "--lat_col")
    parser.add_argument("-lonc", "--lon_col")
    parser.add_argument("-vc", "--value_col")
    parser.add_argument("-s", "--scale")
    parser.add_argument("-r", "--radius")
    parser.add_argument("-border", "--border_offset")
    parser.add_argument("-north", "--north_offset")
    parser.add_argument("-south", "--south_offset")
    parser.add_argument("-east", "--east_offset")
    parser.add_argument("-west", "--west_offset")
    parser.add_argument("-cmap", "--colourmap")
    parser.add_argument("-lloc", "--legend_location")
    parser.add_argument("-lfs", "--legend_fontsize")

    args = parser.parse_args()

    dataset = args.dataset
    mode = args.mode.lower() if args.mode else None
    mode = None if mode not in MODES else mode
    name_col = int(args.name_col) if args.name_col else None
    lat_col = int(args.lat_col) if args.lat_col else None
    lon_col = int(args.lon_col) if args.lon_col else None
    value_col = int(args.value_col) if args.value_col else None
    scale = float(args.scale) if args.scale else None
    radius = float(args.radius) if args.radius else None
    border_offset = float(args.border_offset) if args.border_offset else None
    north_offset = float(args.north_offset) if args.north_offset else None
    south_offset = float(args.south_offset) if args.south_offset else None
    east_offset = float(args.east_offset) if args.east_offset else None
    west_offset = float(args.west_offset) if args.west_offset else None
    colourmap = args.colourmap if args.colourmap else None
    legend_location = args.legend_location if args.legend_location else None
    legend_location = None if legend_location not in LEGEND_LOCATIONS else legend_location
    legend_fontsize = int(args.legend_fontsize) if args.legend_fontsize else None

    while dataset == None:
        try:
            dataset = input("Which dataset csv file to use? (enter filepath): ")
            verify_dataset(dataset)
        except Exception as err:
            dataset = None
            print("Error: {}. Please try again.".format(err))

    while mode == None:
        try:
            mode = input(("What mode is the map in? Leave blank for default. "
                         "Type 'list' to get a list of the modes: ")).lower()
            if mode == "list":
                mode = None
                print("Available modes: {}\n".format(", ".join(MODES)))
                print("Please refer to the documentation for more details.")
                continue
            if not mode:
                mode = MODES[0]
            elif mode not in MODES:
                raise ValueError("invalid mode")
        except Exception as err:
            mode = None
            print("Error: {}. Please try again.".format(err))

    while name_col == None:
        try:
            name_col = input(("What column are the point names in? "
                             "Leave blank for column {}: ".format(DEFAULT_NAME_COL + 1)))
            name_col = DEFAULT_NAME_COL + 1 if name_col == "" else int(name_col)
        except Exception as err:
            name_col = None
            print("Error: {}. Please try again.".format(err))

    while lat_col == None:
        try:
            lat_col = input(("What column are the latitudes in? "
                             "Leave blank for column {}: ".format(DEFAULT_LAT_COL + 1)))
            lat_col = DEFAULT_LAT_COL + 1 if lat_col == "" else int(lat_col)
        except Exception as err:
            lat_col = None
            print("Error: {}. Please try again.".format(err))

    while lon_col == None:
        try:
            lon_col = input(("What column are the longitudes in? "
                             "Leave blank for column {}: ".format(DEFAULT_LON_COL + 1)))
            lon_col = DEFAULT_LON_COL + 1 if lon_col == "" else int(lon_col)
        except Exception as err:
            lon_col = None
            print("Error: {}. Please try again.".format(err))

    while value_col == None:
        try:
            value_col = input(("What column are the values in? "
                             "Leave blank for column {}: ".format(DEFAULT_VALUE_COL + 1)))
            value_col = DEFAULT_VALUE_COL + 1 if value_col == "" else int(value_col)
        except Exception as err:
            value_col = None
            print("Error: {}. Please try again.".format(err))

    while scale == None:
        try:
            scale = input(("What is the scale of the map? "
            "Leave blank for the default value of 0.007 "
            "(smaller = more fidelity but slower, "
            "larger = less accurate but faster): "))
            scale = DEFAULT_SCALE if scale == "" else float(scale)
        except Exception:
            scale = None
            print("Please input a valid number.")
    
    while radius == None:
        try:
            radius = input(("What is the checking radius for the data? "
            "Leave blank for the default of 0.3 "
            "(This is based on latitude/longitude degrees "
            "and determines how far the program will look "
            "for another point in the area): "))
            radius = DEFAULT_RADIUS if radius == "" else float(radius)
        except Exception:
            radius = None
            print("Please input a valid number.")

    border_mode = None
    if (border_offset == None and north_offset == None and south_offset == None
        and east_offset == None and west_offset == None):
        while border_mode == None:
            try:
                border_mode = input(("Would you like to specify an offset "
                                     "for the entire border, or assign "
                                     "specific offset to each side? (type "
                                     "'entire', 'specific', 'both', or "
                                     "leave blank to pick 'entire'): ")).lower()
                if border_mode and border_mode not in BORDER_MODES:
                    raise ValueError("invalid border mode provided")
                border_mode = BORDER_MODES[0] if border_mode == "" else border_mode
            except Exception as err:
                border_mode = None
                print("Error: {}. Please try again.")

        if border_mode == BORDER_MODES[0] or border_mode == BORDER_MODES[2]:
            while border_offset == None:
                try:
                    border_offset = input(("What is the border offset of the map? "
                                           "Leave blank for default of 0.03: "))
                    border_offset = 0.03 if border_offset == "" else float(border_offset)
                except Exception:
                    border_offset = None
                    print("Please input a valid number.")
        
        if border_mode == BORDER_MODES[1] or border_mode == BORDER_MODES[2]:
            while north_offset == None:
                try:
                    north_offset = input(("What is the north side offset? "
                                        "Leave blank for 0: "))
                    north_offset = 0 if north_offset == "" else float(north_offset)
                except Exception:
                    north_offset = None
                    print("Please input a valid number.")

            while south_offset == None:
                try:
                    south_offset = input(("What is the south side offset? "
                                        "Leave blank for 0: "))
                    south_offset = 0 if south_offset == "" else float(south_offset)
                except Exception:
                    south_offset = None
                    print("Please input a valid number.")

            while east_offset == None:
                try:
                    east_offset = input(("What is the east side offset? "
                                        "Leave blank for 0: "))
                    east_offset = 0 if east_offset == "" else float(east_offset)
                except Exception:
                    east_offset = None
                    print("Please input a valid number.")

            while west_offset == None:
                try:
                    west_offset = input(("What is the west side offset? "
                                        "Leave blank for 0: "))
                    west_offset = 0 if west_offset == "" else float(west_offset)
                except Exception:
                    west_offset = None
                    print("Please input a valid number.")

    border_offset = 0 if border_offset == None else border_offset
    north_offset = 0 if north_offset == None else north_offset
    south_offset = 0 if south_offset == None else south_offset
    east_offset = 0 if east_offset == None else east_offset
    west_offset = 0 if west_offset == None else west_offset

    heatmap = Heatmap(dataset, mode, name_col - 1, lat_col - 1, lon_col - 1,
                      value_col - 1, scale, radius, border_offset, 
                      north_offset, south_offset, east_offset, west_offset,
                      args.verbose)
    
    heatmap.calculate_grid()

    if mode == MODES[0]:
        while legend_location == None:
            try:
                legend_location = input(("Where should the legend be? "
                                         "Type 'list' to get possible values. "
                                         "Leave blank for default: "))
                if legend_location == "list":
                    legend_location = None
                    print("Possible values are:")
                    print(", ".join(LEGEND_LOCATIONS))
                    continue
                if not legend_location:
                    legend_location = LEGEND_LOCATIONS[0]
                elif legend_location not in LEGEND_LOCATIONS:
                    raise ValueError("invalid location") 
            except Exception as err:
                legend_location = None
                print("Error: {}. Please try again.".format(err))

        while legend_fontsize == None:
            try:
                legend_fontsize = input(("What is the fontsize for the legend? "
                                         "Leave blank for 14: "))
                legend_fontsize = 14 if legend_fontsize == "" else int(legend_fontsize)
            except Exception as err:
                legend_fontsize = None
                print("Error: {}. Please try again.")

    elif mode == MODES[1]:
        while colourmap == None:
            try:
                colourmap = input(("Please specify a colourmap. "
                                   "Leave blank for default of viridis: "))
                colourmap = "viridis" if colourmap == "" else colourmap
                get_cmap(colourmap)
            except Exception as err:
                colourmap = None
                print("Error: {}. Please try again.".format(err))

    heatmap.display_map(colourmap, legend_location, legend_fontsize)

if __name__ == "__main__":
    main()