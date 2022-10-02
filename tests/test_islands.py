import pytest
import os
import sys
FILE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(FILE_PATH, ".."))
from graphlib.metrics import TubemapIslandMetric  # noqa: E402
from graphlib.builders import TubemapCSVBuilder  # noqa: E402


@pytest.fixture
def island1_expected_output():
    return (), [10, 95, 123, 128, 39]


@pytest.fixture
def island2_expected_output():
    return (), [96, 195, 205, 287]


@pytest.fixture
def all_cases(island1_expected_output, island2_expected_output):
    return [island1_expected_output, island2_expected_output]


def has_island(output, expected_island):
    components = output[0]
    return any(expected_island == island for island in components.values())


def build_tubemap():
    tubemap_builder = TubemapCSVBuilder(
        os.path.join(FILE_PATH, "../_dataset/london.stations.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.connections.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.lines.csv")
    )
    return tubemap_builder.build()


def do_test():
    tubemap_graph = build_tubemap()
    return TubemapIslandMetric(tubemap_graph)()


def test_islands(all_cases):
    for case, expected in all_cases:
        result = do_test(*case)
        assert has_island(result, expected)
