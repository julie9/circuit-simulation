"""Deterministic layout for small textbook circuits."""


def _terminal_nodes(element):
    return [node for key, node in element.items() if key.endswith("_node")]


def _book_layout(circuit, grid, origin):
    left, top = origin
    ground_y = top + grid * 3
    node_positions = {1: (left, top), 2: (left + grid * 3, top), 0: (left, ground_y)}
    elements = {}
    branch_index = 0
    for element in circuit:
        name = element["name"]
        nodes = _terminal_nodes(element)
        if element["type"] == "V" and nodes == [1, 0]:
            center = (left, top + grid * 1.5)
            endpoints = [(left, top + grid), (left, top + grid * 2)]
            orientation = "vertical"
        elif element["type"] in {"R", "C", "L", "AM"} and nodes == [1, 2]:
            center = (left + grid * 1.5, top)
            endpoints = [(left + grid, top), (left + grid * 2, top)]
            orientation = "horizontal"
        elif len(nodes) == 2 and nodes[1] == 0:
            branch_x = left + grid * (2.5 + branch_index)
            branch_index += 1
            center = (branch_x, top + grid * 1.5)
            endpoints = [(branch_x, top + grid), (branch_x, top + grid * 2)]
            orientation = "vertical"
        else:
            center = (left + grid * (branch_index + 1), top + grid * 4)
            endpoints = [center for _ in nodes]
            orientation = "horizontal"
        elements[name] = {"x": center[0], "y": center[1], "orientation": orientation, "terminals": endpoints}
    return {"nodes": node_positions, "elements": elements, "ground_rail_y": ground_y}


def make_layout(circuit, grid=80, origin=(100, 100)):
    """Return stable positions and drawable terminal endpoints."""
    nodes = sorted({node for element in circuit for node in _terminal_nodes(element)})
    if {0, 1, 2}.issubset(nodes):
        return _book_layout(circuit, grid, origin)

    node_positions = {node: (origin[0] + index * grid, origin[1]) for index, node in enumerate(nodes) if node != 0}
    node_positions[0] = (origin[0], origin[1] + grid * 2)
    elements = {}
    for index, element in enumerate(circuit):
        element_nodes = _terminal_nodes(element)
        first, second = (element_nodes + [0, 0])[:2]
        center = (origin[0] + (index % 4) * grid, origin[1] + (index // 4 + 1) * grid)
        elements[element["name"]] = {
            "x": center[0], "y": center[1],
            "orientation": "horizontal" if first != 0 and second != 0 else "vertical",
            "terminals": [center for _ in element_nodes],
        }
    return {"nodes": node_positions, "elements": elements, "ground_rail_y": node_positions[0][1]}
