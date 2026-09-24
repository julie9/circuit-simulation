# Circuit Simulator

An incremental Python 3.12+ learning project based on Farid N. Najm's
*Circuit Simulation*. The project reads a restricted netlist, displays it as a
read-only Tkinter schematic, and reports a DC operating point with a
node-voltage plot when the circuit uses supported analysis elements.

## Current State

The completed milestones currently provide:

- parses the restricted Chapter 1 netlist language;
- preserves node order, source polarity, and current direction;
- validates records with line-numbered errors; and
- displays the parsed circuit in a deterministic, read-only Tkinter viewer;
- assembles and solves linear MNA systems with educational dense LU; and
- solves diode DC operating points with damped Newton iteration.

The current viewer displays the example voltage source, resistor network, and
current source:

![Milestone 1 circuit viewer](docs/images/milestone-1-viewer.png)

In the static/DC formulation, capacitors are open circuits and inductors are
ideal zero-voltage branches. Meters remain display-only, and BJT/MOS records
are not yet part of DC analysis.

## Run

From the repository root:

```text
python -m pip install -e ".[test]"
python -m pytest
python -m circuit_sim.viewer examples/first_circuit.net
```

The example netlist includes display-only meters, so the viewer still draws its
graph but reports that DC analysis is unavailable. To see the solved plot,
pass a netlist containing resistors, independent sources, capacitors, inductors,
and/or diodes, for example:

```text
V1 1 0 5
R1 1 2 1000
D1 2 0
```

The GUI is intentionally read-only: editing, transient waveforms, and
simulation controls remain outside the current milestone.

The parser is independent of Tkinter and returns plain dictionaries that
preserve terminal order and source direction. See
[`docs/project-guide.md`](docs/project-guide.md) for project scope, status,
and roadmap; [`docs/parser-viewer-spec.md`](docs/parser-viewer-spec.md) for
the input and drawing contract; and
[`docs/commit-workflow.md`](docs/commit-workflow.md) for repeatable phase
commits and commit-message conventions.
