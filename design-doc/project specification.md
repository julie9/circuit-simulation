# Circuit Simulator Learning Project Specification

**Primary reference:** Farid N. Najm, *Circuit Simulation* (2010)  
**Language:** Python 3.12+  
**Purpose:** Learn the circuit theory and numerical methods in the book while progressively building a small, coherent circuit simulator.

---

## 1. Project principles

1. The uploaded book is the primary technical reference.
2. Preserve the book's voltage references, current directions, terminal order, MNA variables, and matrix conventions.
3. Implement the important numerical algorithms explicitly before using NumPy or SciPy solvers as references.
4. Work in small, verifiable increments rather than producing a complete solution at once.
5. State equations, dimensions, units, assumptions, and indexing conventions before numerical code.
6. Translate mathematical one-based indexing into Python zero-based indexing explicitly.
7. Use deterministic tests with known answers.
8. Keep parsing, representation, drawing, assembly, solving, nonlinear iteration, and transient integration separate.
9. Prefer beginner-friendly Python. Introduce abstraction only when it solves an observed problem.
10. Use the graphical viewer to inspect parser output and circuit conventions, not as a schematic editor.

---

## 2. Book overview

Najm's five chapters form a cumulative simulator-development sequence.

### Chapter 1: Introduction

Introduces device equations, circuit-equation formulation, solution techniques, simulation modes, and the overall nested simulation flow. The computer project begins with a parser for a restricted circuit-description language.

**Project result:** a validated circuit representation and a read-only circuit viewer.

### Chapter 2: Network Equations

Develops network graphs, incidence matrices, KCL, KVL, Sparse Tableau Analysis, nodal analysis, Modified Nodal Analysis, element groups, and element stamps.

**Project result:** dense linear MNA assembly for supported elements, followed later by sparse assembly.

### Chapter 3: Linear Algebraic Equations

Covers triangular substitution, Gaussian elimination, LU factorization, pivoting, numerical accuracy, conditioning, residuals, iterative methods, sparse storage, fill-in, and ordering.

**Project result:** an educational dense LU solver with pivoting and diagnostics. Sparse techniques follow after dense correctness.

### Chapter 4: Nonlinear Algebraic Equations

Develops nonlinear MNA equations, residuals, Jacobians, Newton iteration, companion models, convergence tests, damping, and continuation methods.

**Project result:** a nonlinear DC operating-point solver, beginning with a diode circuit.

### Chapter 5: Differential Circuit Equations

Relates ODEs and DAEs to circuit simulation. Develops Forward Euler, Backward Euler, trapezoidal integration, BDF methods, stability, local truncation error, dynamic companion models, and time-step control.

**Project result:** a transient simulator with an outer time-step loop, an inner Newton loop, and waveform output.

### Overall simulation flow

```text
netlist
  -> parser
  -> circuit and device records
  -> node and unknown indexing
  -> MNA assembly
  -> linear solve
  -> nonlinear Newton iteration
  -> transient time stepping
  -> results and plots
```

---

## 3. Chapter learning workflow

At the start of each chapter, prepare a short map containing:

- purpose and prerequisites;
- major sections and their connections;
- new mathematical objects and notation;
- algorithms and pseudocode;
- element stamps or companion models;
- numerical risks and misconceptions;
- computer project requirements;
- simulator extension;
- proposed sequence of short sessions.

Each learning or coding session should include:

1. learning objectives;
2. plain-language explanation;
3. formal mathematics and symbols;
4. dimensions, units, and physical interpretation;
5. a small hand-worked example;
6. equation-to-algorithm translation;
7. book-faithful pseudocode;
8. a minimal Python increment;
9. tests and expected results;
10. numerical and edge cases;
11. a comprehension check;
12. one small exercise;
13. completion criteria and milestone update.

Do not advance automatically. Continue after the comprehension check is answered or continuation is requested.

---

## 4. Simplified Python coding style

### Initial style

Use:

- small functions;
- plain dictionaries for element records;
- plain lists for circuits;
- descriptive variable names;
- keyword arguments where terminal order could be unclear;
- ordinary `if`, `for`, and `return` statements;
- pytest tests with direct expected results.

Avoid initially:

- inheritance;
- complicated object-oriented hierarchies;
- abstract base classes;
- design patterns;
- advanced type annotations;
- decorators that hide behavior;
- premature optimization;
- GUI classes unless shared state makes one useful.

Dataclasses may be introduced later if dictionary keys become difficult to maintain. The migration must be explained and tested.

### Element helper example

