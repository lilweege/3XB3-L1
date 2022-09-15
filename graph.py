
class Edge:
    def __init__(self, v, **kwargs):
        self.to = v
        for k, v in kwargs.items():
            self.__dict__[k] = v

class Node:
    def __init__(self, id, **kwargs):
        self.id = id
        self.edges = []
        for k, v in kwargs.items():
            self.__dict__[k] = v


class BiGraph:
    def __init__(self, N):
        self.adj = [Node(i) for i in range(N)]
        self.edges = 0
    def add_node(self, u, **kwargs):
        self.adj[u] = Node(u, **kwargs)
    def add_edge(self, u, v, **kwargs):
        self.adj[u].edges.append(Edge(v, **kwargs))
        self.adj[v].edges.append(Edge(u, **kwargs))
        self.edges += 1
