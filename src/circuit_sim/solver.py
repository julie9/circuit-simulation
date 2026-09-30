"""Educational dense linear algebra for Chapter 3 circuits."""

import numpy as np


def _as_square_matrix(matrix):
    values = np.asarray(matrix, dtype=np.float64)
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("matrix must be a square two-dimensional array")
    return values


def _as_vector(vector, size, name):
    values = np.asarray(vector, dtype=np.float64)
    if values.ndim != 1 or values.shape[0] != size:
        raise ValueError(f"{name} must be a one-dimensional vector of length {size}")
    return values


def forward_substitution(lower, rhs):
    """Solve ``L @ y = rhs`` for a unit lower-triangular matrix ``L``."""
    lower = _as_square_matrix(lower)
    rhs = _as_vector(rhs, lower.shape[0], "rhs")
    solution = np.zeros_like(rhs)
    for row in range(lower.shape[0]):
        solution[row] = rhs[row] - lower[row, :row] @ solution[:row]
    return solution


def backward_substitution(upper, rhs, pivot_tolerance=1e-12):
    """Solve ``U @ x = rhs`` for an upper-triangular matrix ``U``."""
    upper = _as_square_matrix(upper)
    rhs = _as_vector(rhs, upper.shape[0], "rhs")
    solution = np.zeros_like(rhs)
    scale = max(1.0, np.max(np.abs(upper))) if upper.size else 1.0
    threshold = pivot_tolerance * scale
    for row in range(upper.shape[0] - 1, -1, -1):
        pivot = upper[row, row]
        if abs(pivot) <= threshold:
            raise np.linalg.LinAlgError("matrix has a singular or unusable pivot")
        solution[row] = (rhs[row] - upper[row, row + 1:] @ solution[row + 1:]) / pivot
    return solution


def lu_factor(matrix, pivot_tolerance=1e-12):
    """Factor a dense square matrix and return ``P @ A = L @ U`` data."""
    matrix = _as_square_matrix(matrix)
    if not np.all(np.isfinite(matrix)):
        raise ValueError("matrix must contain only finite values")
    if pivot_tolerance < 0:
        raise ValueError("pivot_tolerance must be non-negative")

    size = matrix.shape[0]
    upper = matrix.copy()
    lower = np.eye(size, dtype=np.float64)
    permutation = np.arange(size)
    scale = max(1.0, np.max(np.abs(matrix))) if matrix.size else 1.0
    threshold = pivot_tolerance * scale

    for column in range(size):
        pivot_row = column + np.argmax(np.abs(upper[column:, column]))
        pivot = upper[pivot_row, column]
        if abs(pivot) <= threshold:
            raise np.linalg.LinAlgError("matrix has a singular or unusable pivot")
        if pivot_row != column:
            upper[[column, pivot_row], :] = upper[[pivot_row, column], :]
            if column:
                lower[[column, pivot_row], :column] = lower[[pivot_row, column], :column]
            permutation[[column, pivot_row]] = permutation[[pivot_row, column]]
        for row in range(column + 1, size):
            lower[row, column] = upper[row, column] / upper[column, column]
            upper[row, column:] -= lower[row, column] * upper[column, column:]
            upper[row, column] = 0.0

    return {
        "lower": lower,
        "upper": upper,
        "permutation": permutation,
    }


def solve_linear_system(matrix, rhs, pivot_tolerance=1e-12):
    """Solve ``A @ x = b`` with educational dense LU and report diagnostics."""
    matrix = _as_square_matrix(matrix)
    rhs = _as_vector(rhs, matrix.shape[0], "rhs")
    if not np.all(np.isfinite(rhs)):
        raise ValueError("rhs must contain only finite values")
    factorization = lu_factor(matrix, pivot_tolerance)
    permuted_rhs = rhs[factorization["permutation"]]
    intermediate = forward_substitution(factorization["lower"], permuted_rhs)
    solution = backward_substitution(
        factorization["upper"], intermediate, pivot_tolerance
    )
    residual = rhs - matrix @ solution
    return {
        "solution": solution,
        "residual": residual,
        "residual_norm": np.linalg.norm(residual),
        **factorization,
    }