from abc import ABC, abstractmethod


class GraphMetric(ABC):
    def __init__(self, graph):
        self.graph = graph

    @abstractmethod
    def __call__(self):
        '''Computes the metric as presrcibed by the derrived class'''
        pass
