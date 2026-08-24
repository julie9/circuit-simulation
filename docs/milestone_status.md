# Milestone 1 Status

Status: initial implementation complete.

- Concepts: restricted netlist grammar, terminal orientation, line-numbered validation, parser/viewer separation.
- Code: Chapter 1 element records, parser, deterministic layout, Tkinter Canvas viewer, example netlist.
- Supported records: V, VM, AM, I, R, C, L, D, QN, QP, MN, MP; G2 is retained for I/R/C.
- Viewer example: V1 source, AM1 series ammeter, R1 load, and VM1 across the load.
- Tests: parser behavior and headless viewer drawing are covered by pytest.
- Assumptions: scale defaults to `1.0`; numeric values are decimal or scientific notation; viewer layout targets small circuits.
- Limitations: no matrix assembly, solving, editing, or arbitrary automatic schematic routing.
- Next session: derive node indexing and linear MNA stamps for the R/V/I subset.
