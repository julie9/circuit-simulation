# Book Coverage and Learning Plan

This plan turns Farid N. Najm's *Circuit Simulation* into a sequence of
small, reviewable Python milestones. The goal is not merely to add features;
it is to make every major algorithm understandable, testable, and connected
to the simulator already in this repository.

## Coverage status

| Book area | Current status | Code evidence | Next outcome |
|---|---|---|---|
| Chapter 1: parser and simulation overview | Implemented in part | `parser.py`, `elements.py`, viewer tests | Keep the grammar contract; add explicit device-model limits |
| Chapter 2: static linear MNA | Implemented for a subset | `mna.py`, MNA tests | Add graph/topology helpers and complete source/stamp coverage |
| Chapter 3: dense linear solve | Implemented educationally | `solver.py`, solver tests, solver guide | Add diagnostics, conditioning experiments, and sparse pathway |
| Chapter 4: nonlinear DC | Not implemented | No nonlinear solver or device models | Add diode first, then BJT/MOSFET and continuation |
| Chapter 5: transient analysis | Not implemented | No time-step loop or histories | Add BE/TR linear RC/RL, then nonlinear transient analysis |
| Sparse simulation | Study-only | No sparse assembly/factorization | Introduce sparse storage after dense correctness is stable |
| AC, noise, sensitivity, pole-zero | Not implemented | No analysis-mode framework | Treat as post-book extensions after DC/transient completion |

The existing chapter summary is the reading map. This file is the implementation
map and should be updated whenever a milestone changes status.

## Pedagogical contract

Every milestone follows the same learning loop:

1. **Map:** state the chapter sections, prerequisites, notation, and project
   requirement for the slice.
2. **Derive:** write the governing equations, dimensions, units, signs, and a
   hand-worked example before coding.
3. **Implement:** add the smallest production slice with descriptive Python,
   keeping the algorithm visible rather than hiding it in a library call.
4. **Test:** include a hand-solvable case, an expected failure or edge case, a
   residual or conservation check, and an independent NumPy/SciPy comparison
   where appropriate.
5. **Review:** explain the numerical risks, ask a short comprehension check,
   and record limitations before advancing.

The code should remain simple: plain records or small focused data structures,
separate assembly/solve/model/integration layers, configurable tolerances, and
no large framework introduced merely to support a single feature.

## Branch and PR sequence

Each item below should be implemented on its own branch from the previous
milestone, with one focused PR. A PR is ready only when its tests, learning
notes, limitations, and comprehension check are present.

1. `feature/book-ch2-topology`
   - Add reduced-incidence and graph helpers.
   - Derive and test KCL/KVL, cycle-space fixtures, and source/branch signs.
   - Finish missing linear source stamps without changing existing APIs.
2. `feature/book-ch3-numerical-diagnostics`
   - Add scaled residual reporting, pivot-growth/conditioning experiments,
     iterative refinement, and documented failure interpretation.
   - Keep the dense educational solver as the reference implementation.
3. `feature/book-ch4-newton-core`
   - Add residual/Jacobian interfaces, Newton iteration, absolute/relative
     stopping rules, iteration history, and clear convergence failures.
   - Start with a scalar nonlinear resistor and a one-diode operating point.
4. `feature/book-ch4-diode-device`
   - Add diode companion-model stamps, exponential overflow protection,
     voltage/current iteration, and damping experiments.
   - Reproduce the book's diode test circuits with independent references.
5. `feature/book-ch4-transistor-devices`
   - Add the simple Ebers-Moll BJT and piecewise quadratic MOSFET models.
   - Test region boundaries, KCL conservation, Jacobian terms, and the book's
     DC sweep fixture.
6. `feature/book-ch4-continuation`
   - Add source stepping first, then Gmin stepping, then pseudo-transient as
     separate strategies behind one solver interface.
   - Record when each strategy succeeds or fails; do not claim guaranteed
     global convergence.
7. `feature/book-ch5-dynamic-state`
   - Add capacitor voltage and inductor current histories plus DC
     initialization. Start with linear BE companion models.
8. `feature/book-ch5-trapezoidal-transient`
   - Add TR companion models and the nested time-step/Newton loop.
   - Reproduce analytic RC/RL cases and the book's transient fixture.
9. `feature/book-ch5-error-control`
   - Add step acceptance/rejection, PLTE estimates, breakpoints, minimum-step
     failures, and waveform reporting.
10. `feature/sparse-linear-path`
    - Add triplet and compressed-column representations, structural tests,
      fill-in demonstrations, and a SciPy sparse reference path.
    - Only optimize after dense and sparse results agree on shared fixtures.

Branch names are targets, not permission to create a large speculative change:
each branch should contain one coherent learning increment.

## Chapter 1 completion work

The parser already covers the restricted netlist grammar and the viewer is
deliberately read-only. Remaining Chapter 1 work is documentation and contract
clarity rather than a new simulator subsystem:

- document that engineering suffixes such as `1k` are intentionally not yet
  accepted, or add a separate suffix-parsing milestone with tests;
- document that diode, BJT, and MOSFET records parse but are not yet solvable;
- preserve terminal order, source polarity, and current direction in every
  later model;
