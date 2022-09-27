from abc import ABC, abstractmethod
from graphlib.graphs.bigraph import BiGraph


class BiGraphBuilder(ABC):
    '''A factory class for constructing graphs in a reusable fashion'''

    @abstractmethod
    def build(self, *args, **kwargs) -> BiGraph:
        '''Build a BiGraph from some input data, given in the constructor'''
        pass
