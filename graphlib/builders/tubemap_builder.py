from graphlib.builders.graph_builder import BiGraphBuilder
from graphlib.common.csv_reader import read_csv_contents
from graphlib.graphs.bigraph import BiGraph

class TubemapCSVBuilder(BiGraphBuilder):
    def build(self, stations_fn, connections_fn, lines_fn) -> BiGraph:
        self.stations = read_csv_contents(stations_fn)
        self.connections = read_csv_contents(connections_fn)
        self.lines = read_csv_contents(lines_fn)
        self.station_id_to_name = {}
        self.station_name_to_id = {}
        self.line_id_to_name = {}
        self.line_name_to_id = {}
        for line in self.lines:
            self.line_id_to_name[line.line] = line.name
            self.line_name_to_id[line.name] = line.line

        G = BiGraph()
        for station in self.stations:
            G.add_node(station.id, name=station.name, zone=station.zone, latitude=station.latitude, longitude=station.longitude)
            self.station_id_to_name[station.id] = station.name
            self.station_name_to_id[station.name] = station.id
        for connection in self.connections:
            G.add_edge(connection.station1, connection.station2, line=connection.line, time=connection.time)
        return G