- keep parser errors line-numbered and deterministic;
- add a small netlist validation report useful to later analysis modes.

## Chapter 2 completion work

Static linear MNA is usable but narrower than the book's full formulation.
The next implementation should cover:

- a reduced-incidence matrix helper and explicit KCL/KVL validation;
- graph connectivity, self-loop, source-loop, and source-cutset checks where
  they can be stated reliably for the supported element set;
- complete group-1/group-2 stamps for independent sources and retained
  currents, with focused tests for grounded terminals;
- explicit VCCS and CCCS stamp support if the netlist representation is
  extended to carry their control terminals;
- dynamic stamp documentation separated from the current static/DC behavior;
- a clear distinction between an assembled singular system and a malformed
  netlist.

The current capacitor-open and inductor-zero-voltage behavior is correct for
the static/DC formulation, but it must not be reused silently for transient
analysis.

## Chapter 3 completion work

The dense LU implementation is a good educational baseline. It does not yet
cover the chapter's broader numerical toolbox. Add these in increasing order:

- residuals normalized by `||A||`, `||x||`, and `||b||`, with interpretation;
- pivot-size and matrix-scale diagnostics;
- condition-number experiments using NumPy references, not an explicit inverse
  in production code;
- iterative refinement using the existing factors;
- Gauss-Jacobi and Gauss-Seidel as teaching implementations with convergence
  guards and spectral-radius experiments;
- a block-elimination notebook or small module for Schur complements;
- triplet and compressed-column storage, followed by fill-in visualizations;
- Markowitz/minimum-degree concepts as documented experiments before any
  production sparse pivoting implementation.

The project should not claim to be a production sparse solver. SciPy sparse
factorization is the modern reference path; the educational implementation
exists to expose the algorithm and its tradeoffs.

## Chapter 4 implementation plan

### Stage A: Newton core

Define a small solver contract around a residual function and Jacobian builder:

- input: candidate vector `x`, residual `f(x)`, Jacobian `J(x)`;
- solve: `J(x_k) delta = -f(x_k)` using the educational linear solver;
- update: `x_(k+1) = x_k + delta`;
- stop: both a scaled step test and a scaled residual test;
- failure: maximum iterations, unusable Jacobian, non-finite device values,
  and stagnation are reported distinctly.

### Stage B: diode

Implement the exponential diode first. Its companion model must expose the
operating-point conductance and equivalent source, with guarded exponential
evaluation. Test forward bias, reverse bias, a known resistor-diode circuit,
and a deliberately difficult initial guess.

### Stage C: BJT and MOSFET

Add the book's simple models only after the diode path is stable. Keep model
evaluation separate from stamping so that device equations can be tested
without assembling a full circuit. Verify terminal-current conservation and
finite Jacobians at region transitions.

### Stage D: globalization

Implement source stepping before Gmin stepping. Add damping as an independent
policy so experiments can compare a full Newton step with a limited step. Add
pseudo-transient only after the transient state representation exists; otherwise
it would obscure the learning objective.

## Chapter 5 implementation plan

### Stage A: linear dynamic history

Represent capacitor voltage and inductor current histories explicitly. Define
initialization rules and units. Validate each companion model against the
continuous equation and an analytic first-order circuit.

### Stage B: BE, then TR

Implement BE first because its companion models and stability behavior are
simpler. Then implement TR, explain its A-stability and ringing, and compare
both methods on the same RC/RL fixtures.

### Stage C: time-step control

Add a time-point result record containing time, solution, Newton iterations,
accepted/rejected state, and error estimate. Add PLTE estimates, breakpoint
alignment, minimum-step failure, and deterministic retry behavior.

### Stage D: nonlinear transient

Only after linear transient analysis is independently verified should dynamic
elements be combined with diode/BJT/MOSFET Newton models. Add charge-based
capacitor interfaces before claiming charge conservation.

## Future work and missing points from the book

The sections above explain the implementation details. This section is the
ordered backlog: it records what is still missing, what should build on earlier
work, and which items are extensions beyond the book's main projects. The
implementation should continue forward through the existing pipeline:

```text
parser -> MNA -> linear solver -> Newton DC -> transient integration
```

Each stage should reuse the preceding stage's equations, tests, sign
conventions, and diagnostics rather than introducing a parallel implementation.

### Chapter 1: parser and representation

- Clarify the supported netlist contract, including the intentional rejection
  of engineering suffixes such as `1k`, or add suffix parsing as a separate
  feature.
- Document that diode, BJT, and MOSFET records can be parsed before their
  solving models are available.
- Preserve terminal order, source polarity, current direction, and line-numbered
  parser errors for every later analysis mode.
- Add a small netlist validation report for later solvers.

### Chapter 2: network equations and MNA

Build on the existing static MNA assembly and topology helpers by adding:

- graph connectivity, self-loop, source-loop, and source-cutset checks where
  they are well-defined for the supported element set;
- complete STA, nodal-analysis, cycle-space, bond-space, and network
  solvability study tools;
