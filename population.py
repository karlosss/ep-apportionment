import csv
from collections import OrderedDict


def get_pop(year):
    with open("population.csv") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        yr_list = data[0]
        data = data[1:]
        i = 1
        while int(yr_list[i]) != year:
            i += 1
            if i == len(yr_list):
                raise RuntimeError("Invalid year")
        out = OrderedDict()
        for row in data:
            out[row[0]] = int(row[i])
        return out
