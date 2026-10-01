# Circuit Simulation: Chapter-by-Chapter Summary

This document summarizes Farid N. Najm's *Circuit Simulation* (2010), based
on the supplied PDF. It is a study guide, not a replacement for the book: the
book's derivations, proofs, diagrams, references, and detailed examples remain
the authoritative source.

## Book-wide picture

The book explains how a circuit simulator turns a netlist into numerical
waveforms:

```text
circuit description
    -> device equations
    -> KCL/KVL and MNA formulation
    -> linear algebra solve
    -> Newton linearization for nonlinear devices
    -> time discretization for dynamic devices
    -> repeated solves, convergence checks, and time-step control
```

The central practical idea is to reduce difficult circuit problems to repeated
solutions of linear algebraic systems. Modified nodal analysis (MNA) provides
the common equation format; element stamps assemble the system directly from
the netlist; companion models turn nonlinear or dynamic elements into linear
models for one iteration or one time step.

The book focuses on DC analysis and transient analysis. It also surveys the
numerical issues that decide whether a simulator is fast, accurate, stable,
and able to converge: sparsity, pivoting, conditioning, Newton globalization,
integration accuracy, stiffness, charge conservation, and time-step control.

## Chapter 1: Introduction

### Topics and explanations

- **What circuit simulation does.** A circuit simulator checks an electrical
  design before manufacture by evaluating detailed device models and solving
  the resulting equations. It can produce node-voltage and element-current
  waveforms.
- **Device equations.** A device is introduced through a current-voltage
  relation. A resistor uses Ohm's law, a capacitor relates current to the
  derivative of voltage, and a general two-terminal nonlinear device can be
  written as `i = f(v)`. Linear means no powers above one; dynamic means that
  derivatives occur in the element equation.
- **Reference conventions.** Voltage is measured from the positive terminal
  to the negative terminal, and positive current flows from the positive
  terminal to the negative terminal. These conventions determine every later
  sign in KCL, KVL, and an MNA stamp.
- **Equation formulation.** Circuit behavior combines device equations with
  Kirchhoff's Current Law (KCL) and Kirchhoff's Voltage Law (KVL). The simple
  divider example illustrates substitution, but the book emphasizes that an
  ad hoc approach does not scale to large networks.
- **STA and MNA.** Sparse tableau analysis keeps branch currents, branch
  voltages, and node voltages. MNA eliminates most branch variables while
  retaining currents that cannot be eliminated, such as ideal voltage-source
  currents. MNA is smaller and is the formulation used throughout the book.
- **Linear solution.** A linear resistive circuit becomes `A x = b`. Direct
  methods include Gaussian elimination and LU factorization; iterative methods
  include Gauss-Jacobi and Gauss-Seidel. LU proceeds by factorization, forward
  substitution, and backward substitution.
- **Nonlinear solution.** Newton's method repeatedly linearizes the equations
  around a candidate point and solves the linearized circuit. Linearizing a
  nonlinear resistor gives a tangent conductance and an equivalent current
  source: its companion model.
- **Dynamic solution.** A finite-difference approximation replaces derivatives
  with algebraic expressions. Each time point is then a possibly nonlinear
  resistive problem based on dynamic companion models.
- **Overall flow.** The simulator reads a circuit file, discretizes dynamic
  equations, linearizes nonlinear equations, solves `A x = b`, checks
  convergence, and repeats until the final time.
- **Analysis modes.** SPICE-style modes include DC, transient, AC small
  signal, pole-zero, distortion, sensitivity, and noise analysis. This book
  concentrates on DC operating points and transient waveforms.

### Exercises and suggested work

Problem 1.1 is the first computer project: implement a parser for a small,
case-insensitive circuit language. It should normalize spaces and tabs, ignore
comments after `%`, accept non-negative integer nodes with node `0` as ground,
and represent each element as a linked-list record. The specified primitives
are independent voltage and current sources, resistors, capacitors, inductors,
diodes, npn/pnp BJTs, and n-/p-channel MOSFETs, with optional parameters or
`G2` group markers where specified.

