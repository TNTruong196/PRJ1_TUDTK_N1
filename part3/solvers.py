import os
import sys
import unittest

import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from part1.gaussian import gaussian_eliminate
from part2.decomposition import cholesky_custom


def forward_substitution(L, b):
    n = len(b)
    y = np.zeros(n, dtype=float)
    eps = 1e-12
    for i in range(n):
        if abs(L[i, i]) <= eps:
            raise ValueError("ma tran tam giac duoi suy bien")
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    return y


def backward_substitution(U, y):
    n = len(y)
    x = np.zeros(n, dtype=float)
    eps = 1e-12
    for i in range(n - 1, -1, -1):
        if abs(U[i, i]) <= eps:
            raise ValueError("ma tran tam giac tren suy bien")
        x[i] = (y[i] - np.dot(U[i, i + 1 :], x[i + 1 :])) / U[i, i]
    return x


def solve_via_gauss(A, b):
    A_list = np.array(A, dtype=float).tolist()
    b_list = np.array(b, dtype=float).flatten().tolist()
    _, x, _ = gaussian_eliminate(A_list, b_list)
    if x is None:
        raise ValueError("he khong co nghiem duy nhat")
    return np.array(x, dtype=float)


def solve_via_cholesky(A, b):
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float).flatten()
    L = np.array(cholesky_custom(A_np.tolist()), dtype=float)
    y = forward_substitution(L, b_np)
    x = backward_substitution(L.T, y)
    return x


def solve_via_normal_equations(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).flatten()

    M = A.T @ A
    c = A.T @ b

    L = np.array(cholesky_custom(M.tolist()), dtype=float)
    y = forward_substitution(L, c)
    x = backward_substitution(L.T, y)
    return x


class TestCholeskySolvers(unittest.TestCase):
    def setUp(self):
        self.A_spd = np.array([[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]])
        self.b_spd = np.array([1.0, 2.0, 3.0])

        self.A_diag = np.diag([2.0, 5.0, 10.0])
        self.b_diag = np.array([4.0, 10.0, -20.0])

        self.b_zero = np.zeros(3)

        self.A_large = self.A_spd * 10000.0
        self.b_large = self.b_spd * 10000.0

        self.A_square = np.array([[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]])
        self.b_square = np.array([5.0, -2.0, 9.0])

        self.A_rect = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        self.b_rect = np.array([1.0, 2.0, 3.0])

        self.A_dependent = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])
        self.b_dependent = np.array([1.0, 2.0, 3.0])

    def test_01_cholesky_standard(self):
        x = solve_via_cholesky(self.A_spd, self.b_spd)
        np.testing.assert_allclose(self.A_spd @ x, self.b_spd, atol=1e-5)

    def test_02_cholesky_diagonal(self):
        x = solve_via_cholesky(self.A_diag, self.b_diag)
        np.testing.assert_allclose(self.A_diag @ x, self.b_diag, atol=1e-5)

    def test_03_cholesky_zero_b(self):
        x = solve_via_cholesky(self.A_spd, self.b_zero)
        np.testing.assert_allclose(self.A_spd @ x, self.b_zero, atol=1e-5)

    def test_04_cholesky_large_values(self):
        x = solve_via_cholesky(self.A_large, self.b_large)
        np.testing.assert_allclose(self.A_large @ x, self.b_large, atol=1e-5)

    def test_05_cholesky_fail_non_spd(self):
        with self.assertRaises(ValueError):
            solve_via_cholesky(self.A_square, self.b_square)

    def test_06_normal_eq_square(self):
        x = solve_via_normal_equations(self.A_square, self.b_square)
        np.testing.assert_allclose(self.A_square @ x, self.b_square, atol=1e-5)

    def test_07_normal_eq_rect(self):
        x = solve_via_normal_equations(self.A_rect, self.b_rect)
        np.testing.assert_allclose(self.A_rect.T @ self.A_rect @ x, self.A_rect.T @ self.b_rect, atol=1e-5)

    def test_08_normal_eq_spd(self):
        x = solve_via_normal_equations(self.A_spd, self.b_spd)
        np.testing.assert_allclose(self.A_spd @ x, self.b_spd, atol=1e-5)

    def test_09_normal_eq_zero_b(self):
        x = solve_via_normal_equations(self.A_square, self.b_zero)
        np.testing.assert_allclose(self.A_square @ x, self.b_zero, atol=1e-5)

    def test_10_normal_eq_fail_dependent_cols(self):
        with self.assertRaises(ValueError):
            solve_via_normal_equations(self.A_dependent, self.b_dependent)

    def test_11_gauss_square(self):
        x = solve_via_gauss(self.A_square, self.b_square)
        np.testing.assert_allclose(self.A_square @ x, self.b_square, atol=1e-5)

    def test_12_gauss_requires_pivot(self):
        A_pivot = np.array([[0.0, 2.0], [3.0, 4.0]])
        b_pivot = np.array([4.0, 11.0])
        x = solve_via_gauss(A_pivot, b_pivot)
        np.testing.assert_allclose(A_pivot @ x, b_pivot, atol=1e-5)

    def test_13_gauss_spd(self):
        x = solve_via_gauss(self.A_spd, self.b_spd)
        np.testing.assert_allclose(self.A_spd @ x, self.b_spd, atol=1e-5)

    def test_14_gauss_zero_b(self):
        x = solve_via_gauss(self.A_square, self.b_zero)
        np.testing.assert_allclose(self.A_square @ x, self.b_zero, atol=1e-5)

    def test_15_gauss_singular(self):
        with self.assertRaises(ValueError):
            solve_via_gauss(self.A_dependent, self.b_dependent)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
