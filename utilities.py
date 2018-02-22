"""
utilities module for map
"""
import csv

def load_from_csv(filepath: str) -> tuple:
    """ Loads the csv file and processes the data
    """
    lats, lons, values, names = [], [], [], []

    # make sure the file being opened is a csv file
    assert filepath[-4:] == ".csv"

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

        assert all([len(x) == len(lats) for x in [lons, values, names]])

        return lats, lons, values, names