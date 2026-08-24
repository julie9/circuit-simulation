# Book Overview

**Reference:** Farid N. Najm, *Circuit Simulation* (2010)

Najm's five chapters form the learning sequence for this project:

| Chapter | Main topics | Project result |
|---|---|---|
| 1. Introduction | Device equations, circuit formulation, solution techniques, and simulation modes | Validated circuit representation and read-only viewer |
| 2. Network Equations | Network graphs, KCL/KVL, nodal analysis, MNA, element groups, and stamps | Verified dense linear MNA assembly |
| 3. Linear Algebraic Equations | Substitution, Gaussian elimination, LU, pivoting, conditioning, and sparse methods | Educational dense LU solver with diagnostics |
| 4. Nonlinear Algebraic Equations | Residuals, Jacobians, Newton iteration, companion models, and convergence | Nonlinear DC operating-point solver |
| 5. Differential Circuit Equations | ODEs, DAEs, integration methods, companion models, and time-step control | Transient simulator with waveform output |

## Overall simulation flow

```text
netlist
  -> parser
  -> circuit and device records
  -> node and unknown indexing
  -> MNA assembly
  -> linear solve
  -> nonlinear Newton iteration
  -> transient time stepping
  -> results and plots
```

The complete book is kept outside normal source and documentation files when possible. Project notes should summarize concepts, record page references, and explain how the theory is translated into code without reproducing substantial copyrighted text.
