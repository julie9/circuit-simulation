"""Educational nonlinear DC operating-point analysis."""

import numpy as np

from .mna import _stamp_branch_constraint, _stamp_conductance, _stamp_current
from .solver import solve_linear_system


_SUPPORTED_TYPES = {"R", "V", "I", "C", "L", "D"}
_DEFAULT_SATURATION_CURRENT = 1e-14
_DEFAULT_THERMAL_VOLTAGE = 0.02585
_MAX_EXPONENT = 40.0


class NewtonConvergenceError(RuntimeError):
    """Raised when a DC Newton iteration reaches its iteration limit."""


def diode_current_and_conductance(
    voltage,
    scale=1.0,
    saturation_current=_DEFAULT_SATURATION_CURRENT,
    thermal_voltage=_DEFAULT_THERMAL_VOLTAGE,
):
    """Return Shockley diode current and derivative at a terminal voltage."""
    if scale <= 0 or saturation_current <= 0 or thermal_voltage <= 0:
        raise ValueError("diode parameters must be positive")
    exponent = np.clip(voltage / thermal_voltage, -_MAX_EXPONENT, _MAX_EXPONENT)
    exponential = np.exp(exponent)
    current = scale * saturation_current * (exponential - 1.0)
    conductance = scale * saturation_current * exponential / thermal_voltage
    return float(current), float(conductance)


def _build_indices(circuit):
    unsupported = [element["type"] for element in circuit if element["type"] not in _SUPPORTED_TYPES]
    if unsupported:
        types = ", ".join(sorted(set(unsupported)))
        raise ValueError(f"DC analysis does not support element type(s): {types}")

    nodes = sorted({
        node
        for element in circuit
        for node in (element["positive_node"], element["negative_node"])
        if node != 0
    })
    branch_elements = [element for element in circuit if element["type"] in {"V", "L"}]
    node_indices = {node: index for index, node in enumerate(nodes)}
    branch_indices = {
        element["name"]: len(nodes) + index
        for index, element in enumerate(branch_elements)
    }
    unknowns = [f"V({node})" for node in nodes]
    unknowns.extend(f"I({element['name']})" for element in branch_elements)
    return node_indices, branch_indices, unknowns


def _node_voltage(solution, node_indices, node):
    index = node_indices.get(node)
    return 0.0 if index is None else solution[index]


def assemble_dc(circuit, iterate):
    """Assemble a Newton-linearized MNA system at a voltage iterate."""
    node_indices, branch_indices, unknowns = _build_indices(circuit)
    iterate = np.asarray(iterate, dtype=np.float64)
    if iterate.ndim != 1 or iterate.shape[0] != len(unknowns):
        raise ValueError(f"iterate must be a one-dimensional vector of length {len(unknowns)}")
    if not np.all(np.isfinite(iterate)):
        raise ValueError("iterate must contain only finite values")

    size = len(unknowns)
    matrix = np.zeros((size, size), dtype=np.float64)
    rhs = np.zeros(size, dtype=np.float64)
    for element in circuit:
        positive_node = element["positive_node"]
        negative_node = element["negative_node"]
        element_type = element["type"]
        if element_type == "R":
            if element["resistance"] == 0:
                raise ValueError(f"resistor {element['name']} must have non-zero resistance")
            _stamp_conductance(
                matrix,
                node_indices,
                positive_node,
                negative_node,
                1.0 / element["resistance"],
            )
        elif element_type == "I":
            _stamp_current(
                rhs,
                node_indices,
                positive_node,
                negative_node,
                element["current"],
            )
        elif element_type in {"V", "L"}:
            if positive_node == negative_node:
                raise ValueError(
                    f"{element_type} element {element['name']} must connect two distinct nodes"
                )
            _stamp_branch_constraint(
                matrix,
                rhs,
                node_indices,
                branch_indices[element["name"]],
                positive_node,
                negative_node,
                element.get("voltage", 0.0),
            )
        elif element_type == "D":
            voltage = (
                _node_voltage(iterate, node_indices, positive_node)
                - _node_voltage(iterate, node_indices, negative_node)
            )
            current, conductance = diode_current_and_conductance(
                voltage,
                scale=element["scale"],
            )
            _stamp_conductance(
                matrix,
                node_indices,
                positive_node,
                negative_node,
                conductance,
            )
            _stamp_current(
                rhs,
                node_indices,
                positive_node,
                negative_node,
                current - conductance * voltage,
            )
        elif element_type == "C":
            continue

    return {
        "matrix": matrix,
        "rhs": rhs,
        "node_indices": node_indices,
        "branch_indices": branch_indices,
        "unknowns": unknowns,
    }


