class TubemapItinerary:
    '''
    Computes the shortest path between two stations in a BiGraph
    NOTE: Each Edge (Connection) in a Tubemap should have a "time" and
    "line" attribute
    '''

    def __init__(self, u, v):
        self.station1 = u
        self.station2 = v
        self.search_strategy = None

    def set_search_strategy(self, strategy):
        # Use the strategy pattern to store a callable (PathMetric)
        # and call back to it when computing the shortest path
        self.search_strategy = strategy

    def shortest_path(self, time_weight=1, conn_weight=0, transfer_weight=0):
        if time_weight < 0:
            raise ValueError(
                f"time_weight must be non-negative, got {time_weight}"
            )
        if conn_weight < 0:
            raise ValueError(
                f"conn_weight must be non-negative, got {conn_weight}"
            )
        if transfer_weight < 0:
            raise ValueError(
                f"transfer_weight must be non-negative, got {transfer_weight}"
            )
        if self.search_strategy is None:
            raise ValueError("No search stategy defined")

        # Combine weights into a single weight function
        # Each connection is evaluated by this function

        def weight(prev_edge, curr_edge):
            time_value = time_weight * curr_edge.time
            conn_value = conn_weight
            did_trans = bool(prev_edge and (curr_edge.line != prev_edge.line))
            trans_value = transfer_weight * did_trans
            return time_value + conn_value + trans_value
        path = self.search_strategy(self.station1, self.station2, weight)
        return path
