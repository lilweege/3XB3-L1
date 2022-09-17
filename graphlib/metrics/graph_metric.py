from abc import ABC, abstractmethod

class GraphMetric(ABC):
    def __init__(self, graph):
        self.graph = graph
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
    def __call__(self, *args, **kwargs):
        '''Computes the metric as presrcibed by the derrived class'''
        pass
