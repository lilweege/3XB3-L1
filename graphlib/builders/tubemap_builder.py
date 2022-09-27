from graphlib.builders.graph_builder import BiGraphBuilder
from graphlib.common.csv_reader import read_csv_contents
from graphlib.graphs.bigraph import BiGraph


class TubemapCSVBuilder(BiGraphBuilder):
    def __init__(self, stations_fn, connections_fn, lines_fn):
        # Filenames of input CSV files
        self.stations_fn = stations_fn
        self.connections_fn = connections_fn
        self.lines_fn = lines_fn

    def build(self) -> BiGraph:
        # Open and read CSV files to build graph
        self.stations = read_csv_contents(self.stations_fn)
        self.connections = read_csv_contents(self.connections_fn)
        self.lines = read_csv_contents(self.lines_fn)

        # Associate names with ids to go alongside the graph
        # Useful for representative purposes
        self.station_id_to_name = {}
        self.station_name_to_id = {}
        self.line_id_to_name = {}
        self.line_name_to_id = {}
        for line in self.lines:
            self.line_id_to_name[line.line] = line.name
            self.line_name_to_id[line.name] = line.line

        # Construct and return the graph from data in CSV files
        G = BiGraph()
        for station in self.stations:
            G.add_node(
                station.id,
                name=station.name,
                zone=station.zone,
                latitude=station.latitude,
                longitude=station.longitude
            )
            self.station_id_to_name[station.id] = station.name
            self.station_name_to_id[station.name] = station.id
        for connection in self.connections:
            G.add_edge(
                connection.station1,
                connection.station2,
                line=connection.line,
                time=connection.time
            )
        return G
