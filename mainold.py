"""
geographical heatmap
"""
from math import sqrt, floor, ceil
from collections import Counter
import csv
import progressbar
import numpy as np
from mpl_toolkits import basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import get_cmap
from colourmaps import get_colourmap

THRESHOLD_DEFAULT = 0
def generate_overlay(data, lat_min, lat_max, lon_min, lon_max, scale):
    """Does the necessary calculations in order to generate the mesh representing
    the area of effect for each point given.
    """
    print("Initiating map generation...")
    # initial grid
    grid_width = ceil((lon_max - lon_min) / scale)
    grid_height = ceil((lat_max - lat_min) / scale)
    print("Lat: {} - {} = {}".format(lat_max, lat_min, lat_max - lat_min))
    print("Lon: {} - {} = {}".format(lon_max, lon_min, lon_max - lon_min))
    print((lat_max - lat_min) / scale, (lon_max - lon_min) / scale)
    print(grid_width, grid_height)
    grid = np.full((grid_height, grid_width), 0.0)

    threshold = THRESHOLD_DEFAULT * scale
    print("Threshold: {}".format(threshold))

    print("Placing initial points on the map...")
    for i, item in enumerate(data):
        lat, lon, value, name = item
        grid_x = ceil((lon - lon_min) / scale)
        grid_y = ceil((lat - lat_min) / scale)
        print("{}: ({}, {}) coords: ({}, {})".format(name, grid_x, grid_y, lat, lon))
        data[i].pop()
        data[i].append(grid_x)
        data[i].append(grid_y)
        grid[grid_y][grid_x] = value

    print("Filling in the rest of the map...")
    prog_bar = progressbar.ProgressBar()
    for i in prog_bar(range(grid_height)):
        for j in range(grid_width):
            # current point = i,j
            # compare distance to each point and track
            distances = []
            for point in data:
                # + = up, - = down
                y_dist = i - point[4]
                # + = right, - = left
                x_dist = point[3] - j

                dist = sqrt(x_dist ** 2 + y_dist ** 2)

                # x distance, y distance, total distance, value
                info = [x_dist, y_dist, dist, point[2]]
                distances.append(info)

            distances.sort(key=lambda point: point[2])

            closest = distances[0]
            influence = distances[1]

            north = [point for point in distances if point[1] > 0]
            south = [point for point in distances if point[1] < 0]
            east = [point for point in distances if point[0] > 0]
            west = [point for point in distances if point[0] < 0]

            north.sort(key=lambda point: point[1])
            south.sort(key=lambda point: point[1], reverse=True)
            east.sort(key=lambda point: point[0])
            west.sort(key=lambda point: point[0], reverse=True)

            # if closest[3] == influence[3]:
            #     grid[i][j] = closest[3]
            # if not north or not south or not east or not west:
            #     edge_distances = [i, grid_height - i, j, grid_width - j]
            #     if not north and 
            # if abs(closest[2] - influence[2]) <= threshold:
            #     continue
            # else:
            try:
                grid[i][j] = closest[3] - (closest[2]/influence[2] * 0.5)
            except ZeroDivisionError:
                print("ZeroDivError at {} {}: {} - ({}/{} * 0.5)".format(i, j, closest[3], closest[2], influence[2]))
                grid[i][j] = closest[3] - (closest[2] * 0.5)

    return grid

# load data
def load_from_csv(filepath: str):
    """Loads the csv file and processes the data
    """
    lats, lons, values, names = [], [], [], []

    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if not row[1] or not row[2] or not row[3] or row[3] == " ":
                continue
            lats.append(float(row[1]))
            lons.append(float(row[2]))
            values.append(row[3])
            names.append(row[0])

    return lats, lons, values, names

def generate_map(filepath, scale):
    """Primary map generation function
    """
    lats, lons, values, names = load_from_csv(filepath)

    # determining where the map should be centered around
    lat_min = min(lats)-0.2
    lat_max = max(lats)+0.2
    lon_min = min(lons)-0.4
    lon_max = max(lons)+0.4

    # assigning a number to each unique value provided, then mapping it to the points
    count = Counter(values)
    legend = {value[0]: i + 1 if i + 1 < 11 else 10 for i, value in enumerate(count.most_common())}
    # legend = {value: i + 1 if i + 1 < 8 else 7 for i, value in enumerate(set(values))}
    print(legend)
    values = [legend[value] for value in values]

    plt.figure(figsize=(16, 10))

    m = basemap.Basemap(projection='merc', resolution='i',
                        llcrnrlat=lat_min, llcrnrlon=lon_min,
                        urcrnrlat=lat_max, urcrnrlon=lon_max)
    m.drawcountries()
    m.fillcontinents(color='white', lake_color='#1c9ef7', alpha=.4)
    m.drawcoastlines()
    m.drawrivers(color='#1c9ef7')

    data = [[lats[i], lons[i], values[i], names[i]] for i in range(len(values))]
    overlay = generate_overlay(data, lat_min, lat_max, lon_min, lon_max, scale)

    overlay_cmap = LinearSegmentedColormap.from_list('heatmap_colormap', get_colourmap(len(legend)))
    # cbar = plt.colorbar(overlay, location='bottom', pad='5%')
    m.imshow(overlay, cmap=overlay_cmap, alpha=1, vmin=0, interpolation='bicubic')

    plt.show()

if __name__ == "__main__":
    dataset = None
    while not dataset:
        try:
            dataset = input("Which dataset csv file to use? (enter filepath): ")
            if dataset[-4:] != ".csv":
                raise ValueError
            open(dataset)
        except ValueError:
            print("Please provide a csv file.")
            dataset = None
        except Exception:
            print("That is not a valid dataset. Please try again.")
            dataset = None
    scale = None
    while not scale:
        try:
            scale = input(("What is the scale of the map? "
            "Type 'default' or leave blank for the default value (0.007) "
            "(smaller = more fidelity but slower, "
            "larger = less accurate but faster): "))
            if scale == "default" or not scale:
                scale = 0.007
            else:
                scale = float(scale)
        except Exception:
            print("Please input a valid number or 'default'.")
            scale = None

    generate_map(dataset, scale)
