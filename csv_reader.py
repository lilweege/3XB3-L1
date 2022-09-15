import csv
from types import SimpleNamespace

def autoconvert(value):
    try:
        return int(value)
    except ValueError: pass
    try:
        return float(value)
    except ValueError: pass
    return value

def read_csv_contents(filename):
    with open(filename, "r") as file:
        return [SimpleNamespace(**{ k:autoconvert(v) for k, v in row.items() })
                for row in csv.DictReader(file, delimiter=',', quotechar='"')]
