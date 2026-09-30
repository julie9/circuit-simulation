import numpy as np
import pytest

from circuit_sim.parser import parse_netlist
from circuit_sim.topology import (
    build_topology,
    kcl_residual,
    kvl_branch_voltages,
    reduced_incidence_matrix,
)


def test_reduced_incidence_preserves_element_order_and_removes_ground():
    circuit = parse_netlist("R2 2 0 2\nV1 1 2 5\nR1 1 0 1")

    topology = build_topology(circuit)

    assert topology["nodes"] == [1, 2]
    assert topology["elements"] == ["R2", "V1", "R1"]
    assert topology["matrix"].dtype == np.float64
    np.testing.assert_array_equal(topology["matrix"], [
        [0.0, 1.0, 1.0],
        [1.0, -1.0, 0.0],
    ])


def test_kcl_and_kvl_helpers_match_topological_equations():
    incidence = reduced_incidence_matrix(parse_netlist("R1 1 0 1\nR2 1 2 1\nR3 2 0 1"))

    np.testing.assert_allclose(kcl_residual(incidence, [1.0, -1.0, -1.0]), [0.0, 0.0])
    np.testing.assert_allclose(kvl_branch_voltages(incidence, [5.0, 2.0]), [5.0, 3.0, 2.0])


@pytest.mark.parametrize("circuit", [
    [{"name": "R1", "positive_node": 1}],
    [{"name": "R1", "positive_node": 1, "negative_node": 1}],
    [{"name": "R1", "positive_node": -1, "negative_node": 0}],
])
def test_topology_rejects_malformed_or_self_loop_records(circuit):
    with pytest.raises(ValueError):
        reduced_incidence_matrix(circuit)


def test_topological_helpers_reject_wrong_vector_dimensions():
    incidence = np.zeros((2, 3), dtype=np.float64)

    with pytest.raises(ValueError, match="one current per element"):
        kcl_residual(incidence, [1.0, 2.0])
    with pytest.raises(ValueError, match="one node voltage per"):
        kvl_branch_voltages(incidence, [1.0])