# Chapter 3: Educational Dense Linear Solver

## Purpose and prerequisites

This chapter turns an assembled MNA system into a numerical solution while
keeping the algorithm visible. The prerequisite is a dense system
`A @ x = b` from Chapter 2, together with basic matrix multiplication,
substitution, and floating-point arithmetic.

The solver is educational: NumPy is used for storage and reference checks,
but factorization and substitution are implemented explicitly in
`circuit_sim.solver`.

## Objects and conventions

The input dimensions are:

- `A`: `np.float64` square matrix with shape `(n, n)`;
- `b`: `np.float64` vector with shape `(n,)`;
- `x`: solution vector with shape `(n,)`.

The target equation is:

$$A x = b$$

Partial pivoting records a row permutation so that:

$$P A = L U$$

where `L` is unit lower triangular and `U` is upper triangular. The solve
sequence is:

1. Permute the right-hand side: `P @ b`.
2. Solve `L @ y = P @ b` by forward substitution.
3. Solve `U @ x = y` by backward substitution.
4. Calculate the residual `r = b - A @ x`.

The residual has the same units and shape as `b`. Its norm is a compact
diagnostic, but individual residual entries are useful when checking a circuit
equation or a badly scaled system.

## Worked two-by-two example

Consider:

$$
\begin{bmatrix}
2 & 1\\
4 & 3
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}5\\13\end{bmatrix}
$$

The first column has a larger pivot in row 2, so partial pivoting exchanges the
rows before elimination. After the swap, elimination produces a unit lower
factor and an upper factor satisfying `P @ A = L @ U`. Substitution then gives
`x = [1, 3]`. Multiplying the original matrix by this vector returns `[5, 13]`,
so the residual is zero up to floating-point roundoff.

The row exchange is not cosmetic. Without pivoting, a zero or very small
diagonal entry can cause division by zero or amplify roundoff even when the
matrix has a valid solution.

## Algorithm sketch

```text
U <- copy(A)
L <- identity(n)
permutation <- [0, 1, ..., n-1]

for column in 0 .. n-1:
    pivot_row <- row with largest absolute U[row, column]
    reject pivot if it is unusably small
    swap rows of U, prior columns of L, and permutation
    for row below pivot:
        L[row, column] <- U[row, column] / U[column, column]
        subtract multiplier * pivot row from U[row]

y <- forward_substitution(L, b[permutation])
x <- backward_substitution(U, y)
r <- b - A @ x
```

The row swaps in `L` are restricted to columns before the current pivot. Those
columns already contain elimination multipliers; swapping all of `L` would
destroy the factorization invariant.

## Numerical risks and failure behavior

- A zero pivot means the matrix is singular for this factorization path.
- A very small pivot relative to the matrix scale is treated as unusable by
  `pivot_tolerance`.
- Shape and finite-value checks reject malformed numerical inputs early.
- A small residual supports correctness but does not prove a matrix is well
  conditioned; conditioning is a later diagnostic concern.
- The current solver is dense and intended for small educational circuits.
  Sparse storage and sparse factorization are outside this milestone.

## Project interface

`solve_linear_system(A, b)` returns a dictionary containing `solution`,
`residual`, `residual_norm`, `lower`, `upper`, and `permutation`. The lower and
upper factors are exposed so the learning code and tests can inspect the
factorization rather than treating it as a black box.

## Comprehension check

1. Why must the right-hand side be permuted when the rows of `A` are swapped?
2. Why are only the already-computed columns of `L` swapped during pivoting?
3. What can a small residual tell us, and what can it not tell us about
   conditioning?

Do not advance to nonlinear iteration until these questions can be answered in
your own words.