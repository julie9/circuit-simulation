# AI Work Log

This directory records how AI assistance was used while developing the circuit simulator. The goal is to preserve the main project context, decisions, and lessons learned.

## How to record a session

Add a new entry at the top of this file after a meaningful coding session. Use the date and a short description as the heading.

## Entry format

```
## YYYY-MM-DD: Short description

- AI Model: Which AI model was used, and any relevant settings.

**Prompt**

What was asked of the AI?

**Result**

What changed or was investigated?

**Notes**

Important decisions, tests, lessons, or follow-up work.
```


---

## 2026-09-13: Implement Milestone 3 dense linear solver

- **AI Model**: GitHub Copilot.

**Prompt**

Create a new git branch on top of the completed Milestone 2 and continue with
Milestone 3, preserving logical commits and an AI work-log trace.

**Result**

Created `feature/dense-linear-solver` from the Milestone 2 tip. Added an
educational dense solver with forward substitution, backward substitution,
partial-pivot LU factorization, singular-pivot detection, finite-value and
shape validation, and residual reporting. Exported `solve_linear_system` from
the package API. Tests cover a hand-assembled MNA system, LU reconstruction,
row pivoting, singular matrices, invalid inputs, residuals, and comparison with
`np.linalg.solve`.

**Notes**

The solver returns `solution`, `residual`, `residual_norm`, `lower`, `upper`,
and `permutation`. The factorization convention is `P @ A = L @ U`, where the
returned permutation indexes rows of `A`. A hand-solved expected value initially
omitted the current-source contribution; the focused test caught and corrected
that arithmetic error. The next work is nonlinear DC analysis.

---

## 2026-09-13: Complete Milestone 2 linear MNA assembly

- **AI Model**: GitHub Copilot.

**Prompt**

Check whether Milestone 2 is complete, implement the remaining work in logical
increments, commit the changes, and keep a trace in the AI work log.

**Result**

Extended dense static MNA assembly to support capacitors and inductors. A
capacitor contributes no DC stamp. An inductor contributes an ideal
zero-voltage branch constraint and a branch-current unknown. Branch-current
indices now include voltage sources and inductors in circuit order. Added exact
matrix tests for capacitor behavior, grounded inductors, mixed branch ordering,
unsupported meters and semiconductor records, and a complete hand-assembled
linear fixture.

Milestone 2 documentation now records the retained-element conventions and is
marked complete. VM and AM remain display-only records and are rejected by MNA
assembly, preserving the parser/viewer contract.

**Notes**

The implementation commit is `64e5aac`, `Implement linear MNA assembly`.
Focused validation passed with 10 tests. NumPy and pytest were installed in the
workspace `.venv` because the initially selected interpreter lacked NumPy.
The next milestone is the educational dense linear solver; transient capacitor
and inductor companion models remain deferred.

---

## 2026-08-23: Start implementation 

- **AI Model**: GitHub Copilot Chat, Auto (only choice on Student package). **Selected Model**: GPT5.6-Luna.

**Prompt**

Let's start to work on this Circuit Simulator project following the project specification attached here. Dispatch work and design full loop to check the goal of Milestone 1: Netlist parser and viewer

- parse the restricted language;
- normalize case and whitespace;
- remove comments;
- validate element syntax and node identifiers;
- store typed-by-convention dictionaries;
- display the parsed circuit using real electrical symbols.

**Result**

First draft of implementation for both parser and viewer. Parser is working, but the viewer is not yet displaying the circuit correctly (diagonal links).
 
**Notes**
 
Visualisation was subpar (diagonals links), but the parser was working. Iterates a few times. Provides an example of a simple diagram drawing. Adds voltmeter, ammeter and voltage source.

---

## 2026-08-15: 1st session, Prompt Engineering.

- **AI Model**: MS365 Copilot Chat, GTP5.6-Think.

**Prompt**

Provide a prompt that you enable me to go chapter by chapter in this book, understand the concepts presented and code the suggested methods. FIrst look at the book in general to see its format regarding the code. WHat would be a good prompt for a AI agent?

**Result**

Detailled prompt, learning oriented. See attached file `docs/ai-work-log/prompt1.md`.

**Notes**

I asked to implement in Python instead of C.
