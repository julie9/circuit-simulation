# Circuit Simulator Project Specification

**Primary reference:** Farid N. Najm, *Circuit Simulation* (2010)
**Language:** Python 3.12+
**Purpose:** Learn the circuit theory and numerical methods in the book while progressively building a small, coherent circuit simulator.

## Project principles

1. Preserve the book's voltage references, current directions, terminal order, MNA variables, and matrix conventions.
2. Implement important numerical algorithms explicitly before using NumPy or SciPy solvers as references.
3. Work in small, verifiable increments rather than producing a complete solution at once.
4. State equations, dimensions, units, assumptions, and indexing conventions before numerical code.
5. Translate mathematical one-based indexing into Python zero-based indexing explicitly.
6. Use deterministic tests with known answers.
7. Keep parsing, representation, drawing, assembly, solving, nonlinear iteration, and transient integration separate.
8. Prefer beginner-friendly Python and introduce abstraction only when it solves an observed problem.
9. Use the graphical viewer to inspect parser output and circuit conventions, not as a schematic editor.

## Current scope

The first milestone covers a restricted netlist parser and a read-only Tkinter circuit viewer. It does not assemble or solve circuit equations yet.

The first release must:

- read a small Chapter 1 netlist;
- reject malformed lines clearly;
- return simple element dictionaries;
- display a recognizable R-V-I schematic;
- preserve node order, source polarity, and current direction;
- pass deterministic parser tests; and
- keep parser, GUI, and circuit-data responsibilities separate.

## Supporting documents

- [Book overview](../docs/book-overview.md): chapter summaries and the overall simulation flow.
- [Learning and coding workflow](../docs/learning-workflow.md): session format, Python style, and numerical policy.
- [Parser and viewer specification](../docs/parser-viewer-spec.md): Chapter 1 grammar, conventions, and viewer requirements.
- [Implementation roadmap](../docs/implementation-roadmap.md): chapter targets, milestones, and next sessions.
- [Milestone status](../docs/milestone_status.md): current implementation state.
- [AI work log](../docs/prompts/README.md): prompts, results, and decisions from AI-assisted sessions.

## Repository structure

Keep the structure small initially. Add directories for `mna`, `linalg`, `nonlinear`, and `transient` only when those chapters begin.

```text
circuit-simulation/
├── pyproject.toml
├── README.md
├── design-doc/
│   └── project specification.md
├── src/
│   └── circuit_sim/
├── tests/
├── examples/
└── docs/
```
