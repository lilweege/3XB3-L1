from graphlib.common.priority_queue import PriorityQueue

class Itinerary:
    def __init__(self, u, v):
        self.station1 = u
        self.station2 = v
        self.search_strategy = None

    def set_search_strategy(self, strategy):
        self.search_strategy = strategy

    def shortest_path(self, time_weight=1, conn_weight=1, transfer_weight=1):
        if time_weight < 0: raise ValueError(f"time_weight must be non-negative, got {time_weight}")
        if conn_weight < 0: raise ValueError(f"conn_weight must be non-negative, got {conn_weight}")
        if transfer_weight < 0: raise ValueError(f"transfer_weight must be non-negative, got {transfer_weight}")
        if self.search_strategy is None: raise ValueError("No search stategy defined")

        weight = lambda prev_edge, curr_edge: (
            time_weight * curr_edge.time +
            conn_weight +
            transfer_weight * bool(prev_edge and (curr_edge.line != prev_edge.line))
        )

        path = self.search_strategy(self.station1, self.station2, weight)
        return path
