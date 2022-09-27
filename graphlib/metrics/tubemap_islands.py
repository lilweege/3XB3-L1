from graphlib.metrics.graph_metric import GraphMetric
from collections import defaultdict


class TubemapIslandMetric(GraphMetric):
    '''
    Computes "traffic islands" in a BiGraph representing a Tubemap
    NOTE: Each Node (Station) in a Tubemap should have a "zone" attribute
    '''

    def __call__(self):
        '''
        For each component "representitive node", store a list of components.
        For each node, store its representitive node (this is similar
        to union find)
        This representation is useful for computing connected components
        '''
        rep_node = {}
        components = defaultdict(list)

        def dfs(start, u):
            if u in rep_node:
                return
            rep_node[u] = start
            components[start].append(u)
            for edge in self.graph.adj[u].edges:
                fr_zone = self.graph.adj[edge.fr].zone
                to_zone = self.graph.adj[edge.to].zone
                if fr_zone == to_zone:
                    dfs(start, edge.to)

        '''
        Perform depth first search starting at every node if it hasn't
        been visited yet. This will traverse the entire forest of
        disconnected components. The starting node for each dfs is the
        representitive node of that component
        '''
        for start in self.graph.adj.keys():
            dfs(start, start)

        # Add every edge that crosses between zones.
        # These can be used when building a kernel graph
        zone_edges = []
        for node in self.graph.adj.values():
            for edge in node.edges:
                if edge.fr < edge.to:
                    fr_zone = self.graph.adj[edge.fr].zone
                    to_zone = self.graph.adj[edge.to].zone
                    if fr_zone != to_zone:
                        zone_edges.append(edge)

        return components, rep_node, zone_edges
