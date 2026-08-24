"""Plain dictionary records used by the Chapter 1 parser."""


def _two_terminal(name, element_type, positive_node, negative_node):
    return {
        "type": element_type,
        "name": name,
        "positive_node": positive_node,
        "negative_node": negative_node,
    }


def make_resistor(name, positive_node, negative_node, resistance, group2=False):
    element = _two_terminal(name, "R", positive_node, negative_node)
    element.update({"resistance": resistance, "group2": group2})
    return element


def make_voltage_source(name, positive_node, negative_node, voltage):
    element = _two_terminal(name, "V", positive_node, negative_node)
    element["voltage"] = voltage
    return element


def make_current_source(name, positive_node, negative_node, current, group2=False):
    element = _two_terminal(name, "I", positive_node, negative_node)
    element.update({"current": current, "group2": group2})
    return element


def make_voltmeter(name, positive_node, negative_node):
    return _two_terminal(name, "VM", positive_node, negative_node)


def make_ammeter(name, positive_node, negative_node):
    return _two_terminal(name, "AM", positive_node, negative_node)


def make_capacitor(name, positive_node, negative_node, capacitance, group2=False):
    element = _two_terminal(name, "C", positive_node, negative_node)
    element.update({"capacitance": capacitance, "group2": group2})
    return element


def make_inductor(name, positive_node, negative_node, inductance):
    element = _two_terminal(name, "L", positive_node, negative_node)
    element["inductance"] = inductance
    return element


def make_diode(name, positive_node, negative_node, scale=1.0):
    element = _two_terminal(name, "D", positive_node, negative_node)
    element["scale"] = scale
    return element


def make_three_terminal(name, element_type, first_node, second_node, third_node, scale=1.0):
    return {
        "type": element_type,
        "name": name,
        "first_node": first_node,
        "second_node": second_node,
        "third_node": third_node,
        "scale": scale,
    }
