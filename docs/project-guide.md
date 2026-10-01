# Circuit Simulator Project Guide

This is an incremental Python 3.12+ learning project based on Farid N. Najm's
*Circuit Simulation* (2010). The goal is to understand the circuit and
numerical methods while building one small, coherent simulator.

## Chapter map

| Chapter | Main topics | Project result |
|---|---|---|
| 1. Introduction | Device equations, circuit formulation, solution techniques, and simulation modes | Validated circuit representation and read-only viewer |
| 2. Network Equations | Network graphs, KCL/KVL, nodal analysis, MNA, element groups, and stamps | Verified dense linear MNA assembly |
| 3. Linear Algebraic Equations | Substitution, Gaussian elimination, LU, pivoting, conditioning, and sparse methods | Educational dense LU solver with diagnostics |
| 4. Nonlinear Algebraic Equations | Residuals, Jacobians, Newton iteration, companion models, and convergence | Nonlinear DC operating-point solver |
| 5. Differential Circuit Equations | ODEs, DAEs, integration methods, companion models, and time-step control | Transient simulator with waveform output |

The intended simulation flow is:

```text
netlist -> parser -> circuit records -> unknown indexing -> MNA assembly
  -> linear solve -> nonlinear iteration -> transient time stepping
  -> results and plots
```

For the complete chapter map, learning sequence, branch plan, and deferred
book topics, see the [book coverage and learning plan](book-coverage-plan.md).

## Principles

- Preserve voltage references, current directions, terminal order, MNA
  variables, and matrix conventions.
- Implement important numerical algorithms explicitly before using NumPy or
  SciPy implementations as references.
- Work in small, verifiable increments with deterministic tests.
- State equations, dimensions, units, assumptions, and indexing conventions
  before numerical code.
- Keep parsing, representation, drawing, assembly, solving, nonlinear
  iteration, transient integration, and reporting separate.
- Prefer simple Python and introduce abstractions only when they solve an
  observed problem.

## Current status

| Milestone | Status | Repository result |
|---|---|---|
| 1. Parser and viewer | Complete | Restricted netlist parsing and deterministic read-only Tkinter viewer |
| 2. Linear MNA assembly | Complete | Dense static assembly for resistors, sources, capacitors, and inductors |
| 3. Dense linear solver | Complete | Educational LU with partial pivoting, failure detection, and residuals |
| 4. Nonlinear DC analysis | In progress | Diode companion model and damped Newton operating-point solver |
| 5. Transient analysis | Planned | Dynamic histories, companion models, and waveform output |

The current implementation is intentionally educational. Capacitors are open
circuits and inductors are ideal zero-voltage branches only in the static/DC
formulation. Meters and semiconductor records remain outside the supported
linear MNA solve unless a later milestone adds their models.

The next implementation slice is defined in the coverage plan rather than in
this guide. This keeps the repository status current without duplicating the
book's detailed learning roadmap.

## Numerical policy

Use NumPy for Chapter 2 onward. Unless another precision is being studied,
matrix, right-hand-side, and solution arrays use `np.float64` with shapes
`(n_unknowns, n_unknowns)`, `(n_unknowns,)`, and `(n_unknowns,)`.

Implement the educational algorithm explicitly before using NumPy or SciPy
solvers as references. Explain dimensions, indexing, broadcasting, and any
in-place mutation. Develop dense assembly and an educational dense solver
before sparse storage or sparse solvers.

Every solver needs a hand-solvable case, a residual check, an edge or failure
case, an independent reference comparison where appropriate, and a stated
tolerance. For `A @ x = b`, calculate `r = b - A @ x` and consider scaling,
conditioning, singularity, and small pivots.

## Project boundaries

Use small functions, plain dictionaries for element records, plain lists for
circuits, descriptive names, visible terminal order, and direct pytest
assertions. Avoid inheritance, complicated class hierarchies, hidden
behavior, premature optimization, and GUI classes unless shared state makes
one useful. Introduce dataclasses only when dictionary keys become difficult
to maintain, and explain and test that migration.

Use Jupyter notebooks only for derivations, experiments, and visualizations.
The viewer is read-only and targets small circuits; editing, arbitrary
automatic routing, hierarchical circuits, waveform plotting, and simulation
controls are deferred.

The first release reads a small netlist, rejects malformed lines clearly,
returns simple element dictionaries, displays an R-V-I schematic, preserves
terminal and source conventions, passes parser tests, and keeps parser, GUI,
and circuit-data responsibilities separate. It does not solve circuits.

Keep production simulator code under `src/` and tests under `tests/`.

## Supporting documents

- [Book coverage and learning plan](book-coverage-plan.md): implementation
  status, pedagogical milestones, branch/PR sequence, missing topics, and
  modern numerical-practice extensions.
- [Parser and viewer specification](parser-viewer-spec.md): grammar,
  electrical conventions, and drawing requirements.
- [Dense solver guide](solver-guide.md): Chapter 3 concepts, derivation,
  algorithm, numerical risks, and comprehension check.
- [Commit workflow](commit-workflow.md): commit, branch, and pull-request
  conventions.
- [AI work log](ai-work-log/README.md): historical prompts, decisions, and
  lessons from AI-assisted sessions.
