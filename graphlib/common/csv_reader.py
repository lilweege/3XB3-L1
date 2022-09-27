import csv
from types import SimpleNamespace

def read_csv_contents(filename):
    def autoconvert(value):
        try:
            return int(value)
        except ValueError: pass
        try:
            return float(value)
        except ValueError: pass
        if value == "NULL":
            return None
        return value

    with open(filename, "r") as file:
        return [SimpleNamespace(**{ k:autoconvert(v) for k, v in row.items() })
                for row in csv.DictReader(file, delimiter=',', quotechar='"')]