Recommended implementation checks are: parse the supplied grammar, reject
malformed records with useful errors, preserve terminal order and source
direction, test comments and case insensitivity, and verify that element order
does not affect the resulting records.

## Chapter 2: Network Equations

### Topics and explanations

- **Elements and networks.** The chapter classifies passive elements as
  resistive or dynamic and linear or nonlinear. It distinguishes independent
  sources from controlled voltage and current sources, then explains equivalent
  circuit models as a way to represent complex components with basic lumped
  elements.
- **Simple device models.** The diode is introduced with an exponential
  current-voltage law. A basic MOSFET model is described using nonlinear
  resistive branches, controlled current, and capacitances. The purpose is to
  show how device physics becomes a circuit model, not to develop production
  semiconductor models.
- **Graph representation.** Circuit nodes become graph vertices and elements
  become directed edges. The edge direction follows positive current and
  voltage reference directions. The incidence matrix records `+1` at a tail,
  `-1` at a head, and zero elsewhere. Removing the ground row gives the
  reduced incidence matrix `A`.
- **Topological constraints.** KCL is `A i = 0`. KVL is `u = A^T v`, where
  `u` contains branch voltages and `v` contains non-ground node voltages.
  These constraints depend only on topology, not on element values.
- **Cycle and bond spaces.** Valid currents form the cycle space and valid
  voltages form the bond space. The two spaces are orthogonal and together span
  the branch space. A spanning tree constructs fundamental circulation vectors
  for the cycle-space basis; the reduced incidence matrix is a basis for the
  bond space.
- **Sparse tableau analysis.** Branch equations can be collected as
  `Z i + Y u = s`. Combining them with KCL and KVL produces a sparse tableau
  system. The form is general and very sparse but contains more variables than
  MNA.
- **Nodal analysis.** If there are no voltage sources, branch currents can be
  eliminated in favor of an admittance equation. The conductance matrix is
  `G = A Y A^T`. For connected passive resistive networks it has useful
  properties such as symmetry, diagonal dominance, positive definiteness, and
  the M-matrix property under the stated assumptions.
- **Solvability.** Necessary consistency conditions include no all-current-source
  cutset and no all-voltage-source loop. Dynamic networks require additional
  topological care, including avoiding problematic capacitor-voltage loops and
  inductor-current cutsets.
- **Modified nodal analysis.** MNA retains currents for voltage sources,
  inductors, current-control variables, and requested current outputs. Group 1
  elements have currents that can be eliminated; group 2 elements contribute
  explicit current unknowns and equations. This balances compactness and
  generality.
- **Element stamps.** The matrix and RHS are initialized to zero and each
  element adds a local contribution. Resistors contribute conductance stamps;
  current sources contribute RHS entries or a current equation; voltage sources
  add a branch-current unknown and voltage equation; controlled sources add
  coupling entries. Stamps are the practical bridge from a netlist to MNA.
- **Dynamic MNA.** Capacitors may be group 1 or group 2, while inductors must
  retain a current unknown. Their derivative terms add a dynamic matrix to the
  algebraic MNA system. The frequency-domain analogy replaces derivatives by
  impedances/admittances, although frequency analysis is not developed here.

### Exercises and suggested work

- **2.1:** Draw directed and undirected graphs, form the incidence matrix,
  construct a cycle-space basis, and write the compact topological constraints.
- **2.2-2.5:** Prove core matrix properties: positive diagonal entries of an
  SPD matrix, symmetry and diagonal dominance of a resistive conductance
  matrix, strict diagonal dominance with grounding resistors, and irreducible
  diagonal dominance under connectivity and consistency assumptions.
- **2.6-2.7:** Explain nodal analysis for grounded voltage sources and use
  superposition to solve networks containing voltage sources.
- **2.8:** Derive VCCS and CCCS stamps for both element groups.
- **2.9:** Derive the full dynamic MNA equations, including capacitor and
  inductor derivative terms.
- **2.10:** Build a linear MNA assembler for resistors, independent current
  sources, and independent voltage sources. Use the parser and linked-list
  records from Problem 1.1, interpret `G2`, and reproduce the supplied test
  matrix and solution.

