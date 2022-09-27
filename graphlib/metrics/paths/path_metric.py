from abc import abstractmethod
from graphlib.metrics.graph_metric import GraphMetric


class PathMetric(GraphMetric):
    def __init__(self, graph):
        super().__init__(graph)
        self.reset_counters()

    def reset_counters(self):
        self._edges_counter = 0
        self._nodes_counter = 0
        self._relaxation_counter = 0

    def increment_edges_counter(self):
        self._edges_counter += 1

    def increment_nodes_counter(self):
        self._nodes_counter += 1

    def increment_relaxation_counter(self):
        self._relaxation_counter += 1

    @abstractmethod
    def __call__(self, fr, to, weight_func):
        pass
