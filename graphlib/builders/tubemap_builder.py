from graphlib.builders.graph_builder import BiGraphBuilder
from graphlib.common.csv_reader import read_csv_contents
from graphlib.graphs.bigraph import BiGraph

class TubemapCSVBuilder(BiGraphBuilder):
    def build(self, stations_filename, connections_fliename, lines_filename) -> BiGraph:
        self.stations = read_csv_contents(stations_filename)
        self.connections = read_csv_contents(connections_fliename)
        self.lines = read_csv_contents(lines_filename)

        G = BiGraph()
        for station in self.stations:
            G.add_node(station.id, name=station.name, zone=station.zone, latitude=station.latitude, longitude=station.longitude)
        for connection in self.connections:
            G.add_edge(connection.station1, connection.station2, line=connection.line, time=connection.time)
        return G
