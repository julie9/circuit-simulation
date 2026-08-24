# Circuit Simulator

An incremental Python 3.12+ learning project based on Farid N. Najm's
*Circuit Simulation*. The first milestone reads a restricted netlist and
displays it as a read-only Tkinter schematic. It does not solve circuits yet.

## Current State

Milestone 1 is complete. The project currently:

- parses the restricted Chapter 1 netlist language;
- preserves node order, source polarity, and current direction;
- validates records with line-numbered errors; and
- displays the parsed circuit in a deterministic, read-only Tkinter viewer.

The current viewer displays the example voltage source, resistor network, and
current source:

![Milestone 1 circuit viewer](docs/images/milestone-1-viewer.png)

Matrix assembly and circuit solving are planned for Milestones 2 and 3.

## Run

From the repository root:

```text
python -m pip install -e ".[test]"
python -m pytest
python -m circuit_sim.viewer examples/first_circuit.net
```

The parser is independent of Tkinter and returns plain dictionaries that
preserve terminal order and source direction. See `design-doc/project specification.md`
for the learning sequence, `docs/milestone_status.md` for current scope, and
[`docs/commit-workflow.md`](docs/commit-workflow.md) for repeatable phase
commits and commit-message conventions.
