from graphlib.builders.graph_builder import BiGraphBuilder
from graphlib.common.csv_reader import read_csv_contents
from graphlib.graphs.bigraph import BiGraph

class TubemapCSVBuilder(BiGraphBuilder):
    def build(self, stations_fn, connections_fn, lines_fn) -> BiGraph:
        self.stations = read_csv_contents(stations_fn)
        self.connections = read_csv_contents(connections_fn)
        self.lines = read_csv_contents(lines_fn)
        self.id_to_name = {}
        self.name_to_id = {}

        G = BiGraph()
        for station in self.stations:
            G.add_node(station.id, name=station.name, zone=station.zone, latitude=station.latitude, longitude=station.longitude)
            self.id_to_name[station.id] = station.name
            self.name_to_id[station.name] = station.id
        for connection in self.connections:
            G.add_edge(connection.station1, connection.station2, line=connection.line, time=connection.time)
        return G