For the project, test grounded and floating two-terminal elements, source
orientation, group-2 resistors, deterministic unknown ordering, singular
topologies, and residuals after solving.

## Chapter 3: Solution of Linear Algebraic Circuit Equations

### Topics and explanations

- **Problem statement.** Once MNA is assembled, solve `A x = b`. Circuit
  matrices are large and sparse, so the practical objective is to preserve
  sparsity while obtaining an accurate solution.
- **Matrix foundations.** The chapter reviews determinants, diagonal and
  triangular matrices, permutation matrices, combinatorial counts, and the
  properties used by elimination algorithms.
- **Gaussian elimination.** Forward elimination transforms a system to upper
  triangular form; backward substitution recovers the unknowns. The dense
  operation count is cubic. The chapter also explains elementary row operations,
  repeated right-hand sides, and why a zero pivot requires reordering.
- **LU factorization.** With row permutation `P`, factorization has the form
  `P A = L U`. The system is solved by applying the same permutation to `b`,
  forward substitution through `L`, and backward substitution through `U`.
  Crout, Doolittle, and Gauss variants choose different unit diagonals and
  computation orders. Gauss's method is closely related to in-place GE and is
  convenient when row and column pivoting matter.
- **Block elimination and Cholesky.** Block Gaussian elimination produces a
  Schur complement, which supports partitioning and parallel subproblem solves.
  SPD matrices admit the unique Cholesky factorization `A = L L^T`, reducing
  work and eliminating the need for general pivoting.
- **Accuracy and stability.** The chapter distinguishes input perturbation,
  backward error, forward error, residual, floating-point roundoff, and
  conditioning. A stable algorithm can still produce a poor answer for an
  ill-conditioned problem. The useful heuristic is forward error approximately
  equal to condition number times backward error.
- **Floating point.** IEEE arithmetic, machine epsilon, unit roundoff,
  rounding, overflow, underflow, and the model for basic arithmetic operations
  explain why cancellation and small pivots matter.
- **Pivoting for accuracy.** Partial pivoting chooses the largest entry in the
  current column; full pivoting searches the remaining submatrix and exchanges
  rows and columns. Partial pivoting is usually effective and cheaper, though
  no general strategy guarantees perfect stability.
- **Conditioning and scaling.** The matrix condition number is
  `kappa(A) = ||A|| ||A^-1||`. It is invariant under nonzero scalar scaling and
  permutation but not generally fixed by pivoting. Poorly scaled data can be
  improved with diagonal row and column scaling, though no universal strategy
  exists.
- **Iterative refinement.** Compute a residual, solve for a correction using
  existing factors, and update the solution. Mixed-precision residuals can
  recover additional accuracy when the factorization is stable and the problem
  is not too ill-conditioned.
- **Iterative methods.** Gauss-Jacobi uses old values throughout an iteration;
  Gauss-Seidel uses newly updated values. Both split `A = L + D + U` and
  converge when the iteration matrix has spectral radius below one. Strict
  diagonal dominance is sufficient but not necessary.
- **Partitioning.** Node tearing creates bordered block diagonal systems. Direct
  block elimination forms a smaller tearing-set Schur complement; iterative
  block methods solve subcircuits and update the tearing variables.
- **Sparse matrix techniques.** Triplet and compressed-column storage avoid
  storing zeros. Fill-ins arise during elimination, so row/column ordering is
  crucial. Markowitz pivoting estimates fill-in using row and column counts;
  threshold pivoting also guards accuracy. SPD matrices support diagonal
  minimum-degree ordering. COLMMD, COLAMD, and KLU are discussed as more
  advanced sparse strategies.

### Exercises and suggested work

- **3.1-3.4:** Derive operation counts, revise Crout for `P A = L D U`,
  write a row-oriented Crout variant, and derive Gauss factorization with a
  unit upper diagonal.
- **3.5-3.7:** Prove the SPD property of `C C^T`, derive Cholesky, and derive
  a Gauss-Cholesky algorithm.
