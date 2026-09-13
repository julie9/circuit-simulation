# Milestone Status

## Milestone 1: Netlist parser and viewer

Status: Complete.

- Implemented the restricted netlist grammar, normalization, terminal orientation, and line-numbered validation.
- Added Chapter 1 element records, deterministic layout, the Tkinter Canvas viewer, and the example netlist.
- Supported records: V, VM, AM, I, R, C, L, D, QN, QP, MN, MP; G2 is retained for I/R/C.
- Covered parser behavior and headless viewer drawing with pytest.

## Milestone 2: Linear MNA assembly

Status: In progress; the initial R/V/I assembly slice is complete.

- Implemented deterministic node-voltage and voltage-source branch-current indices.
- Implemented dense `np.float64` assembly of `A` and `b` for resistors, voltage sources, and current sources.
- Tested matrix values, source-current direction, sign conventions, and grounded-terminal stamps.
- Remaining: add stamps for the retained linear element groups, extend hand-assembled matrix tests, and verify the full small-circuit assembly target.

## Current assumptions and limitations

- Scale defaults to `1.0`; numeric values may use decimal or scientific notation.
- Viewer layout targets small circuits and does not provide editing or arbitrary automatic schematic routing.
- Capacitors, inductors, meters, and semiconductor records do not have MNA stamps yet.
- The linear system is assembled but not solved; solving belongs to Milestone 3.

## Next step

Extend the MNA tests and stamps for retained linear element groups, then begin the educational dense solver.
