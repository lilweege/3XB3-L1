import pyperf
from functools import partial
from dataclasses import dataclass
from typing import Callable, Optional

from graphlib.metrics.paths import PathMetric

import re


def normalize_name(s: str):
    return re.sub(r"\s+", "_", s.strip())


@dataclass
class TestCase:
    name: str
    metric: Optional[PathMetric]
    func: Callable
    args: tuple = ()


def london_tubemap_cases() -> list[TestCase]:
    from graphlib.builders import TubemapCSVBuilder
    from graphlib.metrics import TubemapItinerary
    from graphlib.metrics.paths import DijkstraShortestPathMetric
    from graphlib.metrics.paths import CircularDistancePathMetric

    tubemap_builder = TubemapCSVBuilder(
        "_dataset/london.stations.csv",
        "_dataset/london.connections.csv",
        "_dataset/london.lines.csv"
    )
    tubemap_graph = tubemap_builder.build()

    itineraries = [
        # Typical short case
        ("Picadilly Circus", "St. Paul's"),
        # Longer path through center
        ("Hammersmith", "Stratford"),
        # Longest possible path without transfering
        ("Ealing Broadway", "Upminster")
    ]
    edge_weightings = [
        (1, 1, 1),    # Typical case default weightings
        (1, 0, 0),    # Prioritize time only
        (1, 1, 100),  # Deprioritize line transfers
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

                weightings_str = '-'.join(map(str, edge_weighting))
                algorithm_str = f"{search_name}-{weightings_str}"
                start_str = normalize_name(start_station)
                end_str = normalize_name(end_station)
                itinerary_str = f"{start_str}-{end_str}"
                case_name = f"{algorithm_str}-{itinerary_str}"

                case_func = partial(itinerary.shortest_path, *edge_weighting)
                cases.append(TestCase(case_name, search_metric, case_func))

    return cases


def main():
    runner = pyperf.Runner()
    for case in london_tubemap_cases():
        runner.bench_func(case.name, case.func, *case.args)


if __name__ == "__main__":
    main()
