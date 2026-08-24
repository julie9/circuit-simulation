import pytest

from circuit_sim.parser import NetlistError, parse_netlist, remove_comment


def test_remove_comment_and_skip_blank_lines():
    circuit = parse_netlist("\n  % ignored\n r1\t1  0  1000 % load\n")
    assert circuit == [{
        "type": "R",
        "name": "R1",
        "positive_node": 1,
        "negative_node": 0,
        "resistance": 1000.0,
        "group2": False,
    }]
    assert remove_comment("R1 1 0 1000 % load") == "R1 1 0 1000"


def test_parse_all_chapter_one_record_types_and_defaults():
    circuit = parse_netlist("""V1 1 0 5
VM1 2 0
AM1 1 2
I1 2 0 1e-3 G2
R1 1 2 1000
C1 2 0 1e-6
L1 2 0 2e-3
D1 2 0
QN1 3 2 0
QP1 3 2 0 2
MN1 3 2 0
MP1 3 2 0 0.5
""")
    assert [element["type"] for element in circuit] == ["V", "VM", "AM", "I", "R", "C", "L", "D", "QN", "QP", "MN", "MP"]
    assert circuit[2]["positive_node"] == 1
    assert circuit[3]["group2"] is True
    assert circuit[7]["scale"] == 1.0
    assert circuit[9]["scale"] == 2.0
    assert circuit[10]["first_node"] == 3


def test_engineering_suffix_is_rejected_until_later_extension():
    with pytest.raises(NetlistError, match="resistance must be a real number"):
        parse_netlist("R1 1 0 1k")


@pytest.mark.parametrize("netlist, message", [
    ("R1 -1 0 1", "node must be a non-negative integer"),
    ("R1 1 0 -1", "finite and non-negative"),
    ("R1 1 0 1 BAD", "optional fourth field must be G2"),
    ("R1 1 0 1\n r1 2 0 2", "duplicate element name"),
    ("V1 1 0", "V record expects 4 fields"),
])
def test_invalid_records_have_line_numbered_errors(netlist, message):
    with pytest.raises(NetlistError, match=message) as error:
        parse_netlist(netlist)
    assert str(error.value).startswith("line ")


def test_names_are_canonicalized_and_terminal_order_is_preserved():
    circuit = parse_netlist("v7 8 2 3")
    assert circuit[0]["name"] == "V7"
    assert circuit[0]["positive_node"] == 8
    assert circuit[0]["negative_node"] == 2