- complete group-1/group-2 stamps for retained currents and grounded sources;
- VCCS, CCCS, VCVS, and CCVS syntax and stamps when control terminals and
  control-current conventions are added to the netlist representation;
- dynamic-stamp documentation kept separate from the current static/DC
  behavior.

The current capacitor-open and inductor-zero-voltage behavior is valid only for
static/DC assembly. Transient companion models must not reuse those assumptions
silently.

### Chapter 3: linear numerical methods

Build on the educational dense LU solver and its residual tests by adding:

- normalized residuals, pivot-size and matrix-scale diagnostics, condition
  estimates, growth-factor experiments, and mixed-precision refinement;
- Cholesky and block Gaussian elimination;
- Gauss-Jacobi, Gauss-Seidel, iterative refinement, convergence guards, and
  spectral-radius experiments;
- triplet and compressed-column storage, fill-in demonstrations, and a SciPy
  sparse reference path;
- Markowitz pivoting, minimum-degree concepts, COLAMD-like ordering, and
  circuit-oriented sparse factorization experiments.

The educational implementation should remain separate from the production
reference path: SciPy/SuiteSparse can validate correctness and performance,
but should not hide the algorithms being learned.

### Chapter 4: nonlinear DC analysis

Build on the diode companion-model increment by adding:

- a reusable residual/Jacobian Newton interface with scaled absolute and
  relative tolerances, iteration history, stagnation detection, and distinct
  failure diagnostics;
- Ebers-Moll BJT and piecewise quadratic MOSFET models, including region
  transitions, finite Jacobians, and terminal-current conservation;
- source stepping, Gmin stepping, and pseudo-transient continuation, each as a
  separately testable strategy rather than an opaque fallback;
- temperature dependence, series resistance, breakdown behavior, and richer
  device models only after the educational models are verified.

Nonlinear capacitors and inductors, charge/flux-based models, and multiterminal
device coupling belong with Chapter 5 because they require transient state and
conservation handling.

### Chapter 5: transient analysis

Build on DC initialization and the nonlinear solver by adding:

- capacitor-voltage and inductor-current histories;
- backward Euler, then trapezoidal-rule companion models for linear RC/RL
  circuits;
- BDF2, variable-step methods, LTE/PLTE estimation, smoothing, extrapolation,
  stiffness experiments, and trapezoidal-ringing demonstrations;
- step acceptance/rejection, breakpoints, minimum-step failure, waveform
  output, and reproducible transient fixtures;
- nonlinear transient coupling and charge/flux-conserving multiterminal device
  models.

### Beyond the core book projects

After the DC and transient core is stable, add the analysis modes mentioned in
Chapter 1: AC small-signal, pole-zero, distortion, sensitivity, noise,
temperature, statistical, and switched-capacitor analysis. Model libraries,
subcircuits, hierarchy, parameter sweeps, engineering units, and production
sparse performance are also later extensions.

### Modern production practice

These topics extend beyond the book or connect several chapters:

- automatic differentiation, sparse Newton-Krylov methods, equilibration,
  event handling, and parallel assembly;
- property-based and differential testing, reproducible benchmarks, and
  profiling of assembly, factorization, Newton iterations, and rejected steps;
- robust trust-region or line-search methods alongside circuit-specific
  Newton iteration;
- current sparse-DAE and circuit-simulation literature after the core
  implementation is complete.

## Modern practice to learn alongside the book

The book is an excellent algorithmic foundation, but a current simulator also
needs practice beyond its 2010 scope:

1. Learn sparse matrix formats and use SuiteSparse/SciPy as an independent
   reference before attempting a custom sparse factorization.
2. Study robust nonlinear least-squares and trust-region/line-search methods,
   while preserving Newton's method as the circuit-specific baseline.
3. Study scaling, equilibration, condition estimation, and backward-error
   diagnostics as first-class solver outputs.
4. Compare BE, TR, BDF, and modern variable-order DAE integrators on stiff
   problems; understand why production tools often use adaptive BDF methods.
5. Learn charge/flux conservation and device-model consistency, not only local
   capacitance derivatives.
6. Use property-based tests for KCL/KVL and conservation, differential tests
   against trusted solvers, and regression fixtures with known tolerances.
7. Benchmark assembly, factorization, Newton iterations, and rejected time
   steps separately; numerical correctness and performance should be measured
   independently.
8. Read current sparse-DAE and circuit-simulation literature after the core
   implementation is complete, using the book's bibliography as the historical
   starting point rather than the final word.

## Definition of done for the whole learning project

The repository can claim broad book coverage only when it has:

- a tested parser and documented supported netlist subset;
- static MNA assembly with explicit sign and unknown-ordering contracts;
- educational dense linear methods with residual and conditioning diagnostics;
- nonlinear DC analysis with at least diode, BJT, and MOSFET fixtures;
- BE and TR transient analysis with initialized dynamic histories;
- adaptive step acceptance/rejection and waveform regression tests;
- at least one charge-based dynamic-device example;
- a documented sparse pathway and comparison against SciPy;
- chapter guides, derivations, comprehension checks, and limitations;
- separate PRs whose tests pass independently and whose numerical conventions
  remain compatible across chapters.