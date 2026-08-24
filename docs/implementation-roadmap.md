# Implementation Roadmap

## Chapter 1: Parser and basic viewer

Implement element helpers, parser normalization and validation, line-numbered errors, tests, graphical symbols, and deterministic layouts.

**Completion target:** parse and display a small linear circuit without solving it.

## Chapter 2: Linear MNA assembly

Add node and branch-current indexing, dense `np.float64` matrices, linear element stamps, and hand-assembled matrix comparisons. Add capacitor and inductor symbols when needed.

**Completion target:** assemble a verified dense system `Ax = b` for small linear circuits.

## Chapter 3: Linear solver

Implement forward and backward substitution, dense LU with partial pivoting, singularity detection, residual reporting, and independent reference comparisons. Study sparse storage only after dense correctness.

**Completion target:** solve and validate Chapter 2 systems without explicit matrix inversion.

## Chapter 4: Nonlinear DC analysis

Implement a diode model, Jacobian, Newton iteration, residual and step tests, and robustness techniques such as damping, source stepping, and `Gmin` stepping. Add transistor support after diode validation.

**Completion target:** compute and validate a nonlinear DC operating point.

## Chapter 5: Transient analysis

Implement capacitor and inductor histories, dynamic companion models, DC initialization, the outer time loop, the inner Newton loop, step control, and waveform output. Validate against an analytical RC or RL circuit.

**Completion target:** produce validated transient waveforms.

## Milestones

1. **Netlist parser and viewer:** parse the restricted language and display a recognizable schematic.
2. **Linear MNA assembly:** create unknown indices and verify dense `A` and `b`.
3. **Linear solver:** implement substitution, LU, pivoting, and diagnostics.
4. **Nonlinear DC solver:** add device models, Newton iteration, and convergence controls.
5. **Transient solver:** add histories, companion models, nested iteration, and error control.

## Immediate sessions

1. Create and test element helpers.
2. Implement lexical normalization.
3. Parse R, V, and I records with valid and invalid tests.
4. Draw the fixed demonstration circuit.
5. Connect parser output to reusable symbol functions.
6. Add restricted deterministic layout for small circuits.

## First release

The first release reads a small Chapter 1 netlist, rejects malformed lines clearly, returns simple element dictionaries, displays an R-V-I schematic, preserves terminal and source conventions, passes parser tests, and keeps parser, GUI, and circuit data responsibilities separate. It does not assemble or solve equations.
