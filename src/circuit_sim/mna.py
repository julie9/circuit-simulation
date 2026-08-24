"""Dense modified nodal analysis assembly for linear Chapter 2 circuits."""

import numpy as np


_SUPPORTED_TYPES = {"R", "V", "I"}


def _stamp_conductance(matrix, node_indices, positive_node, negative_node, conductance):
    """Stamp a two-terminal conductance, skipping ground rows and columns."""
    positive_index = node_indices.get(positive_node)
    negative_index = node_indices.get(negative_node)
    if positive_index is not None:
        matrix[positive_index, positive_index] += conductance
    if negative_index is not None:
        matrix[negative_index, negative_index] += conductance
    if positive_index is not None and negative_index is not None:
        matrix[positive_index, negative_index] -= conductance
        matrix[negative_index, positive_index] -= conductance


def _stamp_current(rhs, node_indices, positive_node, negative_node, current):
    """Stamp current flowing from the positive terminal to the negative terminal."""
    positive_index = node_indices.get(positive_node)
    negative_index = node_indices.get(negative_node)
    if positive_index is not None:
        rhs[positive_index] -= current
    if negative_index is not None:
        rhs[negative_index] += current


def _stamp_voltage_source(matrix, rhs, node_indices, branch_index, positive_node, negative_node, voltage):
    positive_index = node_indices.get(positive_node)
    negative_index = node_indices.get(negative_node)
    if positive_index is not None:
        matrix[positive_index, branch_index] += 1.0
        matrix[branch_index, positive_index] += 1.0
    if negative_index is not None:
        matrix[negative_index, branch_index] -= 1.0
        matrix[branch_index, negative_index] -= 1.0
    rhs[branch_index] += voltage


def assemble_mna(circuit):
    """Assemble ``A @ x = b`` for resistor, voltage-source, and current-source records.

    Node voltages are indexed by ascending non-ground node number.  Additional
    unknowns are currents through voltage sources in circuit order.
    """
    unsupported = [element["type"] for element in circuit if element["type"] not in _SUPPORTED_TYPES]
    if unsupported:
        types = ", ".join(sorted(set(unsupported)))
        raise ValueError(f"MNA assembly does not support element type(s): {types}")

    nodes = sorted({
        node
        for element in circuit
        for node in (element["positive_node"], element["negative_node"])
        if node != 0
    })
    voltage_sources = [element for element in circuit if element["type"] == "V"]
    node_indices = {node: index for index, node in enumerate(nodes)}
    branch_indices = {
        element["name"]: len(nodes) + index
        for index, element in enumerate(voltage_sources)
    }
    unknowns = [f"V({node})" for node in nodes]
    unknowns.extend(f"I({element['name']})" for element in voltage_sources)

    size = len(unknowns)
    matrix = np.zeros((size, size), dtype=np.float64)
    rhs = np.zeros(size, dtype=np.float64)
    for element in circuit:
        positive_node = element["positive_node"]
        negative_node = element["negative_node"]
        if element["type"] == "R":
            if element["resistance"] == 0:
                raise ValueError(f"resistor {element['name']} must have non-zero resistance")
            _stamp_conductance(
                matrix,
                node_indices,
                positive_node,
                negative_node,
                1.0 / element["resistance"],
            )
        elif element["type"] == "I":
            _stamp_current(rhs, node_indices, positive_node, negative_node, element["current"])
        else:
            _stamp_voltage_source(
                matrix,
                rhs,
                node_indices,
                branch_indices[element["name"]],
                positive_node,
                negative_node,
                element["voltage"],
            )

    return {
        "matrix": matrix,
        "rhs": rhs,
        "node_indices": node_indices,
        "branch_indices": branch_indices,
        "unknowns": unknowns,
    }