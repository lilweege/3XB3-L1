import pytest
import os
import sys
FILE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(FILE_PATH, ".."))

from graphlib.builders import TubemapCSVBuilder  # noqa: E402
from graphlib.metrics import TubemapItinerary  # noqa: E402
from graphlib.metrics.paths import DijkstraShortestPathMetric  # noqa: E402
from graphlib.metrics.paths import AStarPathMetric  # noqa: E402


@pytest.fixture
def short_path():
    return (197, 250), [197, 151, 60, 126, 48, 250]


@pytest.fixture
def long_path():
    return (110, 247), [110, 17, 74, 99, 236, 229, 273, 248, 285, 279, 13, 156,
                        24, 164, 247]


@pytest.fixture
def all_cases(short_path, long_path):
    """Using fixture composition to bring all the cases together"""
    return [short_path, long_path]


def is_correct_path(output, expected_path):
    actual_path = list(map(lambda e: e.fr, output)) + [output[-1].to]
    return actual_path == expected_path


def do_test(algo_name, source, destination):
    tubemap_builder = TubemapCSVBuilder(
        os.path.join(FILE_PATH, "../_dataset/london.stations.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.connections.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.lines.csv")
    )
    tubemap_graph = tubemap_builder.build()
    itinerary = TubemapItinerary(source, destination)
    if algo_name == "Dijkstra":
        itinerary.set_search_strategy(
            DijkstraShortestPathMetric(tubemap_graph))
    elif algo_name == "AStar":
        itinerary.set_search_strategy(AStarPathMetric(tubemap_graph))
    return itinerary.shortest_path()


@pytest.mark.parametrize("metric_name", ["Dijkstra", "AStar"])
def test_pathfinding(metric_name, all_cases):
    for case, expected in all_cases:
        results = do_test(metric_name, *case)
        assert is_correct_path(results, expected)
