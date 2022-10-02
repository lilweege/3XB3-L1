import pytest
import os
import sys
FILE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(FILE_PATH, ".."))
from graphlib.builders import TubemapCSVBuilder  # noqa: E402
from graphlib.metrics import TubemapPatrolMetric  # noqa: E402


@pytest.fixture
def patrol_short_path():
    return ([1, 2, 3, 4, 5, 6, 7, 8],), [5, 1, 4, 3, 2, 7, 8, 6]


@pytest.fixture
def patrol_long_path():
    return ([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],), \
        [22, 10, 14, 16, 15, 21, 19, 20, 13, 12, 17, 18, 11]


@pytest.fixture
def all_cases(patrol_short_path, patrol_long_path):
    return [patrol_short_path, patrol_long_path]


def is_correct(output, expected_route):
    def rotated(lst, n): return lst[n:] + lst[:n]
    actual_route = [next(map(lambda e: e.fr, path)) for path in output]
    for i in range(len(expected_route)):
        if actual_route == rotated(expected_route, i):
            return True
    return False


def do_test(stations):
    tubemap_builder = TubemapCSVBuilder(
        os.path.join(FILE_PATH, "../_dataset/london.stations.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.connections.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.lines.csv")
    )
    tubemap_graph = tubemap_builder.build()
    return TubemapPatrolMetric(tubemap_graph, stations)()[1]


def test_patrol(all_cases):
    for case, expected in all_cases:
        results = do_test(*case)
        assert is_correct(results, expected)
