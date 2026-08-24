# Circuit Simulator

An incremental Python 3.12+ learning project based on Farid N. Najm's
*Circuit Simulation*. The first milestone reads a restricted netlist and
displays it as a read-only Tkinter schematic. It does not solve circuits yet.

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
