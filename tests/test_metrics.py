import pytest
import os
import sys
FILE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(FILE_PATH, ".."))
from graphlib.builders import TubemapCSVBuilder  # noqa: E402
from graphlib.metrics import NumberOfNodesMetric  # noqa: E402
from graphlib.metrics import NumberOfEdgesMetric  # noqa: E402
from graphlib.metrics import DegreeMetric  # noqa: E402


@pytest.fixture
def tubemap_nodes_metrics():
    return (), 302


@pytest.fixture
def tubemap_edges_metric():
    return (), 406


@pytest.fixture
def station1_degree_metric():
    return (1,), 5


@pytest.fixture
def station2_degree_metric():
    return (2,), 3


@pytest.fixture
def all_nodes_cases(tubemap_nodes_metrics):
    return [tubemap_nodes_metrics]


@pytest.fixture
def all_edges_cases(tubemap_edges_metric):
    return [tubemap_edges_metric]


@pytest.fixture
def all_degree_cases(station1_degree_metric, station2_degree_metric):
    return [station1_degree_metric, station2_degree_metric]


def build_tubemap():
    tubemap_builder = TubemapCSVBuilder(
        os.path.join(FILE_PATH, "../_dataset/london.stations.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.connections.csv"),
        os.path.join(FILE_PATH, "../_dataset/london.lines.csv")
    )
    return tubemap_builder.build()


def do_test_nodes():
    tubemap_graph = build_tubemap()
    return NumberOfNodesMetric(tubemap_graph)()


def do_test_edges():
    tubemap_graph = build_tubemap()
    return NumberOfEdgesMetric(tubemap_graph)()


def do_test_degree(station):
    tubemap_graph = build_tubemap()
    return DegreeMetric(tubemap_graph, station)()


def do_test_cases(do_test_func, cases):
    for case, expected in cases:
        result = do_test_func(*case)
        assert result == expected


def test_nodes_metrics(all_nodes_cases):
    do_test_cases(do_test_nodes, all_nodes_cases)


def test_edges_metrics(all_edges_cases):
    do_test_cases(do_test_edges, all_edges_cases)


def test_degree_metrics(all_degree_cases):
    do_test_cases(do_test_degree, all_degree_cases)
