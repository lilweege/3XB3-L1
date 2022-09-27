import csv
from types import SimpleNamespace


def read_csv_contents(filename):
    '''
    Open a csv file named <filename> and read
    the contents into a list of dictionaries
    '''

    def autoconvert(value):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if value == "NULL":
            return None
        return value

    with open(filename, "r") as file:
        return [SimpleNamespace(**{k: autoconvert(v) for k, v in row.items()})
                for row in csv.DictReader(file, delimiter=',', quotechar='"')]
