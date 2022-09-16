from abc import ABC, abstractmethod
from graphlib.bigraph import BiGraph

class BiGraphBuilder(ABC):
    @abstractmethod
    def build(self, *args, **kwargs) -> BiGraph:
        '''Build a BiGraph from some input data'''
        pass
