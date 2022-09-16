from graphlib.csv_reader import read_csv_contents
from graphlib.bigraph import BiGraph

def build_graph_from_csvs(filename_prefix):
    stations = read_csv_contents(f"{filename_prefix}.stations.csv")
    connections = read_csv_contents(f"{filename_prefix}.connections.csv")
    lines = read_csv_contents(f"{filename_prefix}.lines.csv")

    G = BiGraph()
    for station in stations:
        G.add_node(station.id, name=station.name, zone=station.zone, latitude=station.latitude, longitude=station.longitude)
    for connection in connections:
        u, v, l, t = connection.station1, connection.station2, connection.line, connection.time
        G.add_edge(u, v, line=l, time=t)

    return G