- **3.8-3.12:** Prove induced-norm and condition-number results, including the
  minimum gain relation and invariance under row/column permutations.
- **3.13-3.15:** Design compressed-column transpose, triplet-to-compressed
  conversion, and compressed-column Gauss-Jacobi algorithms.
- **3.16:** Implement a general dense linear circuit solver using in-place Gauss
  LU with partial row pivoting. Reuse the parser and MNA assembler, solve the
  Chapter 2 test circuit, and compare every voltage/current against the given
  reference values.

The most important practical checks are a hand-solvable system, pivot swaps,
singular detection, residual reporting, comparison with an independent solver,
and tests showing that a small residual does not by itself establish good
conditioning.

## Chapter 4: Solution of Nonlinear Algebraic Circuit Equations

### Topics and explanations

- **Where nonlinear solves occur.** DC operating points, initial conditions for
  transient analysis, DC sweeps, and every implicit transient time point can
  require a nonlinear algebraic solve.
- **Nonlinear element classes.** The chapter considers nonlinear resistors,
  nonlinear capacitors/inductors as a later extension, and nonlinear controlled
  sources. For the algebraic part, explicit controlled current sources and
  controlled voltage sources are the key abstractions.
- **Nonlinear MNA.** The system is written as `G x + H g(x) = s`, or as a
  residual `f(x) = G x + H g(x) - s`. `G` captures linear behavior, `H`
  maps device terminal contributions into MNA equations, and `g` contains the
  nonlinear device functions.
- **DC preparation.** Capacitors are opened and inductors are shorted for DC.
  Large leakage resistors may be added to prevent isolated nodes, singular
  Jacobians, and unrealistic idealized topologies.
- **Newton's method.** At candidate `x^(k)`, solve
  `J_f(x^(k)) delta = -f(x^(k))` and set `x^(k+1) = x^(k) + delta`.
  Under local smoothness and nonsingularity assumptions, convergence is
  quadratic, but only when the initial guess is sufficiently close.
- **One-dimensional intuition.** Tangent intersections explain Newton steps.
  Secant approximates derivatives from two points and has golden-ratio order;
  Newton-chord keeps one derivative estimate and is linearly convergent. Fixed
  point iteration converges under contraction conditions and can become
  quadratic when its derivative vanishes at the solution.
- **Multidimensional analysis.** The Jacobian is the derivative matrix. The
  existence of partial derivatives alone is not enough for differentiability;
  continuity and bounded second derivatives provide useful sufficient conditions
  for a Lipschitz Jacobian and local Newton convergence.
- **Companion models.** Linearize each nonlinear element at the current point.
  A diode becomes a conductance `G_eq` in parallel with an equivalent current
  source `I_eq`. Stamping all companion models produces the Newton Jacobian
  and RHS without explicitly forming a symbolic global derivative.
- **General Newton assembly.** The linearized system is
  `J_f(x^(k)) x^(k+1) = H J_g(x^(k)) x^(k) - H g(x^(k)) + s`.
  Linear elements contribute their ordinary stamps; nonlinear elements
  contribute operating-point-dependent matrix and RHS stamps.
- **Multiterminal devices.** Partition terminal variables into voltage-driven
  and current-driven groups, express terminal responses as `y = h(x)`, and
  linearize the vector function. Each terminal response can be represented as
  a controlled source in MNA.
- **BJT and MOSFET examples.** Ebers-Moll BJT equations produce a multiport
  companion model with transconductance-like terms. The piecewise quadratic
  MOSFET model uses `G_ds`, `g_m`, and an equivalent current source whose
  values depend on cutoff, linear, or saturation region.
- **Internal nodes.** Symbolic block Gaussian elimination can remove internal
  device variables. The resulting reduced companion model is smaller, while
  hidden state variables are recovered after each Newton step for the next
  model evaluation.
- **Convergence and globalization.** Step limiting handles overshoot and
  exponential overflow. Diodes can use current/voltage iteration and logarithmic
  damping. Source stepping, Gmin stepping, and pseudo-transient continuation
  address starting points that are too far from the desired DC solution.
