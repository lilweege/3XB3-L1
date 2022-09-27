class BiGraph:
    '''
    Representation of a bidirectional graph using an adjacency map

    In both Edge and Node classes, consume **kwargs so that the user can store
    arbitrary values in each class by passing keyword arguents to the graph
    methods
    '''
    class Edge:
        def __init__(self, u, v, **kwargs):
            self.fr = u
            self.to = v
            self.__dict__ |= kwargs

    class Node:
        def __init__(self, id, **kwargs):
            self.id = id
            self.edges = []
            self.__dict__ |= kwargs

    def __init__(self):
        # 'adj' maps from node id to a Node object
        self.adj = {}
        self.edges = 0

    def add_node(self, u, **kwargs):
        self.adj[u] = self.Node(u, **kwargs)

    def add_edge(self, u, v, **kwargs):
        self.adj[u].edges.append(self.Edge(u, v, **kwargs))
        self.adj[v].edges.append(self.Edge(v, u, **kwargs))
        self.edges += 1
