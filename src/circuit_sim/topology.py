"""Graph and topological equation helpers for Chapter 2 circuits."""

import numpy as np


def _ordered_elements(circuit):
    """Validate two-terminal records and preserve circuit order."""
    elements = list(circuit)
    names = set()
    for element in elements:
        if not isinstance(element, dict):
            raise ValueError("topology records must be dictionaries")
        missing = {"name", "positive_node", "negative_node"} - element.keys()
        if missing:
            fields = ", ".join(sorted(missing))
            raise ValueError(f"topology record is missing field(s): {fields}")
        name = element["name"]
        if name in names:
            raise ValueError(f"duplicate topology element name {name!r}")
        names.add(name)
        positive_node = element["positive_node"]
        negative_node = element["negative_node"]
        if (
            not isinstance(positive_node, (int, np.integer))
            or not isinstance(negative_node, (int, np.integer))
            or positive_node < 0
            or negative_node < 0
        ):
            raise ValueError(f"topology element {name!r} has invalid node numbers")
        if positive_node == negative_node:
            raise ValueError(f"topology element {name!r} must connect two distinct nodes")
    return elements


def build_topology(circuit):
    """Build labels and the reduced incidence matrix for parser records.

    The matrix has shape ``(number of non-ground nodes, number of elements)``.
    Each column is oriented from ``positive_node`` to ``negative_node``:
    ``+1`` marks the positive/tail node and ``-1`` marks the negative/head
    node.  Ground is omitted.  Element columns follow circuit order.
    """
    elements = _ordered_elements(circuit)
    nodes = sorted({
        node
        for element in elements
        for node in (element["positive_node"], element["negative_node"])
        if node != 0
    })
    node_indices = {node: index for index, node in enumerate(nodes)}
    matrix = np.zeros((len(nodes), len(elements)), dtype=np.float64)
    for column, element in enumerate(elements):
        positive_index = node_indices.get(element["positive_node"])
        negative_index = node_indices.get(element["negative_node"])
        if positive_index is not None:
            matrix[positive_index, column] = 1.0
        if negative_index is not None:
            matrix[negative_index, column] = -1.0
    return {
        "matrix": matrix,
        "nodes": nodes,
        "elements": [element["name"] for element in elements],
    }


def reduced_incidence_matrix(circuit):
    """Return the float64 reduced incidence matrix ``A``."""
    return build_topology(circuit)["matrix"]


def kcl_residual(incidence, currents):
    """Return ``A @ i``; zero means the branch currents satisfy KCL."""
    matrix = np.asarray(incidence, dtype=np.float64)
    values = np.asarray(currents, dtype=np.float64)
    if matrix.ndim != 2 or values.ndim != 1 or matrix.shape[1] != values.size:
        raise ValueError("KCL requires a 2-D incidence matrix and one current per element")
    return matrix @ values


def kvl_branch_voltages(incidence, node_voltages):
    """Return branch voltages ``u = A.T @ v`` from non-ground node voltages."""
    matrix = np.asarray(incidence, dtype=np.float64)
    values = np.asarray(node_voltages, dtype=np.float64)
    if matrix.ndim != 2 or values.ndim != 1 or matrix.shape[0] != values.size:
        raise ValueError("KVL requires one node voltage per incidence-matrix row")
    return matrix.T @ values