- **Homotopy methods.** Source stepping ramps independent sources from zero;
  Gmin stepping ramps added grounding conductances down; pseudo-transient adds
  inductors in series with voltage sources and capacitors across current sources
  so a simple initial state can evolve toward a DC steady state.

### Exercises and suggested work

- **4.1-4.4:** Compare fixed-point and Newton solutions for a fractional-power
  equation, analyze an oscillating Newton sequence, prove one-step convergence
  for affine systems, and relate a fixed-point Jacobian to `J_f`.
- **4.5-4.7:** Derive a companion model for a piecewise nonlinear resistor,
  prove useful norm inequalities, and derive the diode's critical voltage from
  its radius of curvature.
- **4.8:** Implement a general nonlinear DC solver for linear elements, diodes,
  BJTs, and MOSFETs. Build `G`, `H`, and nonlinear functions; generate fresh
  Jacobian/RHS stamps each Newton iteration; check both step and residual
  tolerances; apply generalized damping; and perform the supplied DC sweep.

Suggested tests include a one-diode circuit with a known operating point,
Newton failure from a distant initial guess, source stepping recovery, region
boundary tests for MOSFETs, BJT current conservation, overflow protection, and
the supplied node-7 transfer curve.

## Chapter 5: Solution of Differential Circuit Equations

### Topics and explanations

- **Dynamic device equations.** Capacitor current is the derivative of charge,
  `i = d q(v)/dt`; inductor voltage is the derivative of flux,
  `v = d phi(i)/dt`. For multiterminal devices, charge and flux may depend on
  several MNA variables, creating mutual capacitance or inductance terms.
- **Dynamic MNA and DAEs.** The general form is
  `G x(t) + H g(x(t)) + D(x) x'(t) = s(t)`. In general this is a DAE, not an
  ODE, because the derivative coefficient matrix may be singular. DAE index,
  consistent initial conditions, and topological constraints explain why
  circuit transient simulation is more delicate than ordinary ODE solving.
- **ODE background.** The chapter reviews initial-value problems, existence and
  uniqueness, well-posedness, linear constant-coefficient systems, convergence,
  consistency, zero-stability, characteristic roots, and local truncation error.
- **FE, BE, and TR.** Forward Euler is explicit but has a small stability
  region. Backward Euler is implicit, first order, and A-stable. The trapezoidal
  rule is implicit, second order, A-stable, and usually the circuit-simulation
  workhorse.
- **Linear multistep methods.** Adams methods and backward differentiation
  formulas are expressed through characteristic polynomials. BDF1 is backward
  Euler; BDF2 is second order; BDF3-6 are stiffly stable but not A-stable.
  The first Dahlquist barrier limits LMS order, and the second limits the order
  of A-stable LMS methods.
- **Implicit solution.** BE, TR, and BDF methods require solving an algebraic
  or nonlinear equation at each time point. Newton iteration is needed for stiff
  nonlinear circuit problems. Predictors provide an initial candidate; an
  extrapolated interpolation polynomial is particularly useful for stiff cases.
- **Stability and stiffness.** Absolute stability maps the scaled eigenvalue
  `h lambda` to roots inside the unit circle. A-stability removes stability-based
  step restrictions for left-half-plane modes. Stiffness appears when a method's
  stability constraint forces a much smaller step than accuracy alone requires.
- **Trapezoidal ringing.** For very fast decaying modes, TR's numerical root
  approaches `-1`, producing slowly damped alternating error. Smaller steps,
  BDF2, smoothing, or extrapolation can mitigate it.
- **Variable time steps.** Step control needs an LTE estimate, an accept/reject
  rule, and a way to update the integration formula. One-step methods change
  steps easily. Higher-order multistep methods need interpolation or
  variable-coefficient formulas. BDF2 interpolation and non-equidistant
  coefficients are developed explicitly.
- **Direct discretization and companion models.** Discretize each dynamic
  element equation, replace the element with an algebraic companion model, and
  solve the resulting resistive MNA system. FE yields source replacements; BE
  and TR yield Norton-like conductance/current-source models for linear `C` and
  `L`.
