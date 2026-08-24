# Milestone 1 Status

Status: Milestone 1 complete; Milestone 2 initial assembly slice complete.

- Concepts: restricted netlist grammar, terminal orientation, line-numbered validation, parser/viewer separation.
- Code: Chapter 1 element records, parser, deterministic layout, Tkinter Canvas viewer, example netlist.
- Supported records: V, VM, AM, I, R, C, L, D, QN, QP, MN, MP; G2 is retained for I/R/C.
- Viewer example: V1 source, AM1 series ammeter, R1 load, and VM1 across the load.
- Tests: parser behavior and headless viewer drawing are covered by pytest.
- MNA: dense R/V/I assembly now provides deterministic node and voltage-source branch indices, `A`, and `b`.
- Assumptions: scale defaults to `1.0`; numeric values are decimal or scientific notation; viewer layout targets small circuits.
- Limitations: capacitors, inductors, meters, and semiconductor records have no MNA stamps yet; no solving, editing, or arbitrary automatic schematic routing.
- Next session: extend the MNA tests and stamps for retained linear element groups, then begin the educational dense solver.
