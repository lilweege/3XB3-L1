from priority_queue import PriorityQueue
import math

class Itinerary:
    def __init__(self, u, v):
        self.station1 = u
        self.station2 = v
        self.search_strategy = None

    def set_search_strategy(self, strategy):
        self.search_strategy = strategy

    def shortest_path(self, timeWeight=1, connWeight=1, transferWeight=1):
        if timeWeight < 0: raise ValueError(f"timeWeight must be non-negative, got {timeWeight}")
        if connWeight < 0: raise ValueError(f"connWeight must be non-negative, got {connWeight}")
        if transferWeight < 0: raise ValueError(f"transferWeight must be non-negative, got {transferWeight}")
        if self.search_strategy is None: raise ValueError("No search stategy defined")

        weight = lambda edge, prevLine: (
            timeWeight * edge.time +
            connWeight +
            transferWeight * (edge.line != prevLine)
        )

        path = self.search_strategy(self.station1, self.station2, weight)
        return path

class GraphMetrics:
    def __init__(self, graph):
        self.graph = graph

    def astar(self, fr, to, weightFunc):
        def eucl_dist(x1, y1, x2, y2):
            return math.sqrt((x2-x1)**2+(y2-y1)**2)
        def heuristic(u):
            currNode = self.graph.adj[u]
            endNode = self.graph.adj[to]
            dist = eucl_dist(currNode.latitude, currNode.longitude, endNode.latitude, endNode.longitude)
            return dist
        num = 0

        N = len(self.graph.adj)
        dist = [1e99] * N
        edge = [None] * N
        dist[fr] = 0
        pq = PriorityQueue()
        pq.push((dist[fr], fr, -1))
        while pq:
            w, u, prevLine = pq.pop()
            if u == to:
                break
            num += 1
            for v in self.graph.adj[u].edges:
                vw = w + weightFunc(v, prevLine) + heuristic(u)
                if dist[v.to] > vw:
                    dist[v.to] = vw
                    edge[v.to] = u
                    pq.push((vw, v.to, v.line))
        # print(num)
        path = []
        while to != fr:
            path.append(to)
            to = edge[to]
        path.append(to)
        return path[::-1]

    def dijkstras(self, fr, to, weightFunc):
        num = 0
        N = len(self.graph.adj)
        dist = [1e99] * N
        edge = [None] * N
        dist[fr] = 0
        pq = PriorityQueue()
        pq.push((dist[fr], fr, -1))
        while pq:
            w, u, prevLine = pq.pop()
            if u == to:
                break
            num += 1
            for v in self.graph.adj[u].edges:
                vw = w + weightFunc(v, prevLine)
                if dist[v.to] > vw:
                    dist[v.to] = vw
                    edge[v.to] = u
                    pq.push((vw, v.to, v.line))
        path = []
        while to != fr:
            path.append(to)
            to = edge[to]
        path.append(to)
        # print(num)
        return path[::-1]

    def degree(self, u):
        return len(self.graph.adj[u].edges)

    def num_nodes(self):
        return len(self.graph.adj)
    
    def num_edges(self):
        return self.graph.edges

    def number_of_lines(self, uu):
        vis = set()
        lines_of_uu = set()
        for root in list(self.graph.adj.keys()):
            q = deque()
            q.append(root)
            while len(q) != 0:
                u = q.pop()
                if u in vis:
                    continue
                vis.add(u)
                for v in self.graph.adj[u].edges:
                    if u == uu:
                        lines_of_uu.add(v.line)
                    q.append(v.to)
        return len(lines_of_uu)