```python
def make_resistor(
    name,
    positive_node,
    negative_node,
    resistance,
    group2=False,
):
    return {
        "type": "R",
        "name": name,
        "positive_node": positive_node,
        "negative_node": negative_node,
        "resistance": resistance,
        "group2": group2,
    }
```

Usage:

```python
resistor = make_resistor(
    name="R1",
    positive_node=1,
    negative_node=0,
    resistance=1000.0,
)

circuit = [resistor]
```

Keyword arguments make the terminal orientation visible and reduce sign errors.

### Small-function rule

A function should have one clear responsibility. For example:

```python
def remove_comment(line):
    code = line.split("%", 1)[0]
    return code.strip()
```

Test:

```python
def test_remove_comment():
    result = remove_comment("R1 1 0 1000 % resistor")
    assert result == "R1 1 0 1000"
```

---

## 5. Numerical programming policy

### NumPy

Use NumPy when numerical arrays begin in Chapter 2. Unless another precision is being studied deliberately:

```python
A.dtype == np.float64
b.dtype == np.float64
x.dtype == np.float64
```

For a system with `n_unknowns`:

```python
A.shape == (n_unknowns, n_unknowns)
b.shape == (n_unknowns,)
x.shape == (n_unknowns,)
```

When NumPy is used:

- do not hide the algorithm under `numpy.linalg.solve` before implementing it;
- explain dimensions, dtypes, indexing, and broadcasting;
- identify every in-place mutation, such as `A[row, column] += value`;
- keep copies when mutation could destroy test inputs;
- compare the educational result with NumPy or SciPy independently.

### Dense before sparse

1. Dense MNA assembly.
2. Dense educational linear solver.
3. Verified residuals and failure cases.
4. SciPy sparse matrix assembly.
5. Sparse storage, fill-in, and ordering experiments.

### Solver validation

Every solver must include:

- a hand-solvable case;
- a residual check;
- an edge or failure case;
- an independent NumPy or SciPy comparison when appropriate;
- a stated numerical tolerance.

For a computed solution of \(Ax=b\), calculate:

\[
r=b-Ax.
\]

Report a residual norm and compare it with the selected tolerance. Also warn about poor scaling, conditioning, singularity, or small pivots when relevant.

---

## 6. Chapter 1 parser specification

### Responsibility

The parser answers:

> Is this line valid, and what circuit element does it describe?

It does not assemble matrices, solve the circuit, select every MNA unknown, or draw directly on the GUI.

### General grammar rules

- one complete element per line;
- case-insensitive input;
- spaces and tabs act as separators;
- text following `%` is a comment;
- node identifiers are non-negative integers;
- node `0` is ground;
- parameter values are finite, non-negative real numbers;
- terminal order must never be changed silently;
- duplicate canonical element names are rejected.

Initially accept decimal and scientific notation, such as `1000`, `0.002`, and `1e-6`. Engineering suffixes such as `1k` and `10u` are a later extension.

### Supported Chapter 1 records

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

`VM` is an ideal voltmeter connected across its positive and negative
terminals. `AM` is an ideal ammeter whose positive current direction is from
its positive terminal to its negative terminal. Both records are display-only
in Milestone 1; their measured values are not calculated until later analysis
support exists.

Optional device scale defaults to `1.0` as a documented implementation choice.

### Electrical conventions

For two-terminal devices:

\[
v=V(\text{positive node})-V(\text{negative node}).
\]

Positive current points from `positive_node` to `negative_node`.

Terminal order:

- BJT: collector, base, emitter;
- MOSFET: drain, gate, source.

The parser stores `G2`. Chapter 2 determines how retained branch-current unknowns are assigned.

### Parser implementation sequence

1. Create one small helper function per element type.
2. Remove comments and surrounding whitespace.
3. Skip blank and comment-only lines.
4. Split a line into tokens.
5. Normalize names and keywords to uppercase.
6. Identify the element type.
7. Validate token count.
8. Convert and validate nodes, values, scale, and `G2`.
9. Create an element dictionary.
10. Reject duplicate names.
11. Append the element to the circuit list.
12. Add valid, invalid, and regression tests.

---

## 7. Read-only graphical circuit viewer

### Purpose

Display the circuit read by the parser as a recognizable electrical schematic. The initial GUI is a parser and convention inspection tool, not an editor.

### Technology

Use Python's built-in Tkinter library and its `Canvas` widget.

The viewer must use orthogonal Canvas wires and explicit terminal endpoints.
For the first demonstration circuit, use a textbook-style two-node layout:
the voltage source is a left vertical branch, R1 is the top horizontal branch,
grounded branches are vertical, and a bottom return rail connects them. Avoid
diagonal wires and label collisions. The viewer remains read-only and must not
mutate parser records.

