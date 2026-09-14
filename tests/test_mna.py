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


def test_capacitor_is_open_circuit_in_static_mna():
    system = assemble_mna(parse_netlist("C1 1 0 1e-6"))

    assert system["unknowns"] == ["V(1)"]
    assert system["matrix"].dtype == np.float64
    np.testing.assert_allclose(system["matrix"], [[0.0]])
    np.testing.assert_allclose(system["rhs"], [0.0])


def test_inductor_adds_zero_voltage_branch_constraint():
    system = assemble_mna(parse_netlist("L1 1 0 2e-3"))

    assert system["branch_indices"] == {"L1": 1}
    assert system["unknowns"] == ["V(1)", "I(L1)"]
    np.testing.assert_allclose(system["matrix"], [[0.0, 1.0], [1.0, 0.0]])
    np.testing.assert_allclose(system["rhs"], [0.0, 0.0])


def test_mixed_voltage_source_and_inductor_branch_order_follows_circuit():
    system = assemble_mna(parse_netlist("L1 2 0 1e-3\nV1 1 2 5"))

    assert system["branch_indices"] == {"L1": 2, "V1": 3}
    assert system["unknowns"] == ["V(1)", "V(2)", "I(L1)", "I(V1)"]
    np.testing.assert_allclose(system["matrix"], [
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, -1.0],
        [0.0, 1.0, 0.0, 0.0],
        [1.0, -1.0, 0.0, 0.0],
    ])
    np.testing.assert_allclose(system["rhs"], [0.0, 0.0, 0.0, 5.0])


@pytest.mark.parametrize("element_type", ["VM", "AM", "D", "QN"])
def test_display_and_semiconductor_records_are_rejected(element_type):
    netlist = {
        "VM": "VM1 1 0",
        "AM": "AM1 1 0",
        "D": "D1 1 0",
        "QN": "QN1 1 2 0",
    }[element_type]

    with pytest.raises(ValueError, match=rf"does not support element type\(s\): {element_type}"):
        assemble_mna(parse_netlist(netlist))


def test_complete_static_linear_fixture_matches_hand_assembled_system():
    circuit = parse_netlist("""V1 1 0 5
R1 1 2 1000
R2 2 0 2000
I1 2 0 0.001
C1 2 0 1e-6
L1 3 0 1e-3
""")

    system = assemble_mna(circuit)

    assert system["unknowns"] == ["V(1)", "V(2)", "V(3)", "I(V1)", "I(L1)"]
    np.testing.assert_allclose(system["matrix"], [
        [0.001, -0.001, 0.0, 1.0, 0.0],
        [-0.001, 0.0015, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
    ])
    np.testing.assert_allclose(system["rhs"], [0.0, -0.001, 0.0, 5.0, 0.0])