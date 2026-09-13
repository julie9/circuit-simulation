import numpy as np
import pytest

from circuit_sim.dc import (
    NewtonConvergenceError,
    assemble_dc,
    diode_current_and_conductance,
    solve_dc,
)
from circuit_sim.parser import parse_netlist


def test_diode_model_returns_current_and_jacobian():
    current, conductance = diode_current_and_conductance(0.0)

    assert current == pytest.approx(-1e-14)
    assert conductance == pytest.approx(1e-14 / 0.02585)


def test_diode_linearization_matches_tangent_near_operating_voltage():
    voltage = 0.6
    current, conductance = diode_current_and_conductance(voltage)
    nearby_current, _ = diode_current_and_conductance(voltage + 1e-8)

    assert nearby_current == pytest.approx(current + conductance * 1e-8, rel=1e-6)


def test_assemble_dc_contains_diode_companion_stamp():
    circuit = parse_netlist("R1 1 0 1000\nD1 1 0")
    system = assemble_dc(circuit, [0.6])

    current, conductance = diode_current_and_conductance(0.6)
    np.testing.assert_allclose(system["matrix"], [[0.001 + conductance]])
    np.testing.assert_allclose(system["rhs"], [-current + conductance * 0.6])


def test_solve_dc_finds_diode_resistor_operating_point():
    circuit = parse_netlist("V1 1 0 5\nR1 1 2 1000\nD1 2 0")

    result = solve_dc(circuit, residual_tolerance=1e-10)

    assert result["converged"] is True
    assert result["iterations"] < 100
    assert result["solution"][1] == pytest.approx(0.692, abs=0.01)
    assert result["residual_norm"] < 1e-10


def test_solve_dc_rejects_nonconvergence_limit():
    circuit = parse_netlist("V1 1 0 5\nR1 1 2 1000\nD1 2 0")

    with pytest.raises(NewtonConvergenceError):
        solve_dc(circuit, max_iterations=1)