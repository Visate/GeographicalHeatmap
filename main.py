#!/usr/bin/env python
"""
entry point for heatmap program
"""
import argparse
from utilities import verify_dataset
from heatmap import (Heatmap, DEFAULT_NAME_COL, 
                     DEFAULT_LAT_COL, DEFAULT_LON_COL, DEFAULT_VALUE_COL,
                     DEFAULT_SCALE, DEFAULT_RADIUS, DEFAULT_BORDER_SIZE, MODES)

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
    parser.add_argument("-bsize", "--bordersize")
    args = parser.parse_args()

    dataset = args.dataset
    mode = args.mode.lower() if args.mode else None
    name_col = int(args.name_col) if args.name_col else None
    lat_col = int(args.lat_col) if args.lat_col else None
    lon_col = int(args.lon_col) if args.lon_col else None
    value_col = int(args.value_col) if args.value_col else None
    scale = float(args.scale) if args.scale else None
    radius = float(args.radius) if args.radius else None
    border_size = float(args.bordersize) if args.bordersize else None

    while not dataset:
        try:
            dataset = input("Which dataset csv file to use? (enter filepath): ")
            verify_dataset(dataset)
        except Exception as err:
            dataset = None
            print("Error: {}. Please try again.".format(err))

    while not mode:
        try:
            mode = input(("What mode is the map in? Leave blank for default. "
                         "Type 'list' to get a list of the modes: ")).lower()
            if mode == "list":
                mode = None
                print("Available modes: {}\n".format(", ".join(MODES)))
                print("Please refer to the documentation for more details.")
            if not mode:
                mode = MODES[0]
            elif mode not in MODES:
                raise ValueError("invalid mode")
        except Exception as err:
            mode = None
            print("Error: {}. Please try again.".format(err))

    while not name_col:
        try:
            name_col = input(("What column are the point names in? "
                             "Leave blank for column {}: ".format(DEFAULT_NAME_COL + 1)))
            name_col = DEFAULT_NAME_COL + 1 if not name_col else int(name_col)
        except Exception as err:
            name_col = None
            print("Error: {}. Please try again.".format(err))

    while not lat_col:
        try:
            lat_col = input(("What column are the latitudes in? "
                             "Leave blank for column {}: ".format(DEFAULT_LAT_COL + 1)))
            lat_col = DEFAULT_LAT_COL + 1 if not lat_col else int(lat_col)
        except Exception as err:
            lat_col = None
            print("Error: {}. Please try again.".format(err))

    while not lon_col:
        try:
            lon_col = input(("What column are the longitudes in? "
                             "Leave blank for column {}: ".format(DEFAULT_LON_COL + 1)))
            lon_col = DEFAULT_LON_COL + 1 if not lon_col else int(lon_col)
        except Exception as err:
            lon_col = None
            print("Error: {}. Please try again.".format(err))

    while not value_col:
        try:
            value_col = input(("What column are the values in? "
                             "Leave blank for column {}: ".format(DEFAULT_VALUE_COL + 1)))
            value_col = DEFAULT_VALUE_COL + 1 if not value_col else int(value_col)
        except Exception as err:
            value_col = None
            print("Error: {}. Please try again.".format(err))

    while not scale:
        try:
            scale = input(("What is the scale of the map? "
            "Leave blank for the default value of 0.007 "
            "(smaller = more fidelity but slower, "
            "larger = less accurate but faster): "))
            scale = DEFAULT_SCALE if not scale else float(scale)
        except Exception:
            scale = None
            print("Please input a valid number.")
    
    while not radius:
        try:
            radius = input(("What is the checking radius for the data? "
            "Leave blank for the default of 0.3 "
            "(This is based on latitude/longitude degrees "
            "and determines how far the program will look "
            "for another point in the area): "))
            radius = DEFAULT_RADIUS if not radius else float(radius)
        except Exception:
            radius = None
            print("Please input a valid number.")

    while not border_size:
        try:
            border_size = input(("What is the border size of the map? "
                                 "Leave blank for default of 0.03"))
            border_size = DEFAULT_BORDER_SIZE if not border_size else float(border_size)
        except Exception:
            border_size = None
            print("Please input a valid number.")

    heatmap = Heatmap(dataset, mode, name_col - 1, lat_col - 1, lon_col - 1,
                      value_col - 1, scale, radius, border_size, args.verbose)
    heatmap.calculate_grid()
    heatmap.display_map()

if __name__ == "__main__":
    main()