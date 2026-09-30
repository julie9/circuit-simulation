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

These topics are either absent from the code or intentionally deferred:

- full controlled-source syntax and stamps, including VCCS, CCCS, VCVS, and
  CCVS control variables;
- complete STA, nodal-analysis, cycle-space, bond-space, and topology tools;
- rigorous network solvability diagnostics beyond basic singular-matrix errors;
- Cholesky, block GE, Gauss-Jacobi, Gauss-Seidel, and iterative refinement;
- sparse storage, fill-in prediction, Markowitz pivoting, minimum degree,
  COLAMD-like ordering, and circuit-oriented sparse factorization;
- scaling, condition estimates, growth-factor monitoring, and mixed-precision
  refinement;
- diode, BJT, and MOSFET nonlinear models and companion stamps;
- damping, source stepping, Gmin stepping, and pseudo-transient continuation;
- nonlinear capacitors, nonlinear inductors, charge-based and flux-based
  models, and charge-conserving multiterminal device models;
- BE, TR, BDF2, variable-step methods, LTE/PLTE estimation, smoothing,
  extrapolation, and stiffness experiments;
- DC initialization of dynamic states and robust transient failure recovery;
- waveform output, plotting, breakpoints, and reproducible transient fixtures;
- AC small-signal, pole-zero, distortion, sensitivity, noise, temperature,
  statistical, and switched-capacitor analyses mentioned in Chapter 1;
- model libraries, subcircuits, hierarchical netlists, parameter sweeps,
  units/engineering suffixes, and production-grade sparse performance;
- modern production concerns not developed in the book: automatic
  differentiation options, sparse Newton-Krylov methods, scaling/equilibration,
  event handling, parallel assembly, reproducible benchmarks, and stronger
  property-based and differential testing.

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