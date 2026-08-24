"""Read-only Tkinter viewer for parsed Chapter 1 circuits."""

import argparse
import tkinter as tk

from .layout import make_layout
from .parser import parse_file


def draw_wire(canvas, x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, fill="#283238", width=2)


def draw_routed_wire(canvas, start, end, rail_y=None):
    start_x, start_y = start
    end_x, end_y = end
    if rail_y is not None and end_y == rail_y and start_y != end_y:
        canvas.create_line(start_x, start_y, start_x, rail_y, fill="#283238", width=2)
        canvas.create_line(start_x, rail_y, end_x, rail_y, fill="#283238", width=2)
    elif start_x == end_x or start_y == end_y:
        draw_wire(canvas, start_x, start_y, end_x, end_y)
    else:
        canvas.create_line(start_x, start_y, end_x, start_y, end_x, end_y, fill="#283238", width=2)


def draw_ground(canvas, x, y):
    for offset, width in ((0, 28), (7, 18), (14, 8)):
        canvas.create_line(x - width / 2, y + offset, x + width / 2, y + offset, width=2)


def _label(canvas, element, x, y, value_key):
    label_y = y - 38 if element["type"] in {"V", "I"} else y - 24
    canvas.create_text(x, label_y, text=f"{element['name']}  {element[value_key]:g}", fill="#172027")


def draw_resistor(canvas, element, x, y, orientation="horizontal"):
    if orientation == "vertical":
        points = [(x, y - 25), (x - 8, y - 15), (x + 8, y - 5), (x - 8, y + 5), (x + 8, y + 15), (x, y + 25)]
    else:
        points = [(x - 25, y), (x - 15, y - 8), (x - 5, y + 8), (x + 5, y - 8), (x + 15, y + 8), (x + 25, y)]
    canvas.create_line(*[coordinate for point in points for coordinate in point], fill="#b34b2c", width=2)
    _label(canvas, element, x, y, "resistance")


def draw_voltage_source(canvas, element, x, y, orientation="vertical"):
    canvas.create_oval(x - 22, y - 22, x + 22, y + 22, outline="#1d6973", width=2)
    canvas.create_text(x, y - 9, text="+", fill="#1d6973", font=("TkDefaultFont", 12, "bold"))
    canvas.create_text(x, y + 10, text="-", fill="#1d6973", font=("TkDefaultFont", 12, "bold"))
    _label(canvas, element, x, y, "voltage")


def draw_current_source(canvas, element, x, y, orientation="vertical"):
    canvas.create_oval(x - 22, y - 22, x + 22, y + 22, outline="#7b4d85", width=2)
    canvas.create_line(x, y + 13, x, y - 13, arrow=tk.LAST, fill="#7b4d85", width=2)
    _label(canvas, element, x, y, "current")


def draw_meter(canvas, element, x, y, orientation="vertical"):
    color = "#236b58" if element["type"] == "VM" else "#a15b24"
    canvas.create_oval(x - 24, y - 24, x + 24, y + 24, outline=color, width=2)
    canvas.create_text(x, y, text="V" if element["type"] == "VM" else "A", fill=color,
                       font=("TkDefaultFont", 14, "bold"))
    canvas.create_text(x, y - 40, text=element["name"], fill="#172027")


def _draw_placeholder(canvas, element, x, y):
    canvas.create_rectangle(x - 28, y - 20, x + 28, y + 20, outline="#65737a", width=2)
    canvas.create_text(x, y, text=element["type"], fill="#65737a", font=("TkDefaultFont", 10, "bold"))
    canvas.create_text(x, y + 34, text=element["name"], fill="#172027")


def draw_circuit(canvas, circuit, layout):
    canvas.delete("all")
    for node, (x, y) in layout["nodes"].items():
        canvas.create_text(x, y + 25, text=f"node {node}", fill="#42545b")
        if node == 0:
            draw_ground(canvas, x, y)
        else:
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#283238", outline="")
    for element in circuit:
        position = layout["elements"][element["name"]]
        x, y = position["x"], position["y"]
        element_nodes = [node for key, node in element.items() if key.endswith("_node")]
        terminals = position.get("terminals", [(x, y)] * len(element_nodes))
        for node, terminal in zip(element_nodes, terminals):
            draw_routed_wire(canvas, layout["nodes"][node], terminal, layout.get("ground_rail_y"))
        draw_function = {
            "R": draw_resistor,
            "V": draw_voltage_source,
            "I": draw_current_source,
            "VM": draw_meter,
            "AM": draw_meter,
        }.get(element["type"])
        if draw_function:
            draw_function(canvas, element, x, y, position["orientation"])
        else:
            _draw_placeholder(canvas, element, x, y)


def show_circuit(circuit, layout=None):
    window = tk.Tk()
    window.title("Circuit Simulator - Milestone 1")
    canvas = tk.Canvas(window, width=760, height=420, background="#f4f1ea")
    canvas.pack(fill=tk.BOTH, expand=True)
    draw_circuit(canvas, circuit, layout or make_layout(circuit))
    window.mainloop()


def main():
    argument_parser = argparse.ArgumentParser(description="Display a Chapter 1 circuit netlist.")
    argument_parser.add_argument("netlist")
    arguments = argument_parser.parse_args()
    show_circuit(parse_file(arguments.netlist))


if __name__ == "__main__":
    main()
