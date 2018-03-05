"""
utilities module for map
"""
import csv

class Counter(dict):
    """ A dictionary with support for
    adding values despite missing keys
    """
    def __missing__(self, key: object) -> int:
        return 0

def verify_dataset(filepath: str) -> None:
    """
    Verifies that the filepath provided is a valid
    dataset that can be used by the Heatmap
    """
    assert filepath[-4:] == ".csv", "not a csv file"
    open(filepath)

def load_from_csv(filepath: str, name_col: int = 0,
                  lat_col: int = 1, lon_col: int = 2, 
                  value_col: int = 3) -> tuple:
    """
    Loads the csv file and processes the data
    """
    names, lats, lons, values = [], [], [], []

    verify_dataset(filepath)

    with open(filepath) as file:
        reader = csv.reader(file)
        value_label = next(reader)[value_col]
        for row in reader:
            if (not row[name_col].strip()
                or not row[lat_col].strip()
                or not row[lon_col].strip()
                or not row[value_col].strip()):
                continue
            if row[value_col] == "no answer" or row[value_col] == "no data":
                continue
            name = row[name_col].strip()
            lat = float(row[lat_col])
            lon = float(row[lon_col])
            value_split = row[value_col].strip().split("/")
            for value in value_split:
                names.append(name)
                lats.append(lat)
                lons.append(lon)
                values.append(value)

        assert all([len(x) == len(names) for x in [lats, lons, values]])

        return [names, lats, lons, values, value_label]
