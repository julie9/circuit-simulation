# Parser and Viewer Specification

## Parser

The parser answers: "Is this line valid, and what circuit element does it describe?" It does not assemble matrices, solve circuits, select every MNA unknown, or draw on the GUI.

### General rules

- One complete element per line.
- Input is case-insensitive.
- Spaces and tabs separate fields.
- Text after `%` is a comment.
- Nodes are non-negative integers; node `0` is ground.
- Values are finite, non-negative decimal or scientific-notation numbers.
- Terminal order is preserved.
- Duplicate canonical element names are rejected.
- Engineering suffixes such as `1k` and `10u` are deferred.

### Supported records

```text
V<number>  positive_node negative_node voltage
VM<number> positive_node negative_node
AM<number> positive_node negative_node
I<number>  positive_node negative_node current [G2]
R<number>  positive_node negative_node resistance [G2]
C<number>  positive_node negative_node capacitance [G2]
L<number>  positive_node negative_node inductance
D<number>  positive_node negative_node [scale]
QN<number> collector base emitter [scale]
QP<number> collector base emitter [scale]
MN<number> drain gate source [scale]
MP<number> drain gate source [scale]
```

`VM` and `AM` are display-only in Milestone 1. Scale defaults to `1.0`. The parser stores `G2`; Chapter 2 assigns retained branch-current unknowns.

For two-terminal devices, voltage is `V(positive_node) - V(negative_node)` and positive current flows from the positive node to the negative node. BJT order is collector, base, emitter. MOSFET order is drain, gate, source.

### Parsing sequence

1. Remove comments and surrounding whitespace.
2. Skip blank lines.
3. Split tokens and normalize names or keywords.
4. Identify the element type.
5. Validate token count, nodes, values, scale, and `G2`.
6. Create an element dictionary.
7. Reject duplicate names and append valid records.
8. Test valid, invalid, and regression cases.

## Viewer

The viewer displays parser output as a recognizable, read-only schematic. It uses Tkinter `Canvas`, orthogonal wires, explicit terminal endpoints, deterministic placement, and real graphical symbols. It must not mutate parser records or parse netlist text.

Supported early symbols include wires, junctions, ground, resistors, voltage sources, current sources, node labels, names, values, polarity marks, and current arrows. Voltmeter and ammeter symbols contain `V` and `A`.

For small textbook circuits, snap to a fixed grid, place the main path near the top, use a bottom ground rail, prefer horizontal resistors and vertical grounded branches, place voltage sources near the left when suitable, use right-angle wires, and keep placement repeatable. Use a separate optional layout dictionary for demonstrations that need manual coordinates; never put coordinates in electrical records.

The first demonstration circuit is:

```text
V1 1 0 5
R1 1 2 1000
R2 2 0 2000
I1 2 0 0.001
```

The viewer acceptance criteria are: no input prompt on startup, every element drawn once, visible ground and node labels, correct polarity and arrow direction, no parser mutation, deterministic placement, and no GUI startup during parser tests.

Editing, arbitrary automatic routing, hierarchical circuits, waveform plotting, and simulation controls are deferred.
