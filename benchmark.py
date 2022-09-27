import pyperf
from functools import partial
from dataclasses import dataclass
from typing import Callable, Optional

from graphlib.metrics.paths import PathMetric

import re
def normalize_name(s: str):
    return re.sub("\s+", "_", s.strip())

@dataclass
class TestCase:
    name: str
    metric: Optional[PathMetric]
    func: Callable
    args: tuple = ()

def london_tubemap_cases() -> list[TestCase]:
    from graphlib.builders import TubemapCSVBuilder
    from graphlib.metrics import TubemapItinerary
    # from graphlib.metrics.paths import DijkstraShortestPathMetric, EuclidianDistancePathMetric
    from graphlib.metrics.paths import DijkstraShortestPathMetric, CircularDistancePathMetric

    tubemap_builder = TubemapCSVBuilder()
    tubemap_graph = tubemap_builder.build("_dataset/london.stations.csv", "_dataset/london.connections.csv", "_dataset/london.lines.csv")

    itineraries = [
        ("Picadilly Circus", "St. Paul's"), # Typical short case
        ("Hammersmith", "Stratford"),       # Longer path through center
        ("Ealing Broadway", "Upminster")    # Longest possible path without transfering
    ]
    edge_weightings = [
        (1, 1, 1),   # Typical case default weightings
        (1, 0, 0),   # Prioritize time only
        (1, 1, 100), # Deprioritize line transfers
    ]
    path_algorithms = [
        ("Dijkstra", DijkstraShortestPathMetric(tubemap_graph)),
        # ("A*", EuclidianDistancePathMetric(tubemap_graph)),
        ("A*", CircularDistancePathMetric(tubemap_graph)),
    ]

    cases = []
    for start_station, end_station in itineraries:
        u = tubemap_builder.station_name_to_id[start_station]
        v = tubemap_builder.station_name_to_id[end_station]
        for edge_weighting in edge_weightings:
            for search_name, search_metric in path_algorithms:
                itinerary = TubemapItinerary(u, v)
                itinerary.set_search_strategy(search_metric)
                case_name = f"{search_name}-{'-'.join(map(str, edge_weighting))}-{normalize_name(start_station)}-{normalize_name(end_station)}"
                case_func = partial(itinerary.shortest_path, *edge_weighting)
                cases.append(TestCase(case_name, search_metric, case_func))

    return cases


def main():
    runner = pyperf.Runner()
    for case in london_tubemap_cases():
        runner.bench_func(case.name, case.func, *case.args)

if __name__ == "__main__":
    main()
