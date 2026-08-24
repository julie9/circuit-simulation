from circuit_sim.layout import make_layout
from circuit_sim.parser import parse_netlist
from circuit_sim.viewer import draw_circuit


class RecordingCanvas:
    def __init__(self):
        self.calls = []

    def delete(self, tag):
        self.calls.append(("delete", tag))

    def create_line(self, *args, **kwargs):
        self.calls.append(("line", args, kwargs))

    def create_text(self, *args, **kwargs):
        self.calls.append(("text", args, kwargs))

    def create_oval(self, *args, **kwargs):
        self.calls.append(("oval", args, kwargs))

    def create_rectangle(self, *args, **kwargs):
        self.calls.append(("rectangle", args, kwargs))


def test_viewer_draws_symbols_wires_labels_and_does_not_mutate_records():
    circuit = parse_netlist("V1 1 0 5\nR1 1 2 1000\nI1 2 0 0.001")
    original = [element.copy() for element in circuit]
    canvas = RecordingCanvas()

    draw_circuit(canvas, circuit, make_layout(circuit))

    assert [element for element in circuit] == original
    assert sum(call[0] == "oval" for call in canvas.calls) >= 3
    assert sum(call[0] == "line" for call in canvas.calls) >= 3
    labels = [call[2]["text"] for call in canvas.calls if call[0] == "text" and "text" in call[2]]
    assert any("V1" in label for label in labels)
    assert any("node 0" in label for label in labels)


def test_layout_is_deterministic():
    circuit = parse_netlist("V1 1 0 5\nR1 1 2 1000\nR2 2 0 2000")
    layout = make_layout(circuit)
    assert layout == make_layout(circuit)
    assert layout["nodes"][1][1] == layout["nodes"][2][1]
    assert layout["elements"]["R1"]["orientation"] == "horizontal"
    assert layout["elements"]["R2"]["orientation"] == "vertical"
    assert layout["ground_rail_y"] > layout["nodes"][1][1]


def test_example_with_meters_draws_meter_faces():
    circuit = parse_netlist("V1 1 0 5\nAM1 1 2\nR1 2 0 1000\nVM1 2 0")
    canvas = RecordingCanvas()

    draw_circuit(canvas, circuit, make_layout(circuit))

    labels = [call[2]["text"] for call in canvas.calls if call[0] == "text" and "text" in call[2]]
    assert "A" in labels
    assert "V" in labels
    assert make_layout(circuit)["elements"]["AM1"]["orientation"] == "horizontal"
    assert make_layout(circuit)["elements"]["VM1"]["orientation"] == "vertical"