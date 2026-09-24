"""Dense modified nodal analysis assembly for linear Chapter 2 circuits."""

import numpy as np


_SUPPORTED_TYPES = {"R", "V", "I", "C", "L"}


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


def _stamp_branch_constraint(matrix, rhs, node_indices, branch_index, positive_node, negative_node, voltage):
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
    """Assemble ``A @ x = b`` for static linear circuit records.

    Node voltages are indexed by ascending non-ground node number.  Additional
    unknowns are currents through voltage sources and inductors in circuit order.
    Capacitors are open circuits in this static/DC formulation.
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
    branch_elements = [element for element in circuit if element["type"] in {"V", "L"}]
    node_indices = {node: index for index, node in enumerate(nodes)}
    branch_indices = {
        element["name"]: len(nodes) + index
        for index, element in enumerate(branch_elements)
    }
    unknowns = [f"V({node})" for node in nodes]
    unknowns.extend(f"I({element['name']})" for element in branch_elements)

    size = len(unknowns) # Total number of unknowns (node voltages + voltage source currents)
    matrix = np.zeros((size, size), dtype=np.float64) # Coefficient matrix
    rhs = np.zeros(size, dtype=np.float64) # Right-hand side vector
    for element in circuit:
        positive_node = element["positive_node"]
        negative_node = element["negative_node"]
        if element["type"] == "R":
            if element["resistance"] == 0:
                raise ValueError(f"resistor {element['name']} must have non-zero resistance")
            _stamp_conductance(
                matrix, # Coefficient matrix
                node_indices,
                positive_node,
                negative_node,
                1.0 / element["resistance"], # Conductance is 1 / resistance
            )
        elif element["type"] == "I":
            _stamp_current(
                rhs, # Right-hand side vector
                node_indices, positive_node, negative_node, 
                element["current"] # Current value
            )
        elif element["type"] in {"V", "L"}:
            if positive_node == negative_node:
                raise ValueError(
                    f"{element['type']} element {element['name']} must connect two distinct nodes"
                )
            _stamp_branch_constraint(
                matrix, # Coefficient matrix
                rhs, # Right-hand side vector
                node_indices,
                branch_indices[element["name"]], # Index of the voltage source
                positive_node,
                negative_node,
                element.get("voltage", 0.0),
            )
        elif element["type"] == "C":
            # Capacitors have no DC conductance or branch constraint.
            continue

    return {
        "matrix": matrix,
        "rhs": rhs,
        "node_indices": node_indices,
        "branch_indices": branch_indices,
        "unknowns": unknowns,
    }