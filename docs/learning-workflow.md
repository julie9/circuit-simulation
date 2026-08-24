# Learning and Coding Workflow

## Chapter map

At the start of each chapter, write a short map covering:

- purpose and prerequisites;
- major sections and how they connect;
- new mathematical objects and notation;
- algorithms and pseudocode;
- element stamps or companion models;
- numerical risks and misconceptions;
- project requirements and proposed short sessions.

## Session format

Each learning or coding session should cover only what is needed for the next small increment:

1. learning objectives;
2. plain-language explanation;
3. mathematics, dimensions, units, and physical meaning;
4. a small hand-worked example;
5. equation-to-algorithm translation;
6. minimal Python code;
7. tests, edge cases, and expected results;
8. comprehension check and completion criteria.

Do not advance automatically. Continue after the comprehension check is answered or continuation is requested.

## Initial Python style

Use small functions, plain dictionaries for element records, plain lists for circuits, descriptive names, visible terminal order, and direct pytest assertions.

Avoid inheritance, complicated class hierarchies, abstract base classes, advanced annotations, hidden behavior, premature optimization, and GUI classes unless shared state makes one useful. Introduce dataclasses only if dictionary keys become difficult to maintain, and explain and test that migration.

## Numerical policy

Use NumPy when numerical arrays begin in Chapter 2. Unless another precision is being studied deliberately, matrix, right-hand-side, and solution arrays use `np.float64` with shapes `(n_unknowns, n_unknowns)`, `(n_unknowns,)`, and `(n_unknowns,)`.

Implement important algorithms explicitly before using NumPy or SciPy solvers as references. Explain dimensions, indexing, broadcasting, and in-place mutations. Keep copies when mutation could destroy test inputs.

Develop dense assembly and an educational dense solver before sparse storage or sparse solvers.

Every solver needs a hand-solvable case, a residual check, an edge or failure case, an independent reference comparison when appropriate, and a stated tolerance. For `A @ x = b`, calculate `r = b - A @ x` and consider scaling, conditioning, singularity, and small pivots.
