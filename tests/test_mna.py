import numpy as np
import pytest

from circuit_sim.mna import assemble_mna
from circuit_sim.parser import parse_netlist


def test_assemble_voltage_resistor_current_source_circuit():
    circuit = parse_netlist("V1 1 0 5\nR1 1 2 1000\nR2 2 0 2000\nI1 2 0 0.001")

    system = assemble_mna(circuit)

    assert system["node_indices"] == {1: 0, 2: 1}
    assert system["branch_indices"] == {"V1": 2}
    assert system["unknowns"] == ["V(1)", "V(2)", "I(V1)"]
    np.testing.assert_allclose(system["matrix"], [
        [0.001, -0.001, 1.0],
        [-0.001, 0.0015, 0.0],
        [1.0, 0.0, 0.0],
    ])
    np.testing.assert_allclose(system["rhs"], [0.0, -0.001, 5.0])


def test_current_source_direction_and_ground_stamps():
    system = assemble_mna(parse_netlist("I1 1 0 2"))

    np.testing.assert_allclose(system["matrix"], np.zeros((1, 1)))
    np.testing.assert_allclose(system["rhs"], [-2.0])


def test_unsupported_records_are_rejected_until_their_stamps_exist():
    with pytest.raises(ValueError, match=r"does not support element type\(s\): C"):
        assemble_mna(parse_netlist("C1 1 0 1e-6"))