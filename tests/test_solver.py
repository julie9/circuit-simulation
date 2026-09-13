import numpy as np
import pytest

from circuit_sim.solver import (
    backward_substitution,
    forward_substitution,
    lu_factor,
    solve_linear_system,
)


def test_forward_and_backward_substitution():
    lower = np.array([[1.0, 0.0], [2.0, 1.0]])
    upper = np.array([[2.0, 1.0], [0.0, 3.0]])

    np.testing.assert_allclose(forward_substitution(lower, [4.0, 10.0]), [4.0, 2.0])
    np.testing.assert_allclose(backward_substitution(upper, [5.0, 6.0]), [1.5, 2.0])


def test_lu_factorization_reconstructs_permuted_matrix():
    matrix = np.array([[0.0, 2.0], [1.0, 3.0]])

    factorization = lu_factor(matrix)
    permutation = factorization["permutation"]

    np.testing.assert_allclose(
        matrix[permutation],
        factorization["lower"] @ factorization["upper"],
    )
    assert factorization["lower"].dtype == np.float64
    assert factorization["upper"].dtype == np.float64


def test_solve_linear_system_reports_solution_and_residual():
    matrix = np.array([
        [0.001, -0.001, 1.0],
        [-0.001, 0.0015, 0.0],
        [1.0, 0.0, 0.0],
    ])
    rhs = np.array([0.0, -0.001, 5.0])

    result = solve_linear_system(matrix, rhs)

    np.testing.assert_allclose(result["solution"], [5.0, 8.0 / 3.0, -7.0 / 3000.0])
    np.testing.assert_allclose(result["residual"], [0.0, 0.0, 0.0], atol=1e-15)
    assert result["residual_norm"] < 1e-12


def test_solver_matches_independent_numpy_reference():
    matrix = np.array([
        [4.0, -1.0, 2.0],
        [3.0, 6.0, -4.0],
        [2.0, 1.0, 8.0],
    ])
    rhs = np.array([12.0, -25.0, 32.0])

    result = solve_linear_system(matrix, rhs)

    np.testing.assert_allclose(result["solution"], np.linalg.solve(matrix, rhs))


@pytest.mark.parametrize("matrix", [
    [[1.0, 2.0], [2.0, 4.0]],
    [[1.0, 0.0], [0.0, 0.0]],
])
def test_singular_matrix_is_rejected(matrix):
    with pytest.raises(np.linalg.LinAlgError, match="singular or unusable pivot"):
        lu_factor(matrix)


def test_invalid_shapes_and_nonfinite_values_are_rejected():
    with pytest.raises(ValueError, match="square"):
        solve_linear_system([[1.0, 2.0]], [1.0])
    with pytest.raises(ValueError, match="finite"):
        solve_linear_system([[np.inf]], [1.0])
    with pytest.raises(ValueError, match="finite"):
        solve_linear_system([[1.0]], [np.nan])