from graphlib.metrics.graph_metric import GraphMetric
from graphlib.graphs.bigraph import BiGraph
from graphlib.common.graph_utils import reconstruct_path
from collections import defaultdict

class TubemapIslandMetric(GraphMetric):
    def __call__(self):
        augmented_G = BiGraph()
        for node in self.graph.adj.values():
            augmented_G.add_node(node.id, **{ k: node.__dict__[k] for k in node.__dict__.keys() - set(["id", "edges"]) })

        zone_edges = []
        for node in self.graph.adj.values():
            for edge in node.edges:
                if edge.fr < edge.to:
                    if self.graph.adj[edge.fr].zone == self.graph.adj[edge.to].zone:
                        augmented_G.add_edge(edge.fr, edge.to, **edge.__dict__)
                    else:
                        zone_edges.append(edge)

        rep_node = {}
        components = defaultdict(list)

        def DFS(u, start):
            if u in rep_node: return
            rep_node[u] = start
            components[start].append(u)
            for edge in augmented_G.adj[u].edges:
                v = edge.to
                DFS(v, start)

        for start in augmented_G.adj.keys():
            DFS(start, start)

        return components
