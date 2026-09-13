# Chapter 4: Nonlinear DC Analysis

## First increment

This increment adds a diode-only DC operating-point solver. Resistors,
independent sources, ideal inductors, and open-circuit capacitors retain their
Chapter 2 behavior. Three-terminal semiconductor records remain deferred until
their terminal conventions and device equations are introduced.

## Purpose and prerequisites

The linear MNA system from Chapter 2 assumes every element contributes a fixed
stamp. A diode violates that assumption: its current depends nonlinearly on
the terminal voltage. Chapter 4 replaces one fixed solve with repeated local
linearizations and solves until the physical residual is small.

Prerequisites are nodal/MNA stamping, the Chapter 3 dense solver, derivatives,
and the meaning of a residual. The unknown vector still contains node voltages
and ideal branch currents.

## Diode model

For diode voltage $v_D=V_p-V_n$, the Shockley model used here is:

$$I_D(v_D)=s I_S\left(e^{v_D/V_T}-1\right)$$

where `s` is the parsed scale, $I_S=10^{-14}$ A is the default saturation
current, and $V_T=0.02585$ V is the default thermal voltage. Its Jacobian is:

$$G_D(v_D)=\frac{\partial I_D}{\partial v_D}
=\frac{s I_S}{V_T}e^{v_D/V_T}$$

The implementation clips the exponential argument at an upper bound to avoid
floating-point overflow. This protects the iteration but does not replace a
physical model for temperature, series resistance, or breakdown.

## Newton companion stamp

At iterate $v_D^{(k)}$, linearize the diode current:

$$I_D(v)\approx G_D^{(k)}v+I_{eq}^{(k)}$$

with:

$$I_{eq}^{(k)}=I_D(v_D^{(k)})-G_D^{(k)}v_D^{(k)}$$

The conductance $G_D^{(k)}$ receives the ordinary two-terminal conductance
stamp. The equivalent current source $I_{eq}^{(k)}$ uses the project's positive
terminal to negative terminal convention. Solving this linearized system gives
the next Newton candidate.

## Iteration and convergence

```text
solution <- initial guess, or zero vector
repeat until max_iterations:
    assemble linear MNA system using diode tangents at solution
    solve the linear system for raw_candidate
    backtrack candidate toward solution until physical residual decreases
    residual <- KCL and branch-constraint residual at candidate
    stop when step and residual meet their tolerances
raise a convergence error if the iteration limit is reached
```

The residual is evaluated from the original nonlinear device equations, not
only from the linearized matrix. This distinction matters: a linearized solve
can have a tiny algebraic residual while the original diode equation is still
unsatisfied.

## Numerical risks and limitations

- The exponential can overflow, so the model clips its exponent.
- An undamped Newton step can overshoot the diode knee; residual-decreasing
  backtracking is used in this increment.
- A small residual does not establish model accuracy or good conditioning.
- The default diode parameters are educational constants, not a device library.
- BJT/MOS models, source stepping, temperature dependence, and continuation
  are future work.

## Comprehension check

1. Why does the diode contribute both a conductance and an equivalent current
   source during Newton iteration?
2. Why must convergence be checked against the original nonlinear residual?
3. What problem does backtracking address, and what model limitation does it
   not solve?

Answer these questions before treating the diode increment as a complete
nonlinear device framework.