def _dc_residual(circuit, solution, system):
    residual = np.zeros(len(system["unknowns"]), dtype=np.float64)
    node_indices = system["node_indices"]
    branch_indices = system["branch_indices"]
    for element in circuit:
        positive_node = element["positive_node"]
        negative_node = element["negative_node"]
        positive_index = node_indices.get(positive_node)
        negative_index = node_indices.get(negative_node)
        voltage = (
            _node_voltage(solution, node_indices, positive_node)
            - _node_voltage(solution, node_indices, negative_node)
        )
        if element["type"] == "R":
            current = voltage / element["resistance"]
        elif element["type"] == "I":
            current = element["current"]
        elif element["type"] == "D":
            current, _ = diode_current_and_conductance(voltage, element["scale"])
        elif element["type"] in {"C"}:
            continue
        elif element["type"] in {"V", "L"}:
            current = solution[branch_indices[element["name"]]]
            constraint = voltage - element.get("voltage", 0.0)
            residual[branch_indices[element["name"]]] += constraint
        else:
            continue
        if positive_index is not None:
            residual[positive_index] += current
        if negative_index is not None:
            residual[negative_index] -= current
    return residual


def solve_dc(
    circuit,
    initial_guess=None,
    max_iterations=100,
    voltage_tolerance=1e-9,
    residual_tolerance=1e-12,
    minimum_damping=1e-6,
):
    """Find a DC operating point using damped Newton iteration."""
    node_indices, branch_indices, unknowns = _build_indices(circuit)
    size = len(unknowns)
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if voltage_tolerance < 0 or residual_tolerance < 0 or not 0 < minimum_damping <= 1:
        raise ValueError(
            "Newton tolerances must be non-negative and minimum_damping must be in (0, 1]"
        )
    if initial_guess is None:
        solution = np.zeros(size, dtype=np.float64)
    else:
        solution = np.asarray(initial_guess, dtype=np.float64).copy()
        if solution.ndim != 1 or solution.shape[0] != size:
            raise ValueError(f"initial_guess must be a one-dimensional vector of length {size}")
        if not np.all(np.isfinite(solution)):
            raise ValueError("initial_guess must contain only finite values")

    for iteration in range(1, max_iterations + 1):
        system = assemble_dc(circuit, solution)
        linear_result = solve_linear_system(system["matrix"], system["rhs"])
        raw_candidate = linear_result["solution"]
        current_residual = _dc_residual(circuit, solution, system)
        current_norm = np.max(np.abs(current_residual), initial=0.0)
        damping = 1.0
        while damping > minimum_damping:
            candidate = solution + damping * (raw_candidate - solution)
            candidate_residual = _dc_residual(circuit, candidate, system)
            if np.max(np.abs(candidate_residual), initial=0.0) <= current_norm:
                break
            damping *= 0.5
        else:
            candidate = solution + minimum_damping * (raw_candidate - solution)
            candidate_residual = _dc_residual(circuit, candidate, system)
        residual = candidate_residual
        if (
            np.max(np.abs(candidate - solution), initial=0.0) <= voltage_tolerance
            and np.max(np.abs(residual), initial=0.0) <= residual_tolerance
        ):
            return {
                **system,
                "solution": candidate,
                "residual": residual,
                "residual_norm": np.linalg.norm(residual),
                "iterations": iteration,
                "converged": True,
            }
        solution = candidate

    raise NewtonConvergenceError(
        f"DC Newton iteration did not converge in {max_iterations} iterations"
    )