- **Nonlinear dynamic elements.** Capacitance-based models approximate
  `C(v) dv/dt`; charge-based models discretize `d q(v)/dt` directly. Charge
  terms improve conservation and avoid serious errors when capacitance changes
  sharply. Analogous flux-based models apply to nonlinear inductors.
- **Dynamic multiterminal elements.** A device can be represented as
  `y = p(x, x')`, or more practically as `y = g(x) + D(x) x'`. Internal state
  variables must remain tied to accessible terminal variables. MOSFET charge
  models use non-reciprocal capacitances and enforce total charge conservation.
- **Time-step control.** Compare estimated PLTE against relative and absolute
  tolerances, reject inaccurate steps, halve or otherwise reduce the step, and
  increase it when the error is small. Breakpoints in piecewise-linear sources
  must coincide with solution points. Newton iteration counts can provide a
  cheaper heuristic than full LTE estimation.
- **Complete transient flow.** Perform DC initialization, restore dynamic
  elements, predict the next point, run the Newton loop, estimate LTE, accept or
  reject, update histories, and continue until the requested final time.

### Exercises and suggested work

- **5.1-5.2:** Prove FE, BE, and TR consistency, zero-stability, and
  convergence; classify several proposed LMS methods.
- **5.3-5.4:** Implement FE, BE, and TR for scalar and two-state ODEs, use
  several step sizes, and compare stability and accuracy with exact solutions.
- **5.5-5.9:** Derive BDF2 using polynomial and divided-difference approaches,
  prove interpolation and LTE relations, and derive variable-step TR Milne
  estimates.
- **5.10-5.12:** Prove the TR stability-root properties, derive its boundary
  locus, and generate the fifth-order BDF stability region.
- **5.13:** Implement a trapezoidal-rule transient simulator on top of the
  nonlinear DC solver. Support resistors, independent sources, diodes, BJTs,
  MOSFETs, linear capacitors, and inductors; initialize dynamic states from DC;
  use Newton tolerances and a minimum step; implement PLTE-based control; and
  reproduce the supplied node 1, node 4, and node 5 waveforms.

Recommended validation includes a single RC circuit with an analytic response,
an RL circuit with known current, a stiff two-time-constant system, a TR ringing
case, rejected and retried steps, source breakpoints, capacitor charge
conservation, inductor current history, and the supplied transient test circuit.

## Cross-chapter project sequence

The book's computer projects form a coherent implementation path:

1. **Parser:** read and validate a restricted netlist language.
2. **MNA assembler:** create dense matrix and RHS stamps for linear circuits.
3. **Linear solver:** implement LU/GE, substitution, pivoting, and residuals.
4. **Nonlinear DC solver:** add device models, Newton iteration, companion
   models, damping, and continuation.
5. **Transient solver:** add dynamic histories, TR or another implicit method,
   nested Newton iteration, LTE estimation, and time-step control.

The repeated design pattern is deliberately consistent: define the element
equation, linearize or discretize it, express the result as a stamp, assemble a
global MNA system, solve it, and validate both numerical convergence and the
physical residuals implied by KCL/KVL.

## Glossary of recurring ideas

- **MNA:** Modified nodal analysis, the primary equation formulation.
- **STA:** Sparse tableau analysis, a more redundant but highly sparse
  formulation retaining branch currents and voltages.
- **Stamp:** A local matrix/RHS contribution made by one element.
- **Companion model:** A linear approximation of a nonlinear or discretized
  dynamic element used for one Newton iteration or time step.
- **Jacobian:** The matrix of first derivatives of the nonlinear residual.
- **Residual:** The amount by which a candidate fails to satisfy its equations.
- **Conditioning:** Sensitivity of the exact solution to problem-data changes.
- **Stability:** Sensitivity of a numerical algorithm or integration method to
  roundoff, perturbations, and dynamic modes.
- **LTE/PLTE:** Local truncation error and its principal leading-term estimate.
- **Homotopy/continuation:** Gradual transformation from an easy problem to
  the desired nonlinear problem.