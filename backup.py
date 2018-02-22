from math import sqrt
import progressbar
import csv
import numpy as np
from mpl_toolkits import basemap
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import get_cmap

SCALE = 0.005
THRESHOLD = 5  # gap between boundaries in the mesh

"""
Does the necessary calculations in order to generate the mesh representing the area
of effect for each point given.
"""
def generate_overlay(data, lat_min, lat_max, lon_min, lon_max):
    print("Initiating map overlay...")
    # initial grid
    grid_width = int((lon_max - lon_min) / SCALE)
    grid_height = int((lat_max - lat_min) / SCALE / 0.5)
    grid = np.zeros((grid_width, grid_height))

    print("Placing initial points on map...")
    for i, item in enumerate(data):
        lat, lon, value = item
        grid_x = int((lat - lat_min) / SCALE / 0.5)
        grid_y = int((lon - lon_min) / SCALE)
        data[i].append(grid_x)
        data[i].append(grid_y)
        grid[grid_x][grid_y] = value

    print("Filling in the other spaces on the map...")
    bar = progressbar.ProgressBar()
    for i in bar(range(grid_width)):
        for j in range(grid_height):
            # current point = i,j
            # compare distance to each point and track
            distances = []
            for point in data:
                # + = up, - = down
                x_dist = i - point[3]
                # + = right, - = left
                y_dist = point[4] - j

                dist = sqrt(x_dist ** 2 + y_dist ** 2)

                # x distance, y distance, total distance, value
                info = [x_dist, y_dist, dist, point[2]]
                distances.append(info)

            distances.sort(key=lambda point: point[2])

            north = [point for point in distances if point[1] > 0]
            south = [point for point in distances if point[1] < 0]
            east = [point for point in distances if point[0] > 0]
            west = [point for point in distances if point[0] < 0]
            closest = distances[0]

            north.sort(key=lambda point: point[1])
            south.sort(key=lambda point: point[1], reverse=True)
            east.sort(key=lambda point: point[0])
            west.sort(key=lambda point: point[0], reverse=True)

            grid[i][j] = closest[3]

    return grid

# load data
def load_from_csv(filepath):
    print("Reading data from CSV file...")
    lats, lons, values = [], [], []
    data = []

    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append([float(row[1]), float(row[2]), row[3]])
            lats.append(float(row[1]))
            lons.append(float(row[2]))
            values.append(row[3])

    return lats, lons, values, data


def generate_map(filepath):
    lats, lons, values, data = load_from_csv(filepath)

    # determining where the map should be centered around
    lat_min = min(lats)-0.5
    lat_max = max(lats)+0.5
    lon_min = min(lons)-1
    lon_max = max(lons)+1

    # assigning a number to each unique value provided, then mapping it to the points
    legend = {value: i + 1 for i, value in enumerate(set(values))}
    values = [legend[value] for value in values]

    m = basemap.Basemap(projection='merc', resolution='i',
                        llcrnrlat=lat_min, llcrnrlon=lon_min,
                        urcrnrlat=lat_max, urcrnrlon=lon_max)
    m.drawcountries()
    m.fillcontinents(color='white', lake_color='#1c9ef7', alpha=.4)
    m.drawcoastlines()
    m.drawrivers(color='#1c9ef7')

    overlay = generate_overlay(data, lat_min, lat_max, lon_min, lon_max)
    overlay_cmap = get_cmap('jet')
    overlay_cmap.set_under('white')
    m.imshow(overlay, cmap=overlay_cmap, alpha=1, interpolation='bilinear', vmin=1)

    plt.show()

generate_map('tests/map2.csv')