The circuit symbols are real graphical lines, circles, arrows, and text. ASCII drawings are used only in explanations and documentation.

### Data flow

```text
netlist file
  -> parse_file()
  -> circuit list
  -> simple layout
  -> Tkinter Canvas drawing
```

The parser contains no Tkinter code, and the viewer does not parse netlist text.

### First supported symbols

For Chapter 1 and early Chapter 2:

- wire;
- connected-junction dot;
- ground;
- resistor;
- independent voltage source;
- independent current source;
- node labels;
- element names and values;
- voltage polarity and current arrows.

The first actual symbols are drawn as follows:

- resistor: zigzag Canvas line;
- voltage source: circle with `+` and `-` marks;
- current source: circle with an arrow;
- voltmeter: circle containing `V`;
- ammeter: circle containing `A`;
- ground: three horizontal lines of decreasing width;
- wire: straight horizontal or vertical line;
- junction: filled dot.

### Initial layout restrictions

A netlist specifies connectivity but not coordinates. Therefore, the first layout supports small textbook circuits using these rules:

1. snap nodes and elements to a fixed grid;
2. place the main path near the top;
3. place a ground rail near the bottom;
4. prefer horizontal resistors;
5. prefer vertical grounded branches;
6. place voltage sources near the left when suitable;
7. place parallel branches beside one another;
8. use right-angle wires;
9. produce the same layout on repeated runs.

For demonstration circuits that do not fit the simple automatic rules, allow a separate optional layout dictionary. Do not store coordinates in electrical element records.

### Minimal GUI functions

```python
def draw_wire(canvas, x1, y1, x2, y2):
    ...


def draw_ground(canvas, x, y):
    ...


def draw_resistor(canvas, element, x, y, orientation):
    ...


def draw_voltage_source(canvas, element, x, y, orientation):
    ...


def draw_current_source(canvas, element, x, y, orientation):
    ...


def show_circuit(circuit, layout):
    ...
```

Begin with functions rather than a GUI class.

### First demonstration circuit

```text
V1 1 0 5
R1 1 2 1000
R2 2 0 2000
I1 2 0 0.001
```

Expected topology:

- `V1` connects node 1 to ground;
- `R1` connects node 1 to node 2;
- `R2` connects node 2 to ground;
- `I1` is in parallel with `R2`;
- polarity, current direction, values, ground, and node labels are visible.

### First viewer acceptance criteria

- opens without requesting user input;
- draws real Canvas symbols rather than ASCII art;
- displays every supported element exactly once;
- preserves parsed terminal order;
- displays unambiguous ground and node labels;
- displays correct voltage polarity and current-source arrow direction;
- does not mutate parser records;
- produces deterministic placement;
- does not open during parser unit tests.

### Deferred GUI features

- schematic editing;
- dragging and rotating components;
- reading input from GUI controls;
- arbitrary automatic schematic layout;
- curved wire routing;
- hierarchical circuits and subcircuits;
- waveform plotting inside the schematic;
- simulation controls;
- professional schematic-capture behavior.

---

## 8. Recommended repository structure

Keep the structure small initially:

```text
circuit-simulation/
├── pyproject.toml
├── README.md
├── src/
│   └── circuit_sim/
│       ├── __init__.py
│       ├── elements.py
│       ├── parser.py
│       ├── symbols.py
│       ├── layout.py
│       └── viewer.py
├── tests/
│   ├── test_elements.py
│   └── test_parser.py
├── examples/
│   └── first_circuit.net
└── docs/
    ├── conventions.md
    ├── milestone_status.md
    └── numerical_limitations.md
```

Add directories for `mna`, `linalg`, `nonlinear`, and `transient` only when those chapters begin. Avoid creating empty architecture in advance.

---

## 9. Chapter implementation plan

### Chapter 1: Parser and basic viewer

**Theory:** simulation pipeline, device equations, KCL/KVL overview, equation formulation, and analysis modes.

**Code:**

- element helper functions;
- parser normalization and validation;
- structured line-numbered errors;
- valid and invalid parser tests;
- graphical symbols for R, V, I, ground, wires, and junctions;
- one fixed demonstration layout;
- simple deterministic layout for small circuits.

**Completion target:** parse and display a small linear circuit without solving it.

### Chapter 2: Linear MNA assembly

**Theory:** incidence matrices, KCL, KVL, STA, nodal analysis, MNA, grouping, element stamps, and solvability.

**Code:**

