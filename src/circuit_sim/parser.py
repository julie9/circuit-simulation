"""Parser for the restricted Chapter 1 netlist language."""

from pathlib import Path
import math
import re

from .elements import (
    make_capacitor,
    make_current_source,
    make_ammeter,
    make_diode,
    make_inductor,
    make_resistor,
    make_three_terminal,
    make_voltage_source,
    make_voltmeter,
)

_NAME_PATTERN = re.compile(r"(VM|AM|QN|QP|MN|MP|V|I|R|C|L|D)([0-9]+)$", re.IGNORECASE)


class NetlistError(ValueError):
    """A netlist error with its source line number."""

    def __init__(self, line_number, message):
        super().__init__(f"line {line_number}: {message}")
        self.line_number = line_number
        self.message = message


def remove_comment(line):
    """Remove the comment beginning with '%' from a netlist line."""
    return line.split("%", 1)[0].strip()


def _error(line_number, message):
    raise NetlistError(line_number, message)


def _node(token, line_number):
    """Validate a node number; node 0 is the circuit ground."""
    if not token.isascii() or not token.isdecimal():
        _error(line_number, f"node must be a non-negative integer, got {token!r}")
    return int(token)


def _value(token, label, line_number, allow_zero=True):
    try:
        value = float(token)
    except ValueError:
        _error(line_number, f"{label} must be a real number, got {token!r}")
    if not math.isfinite(value) or (not allow_zero and value <= 0) or (allow_zero and value < 0):
        requirement = "finite and positive" if not allow_zero else "finite and non-negative"
        _error(line_number, f"{label} must be {requirement}, got {token!r}")
    return value


def _name(token, line_number):
    match = _NAME_PATTERN.fullmatch(token.upper())
    if match is None:
        _error(line_number, f"invalid element name {token!r}")
    return match.group(0), match.group(1).upper()


def _two_terminal(tokens, line_number, element_type, factory, value_label, optional_group2=False):
    expected = 4
    valid_lengths = {expected, expected + 1} if optional_group2 else {expected}
    if len(tokens) not in valid_lengths:
        if optional_group2:
            message = f"{element_type} record expects {expected} or {expected + 1} fields"
        else:
            message = f"{element_type} record expects {expected} fields"
        _error(line_number, message)
    name, _ = _name(tokens[0], line_number)
    positive_node = _node(tokens[1], line_number)
    negative_node = _node(tokens[2], line_number)
    value = _value(tokens[3], value_label, line_number)
    group2 = False
    if optional_group2 and len(tokens) == 5:
        if tokens[4].upper() != "G2":
            _error(line_number, "optional fourth field must be G2")
        group2 = True
    return factory(name, positive_node, negative_node, value, group2=group2) if optional_group2 else factory(name, positive_node, negative_node, value)


def parse_line(line, line_number):
    code = remove_comment(line)
    if not code:
        return None
    tokens = code.split()
    name, element_type = _name(tokens[0], line_number)
    if element_type == "V":
        return _two_terminal(tokens, line_number, "V", make_voltage_source, "voltage")
    if element_type == "VM":
        if len(tokens) != 3:
            _error(line_number, "VM record expects 3 fields")
        return make_voltmeter(name, _node(tokens[1], line_number), _node(tokens[2], line_number))
    if element_type == "AM":
        if len(tokens) != 3:
            _error(line_number, "AM record expects 3 fields")
        return make_ammeter(name, _node(tokens[1], line_number), _node(tokens[2], line_number))
    if element_type == "I":
        return _two_terminal(tokens, line_number, "I", make_current_source, "current", True)
    if element_type == "R":
        return _two_terminal(tokens, line_number, "R", make_resistor, "resistance", True)
    if element_type == "C":
        return _two_terminal(tokens, line_number, "C", make_capacitor, "capacitance", True)
    if element_type == "L":
        return _two_terminal(tokens, line_number, "L", make_inductor, "inductance")
    if element_type == "D":
        if len(tokens) not in (3, 4):
            _error(line_number, "D record expects 3 or 4 fields")
        scale = _value(tokens[3], "scale", line_number, allow_zero=False) if len(tokens) == 4 else 1.0
        return make_diode(name, _node(tokens[1], line_number), _node(tokens[2], line_number), scale)
    if element_type in {"QN", "QP", "MN", "MP"}:
        if len(tokens) not in (4, 5):
            _error(line_number, f"{element_type} record expects 4 or 5 fields")
        scale = _value(tokens[4], "scale", line_number, allow_zero=False) if len(tokens) == 5 else 1.0
        return make_three_terminal(
            name,
            element_type,
            _node(tokens[1], line_number),
            _node(tokens[2], line_number),
            _node(tokens[3], line_number),
            scale,
        )
    _error(line_number, f"unsupported element type {element_type}")


def parse_netlist(text):
    circuit = []
    names = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        element = parse_line(line, line_number)
        if element is None:
            continue
        if element["name"] in names:
            _error(line_number, f"duplicate element name {element['name']!r}")
        names.add(element["name"])
        circuit.append(element)
    return circuit


def parse_file(path):
    return parse_netlist(Path(path).read_text(encoding="utf-8"))
