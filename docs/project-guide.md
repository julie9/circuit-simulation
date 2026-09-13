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

Milestone 1, netlist parser and viewer, is complete. The project currently
parses the restricted netlist language, validates records with line-numbered
errors, preserves terminal and source conventions, and draws a deterministic,
read-only Tkinter schematic.

Milestone 2, linear MNA assembly, is complete. Deterministic node and branch
indexing and dense `np.float64` assembly are implemented for resistors, voltage
sources, current sources, capacitors, and inductors. In the static/DC
formulation, capacitors are open circuits and inductors are ideal zero-voltage
branches with current unknowns. Meters remain display-only and semiconductor
records are unsupported. The system is assembled but not solved.

### Next actions

- Define the educational dense solver interface and numerical conventions.
- Implement forward and backward substitution.
- Implement dense LU factorization with partial pivoting and diagnostics.
- Compare solver results against independent references.

### Milestone 2 checklist

- [x] Map non-ground nodes and voltage-source branch currents deterministically.
- [x] Assemble dense `A` and `b` with the established unknown ordering.
- [x] Stamp resistors, voltage sources, and current sources.
- [x] Test matrix values, source direction, sign conventions, and grounded terminals.
- [x] Reject unsupported element types explicitly.
- [x] Add stamps for retained linear element groups.
- [x] Decide whether meters contribute to MNA and define their unknowns.
- [x] Add capacitor and inductor MNA tests when their stamps exist.
- [x] Add more hand-assembled matrix comparisons.
- [x] Verify the complete small-circuit assembly target.

## Roadmap

1. **Netlist parser and viewer:** parse and display a recognizable small
   circuit. Complete.
2. **Linear MNA assembly:** add retained linear-element stamps and verify
  dense `A x = b` systems against hand-assembled references. Complete.
3. **Linear solver:** implement substitution, dense LU with partial pivoting,
   singularity detection, residual reporting, and independent comparisons.
4. **Nonlinear DC analysis:** add device models, Jacobians, Newton iteration,
   convergence tests, and robustness techniques such as damping or stepping.
5. **Transient analysis:** add capacitor and inductor histories, companion
   models, DC initialization, nested iteration, time-step control, and
   waveform output.

## Working method

For each learning or coding increment:

1. State the objective, prerequisites, and relevant mathematical objects.
2. Explain the physical meaning, dimensions, units, and sign conventions.
3. Work a small example by hand and translate it into an algorithm.
4. Implement the smallest useful code increment.
5. Add deterministic tests, including a hand-solvable case and failure or
   edge cases where relevant.
6. Check residuals and compare with an independent reference when studying a
   solver.
7. Record assumptions, limitations, and the next small increment.

Do not advance to the next learning session until the comprehension check is
answered or continuation is explicitly requested. At the start of each
chapter, record its purpose and prerequisites, how the sections connect, new
notation, algorithms or pseudocode, element stamps or companion models,
numerical risks, project requirements, and proposed short sessions.

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

## Next solver milestone

Milestone 3 is the educational dense linear solver:

- [ ] Define the solver interface and numerical conventions.
- [ ] Implement forward and backward substitution.
- [ ] Implement dense LU factorization with partial pivoting.
- [ ] Detect singular or unusable pivots.
- [ ] Report residuals and compare against independent reference results.

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

- [Parser and viewer specification](parser-viewer-spec.md): grammar,
  electrical conventions, and drawing requirements.
- [Commit workflow](commit-workflow.md): commit, branch, and pull-request
  conventions.
- [AI work log](ai-work-log/README.md): historical prompts, decisions, and
  lessons from AI-assisted sessions.