- node-to-index mapping;
- retained branch-current indexing;
- dense `np.float64` matrix and RHS allocation;
- stamps for supported linear elements;
- hand-assembled matrix comparisons;
- capacitor and inductor drawing symbols;
- optional GUI annotations for node and MNA indices.

**Completion target:** assemble a verified dense system \(Ax=b\) for small linear circuits.

### Chapter 3: Linear solver

**Theory:** triangular systems, Gaussian elimination, LU factorization, pivoting, stability, conditioning, residuals, and sparse fill-in.

**Code:**

- forward substitution;
- backward substitution;
- dense LU factorization;
- partial pivoting;
- singular and near-singular detection;
- residual and backward-error reporting;
- NumPy and SciPy reference comparisons;
- sparse storage and ordering only after dense correctness.

**GUI:** no required new symbols. Optionally display solver or singularity warnings separately from the schematic.

**Completion target:** solve and validate Chapter 2 MNA systems without explicit matrix inversion.

### Chapter 4: Nonlinear DC analysis

**Theory:** nonlinear residual, Jacobian, Newton correction, companion models, convergence, damping, and continuation.

**Code:**

- diode model and companion stamp;
- Newton iteration;
- residual and step convergence tests;
- difficult and convergent examples;
- damping, followed progressively by source stepping and `Gmin` stepping;
- BJT and MOSFET support after diode validation.

**GUI:** diode symbol first; clearly labeled three-terminal representations before detailed transistor symbols.

**Completion target:** compute and validate a nonlinear DC operating point.

### Chapter 5: Transient analysis

**Theory:** ODEs, DAEs, discretization, FE, BE, trapezoidal rule, BDF, stability, LTE, and companion models.

**Code:**

- capacitor and inductor state histories;
- dynamic companion models;
- DC initial operating point;
- outer time loop and inner Newton loop;
- time-step acceptance and rejection;
- analytical RC or RL validation;
- waveform storage and Matplotlib plots.

**GUI:** time-dependent source labels and optional operating-point annotations. Waveforms remain in separate Matplotlib figures.

**Completion target:** produce validated transient waveforms for a known linear circuit, followed later by nonlinear examples.

---

## 10. Cumulative milestones

### Milestone 1: Netlist parser and viewer

- parse the restricted language;
- normalize case and whitespace;
- remove comments;
- validate element syntax and node identifiers;
- store typed-by-convention dictionaries;
- display the parsed circuit using real electrical symbols.

### Milestone 2: Linear MNA assembly

- create unknown indices;
- derive and implement linear stamps;
- assemble and verify dense \(A\) and \(b\);
- preserve all sign conventions.

### Milestone 3: Linear solver

- implement substitution and LU;
- add pivoting and numerical diagnostics;
- validate using residuals and independent solvers.

### Milestone 4: Nonlinear DC solver

- implement nonlinear models and Jacobians;
- add Newton iteration and convergence controls;
- introduce robustness techniques incrementally.

### Milestone 5: Transient solver

- implement dynamic histories and companion models;
- nest the time-step, Newton, assembly, and linear-solve loops;
- add error control and waveform regression tests.

---

## 11. Running project status record

After every session, update:

- concepts learned;
- code added or modified;
- tests passed;
- tests still needed;
- supported elements;
- assumptions made;
- known limitations;
- numerical weaknesses;
- remaining work;
- recommended next session;
- milestone status.

---

## 12. Immediate next sessions

### Session 1: Element helpers

Create and test small helper functions for resistor, voltage source, and current source records. Verify terminal order and defaults.

### Session 2: Lexical normalization

Implement and test comment removal, blank-line handling, whitespace splitting, and case normalization.

### Session 3: Initial parsing

Parse R, V, and I records. Add valid and invalid tests with line-numbered errors.

### Session 4: First graphical circuit

Draw the fixed demonstration circuit with manually chosen coordinates using Tkinter Canvas.

### Session 5: Parser-to-viewer connection

Pass parsed dictionaries to reusable symbol functions while keeping parser and GUI code independent.

### Session 6: Restricted automatic layout

Add deterministic grid placement for small series, parallel, and grounded branches.

---

## 13. First-release definition

The first project release is complete when it can:

1. read a small Chapter 1 netlist file;
2. reject malformed lines clearly;
3. return a list of simple element dictionaries;
4. display a recognizable R-V-I electrical schematic in Tkinter;
5. preserve node order, source polarity, and current direction;
6. pass deterministic parser tests;
7. keep GUI, parser, and circuit data responsibilities separate.

It does not yet assemble or solve circuit equations.
