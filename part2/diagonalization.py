"""Diagonalization: A = P D P^{-1}.

This implementation keeps the requested approach:
- Reuse Part 1 rank_and_basis to find eigenspaces from null spaces.
- Reuse Part 1 inverse to compute P^{-1}.
- For n >= 5, use numpy.linalg.eigvals as suggested by the addendum.
"""

from __future__ import annotations

import os
import sys
import unittest

import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from part1.inverse import inverse
from part1.rank_basis import rank_and_basis


def get_char_poly_coeffs(A: np.ndarray) -> list[float]:
    """Return characteristic polynomial coefficients via Faddeev-LeVerrier."""
    n = A.shape[0]
    coeffs = [1.0]
    B = np.zeros_like(A, dtype=float)

    for k in range(1, n + 1):
        Ak = A if k == 1 else A @ B
        ck = -float(np.trace(Ak)) / k
        coeffs.append(ck)
        B = Ak + ck * np.eye(n)

    return coeffs


def _dedup_eigenvalues(vals: np.ndarray, tol: float = 1e-7) -> list[float]:
    unique: list[float] = []
    for lam in vals:
        if abs(lam.imag) > 1e-8:
            raise ValueError(
                "Matrix has complex eigenvalues; current Part 1 basis/inverse pipeline supports real values only."
            )
        r = float(lam.real)
        if not any(abs(r - u) <= tol for u in unique):
            unique.append(r)
    return unique


def _is_independent(existing: list[np.ndarray], candidate: np.ndarray, tol: float = 1e-9) -> bool:
    if not existing:
        return True
    M_old = np.column_stack(existing)
    r_old = np.linalg.matrix_rank(M_old, tol=tol)
    M_new = np.column_stack(existing + [candidate])
    r_new = np.linalg.matrix_rank(M_new, tol=tol)
    return r_new > r_old


def diagonalize_matrix(A, cond_threshold: float = 1e8):
    """Diagonalize A and return (P, D, P_inv)."""
    A = np.array(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("Input matrix A must be square.")

    n = A.shape[0]
    if n >= 5:
        print(f"[*] n={n} >= 5, using numpy.linalg.eigvals as allowed by addendum.")
        eigvals = np.linalg.eigvals(A)
    else:
        eigvals = np.roots(get_char_poly_coeffs(A))

    unique_eigvals = _dedup_eigenvalues(np.array(eigvals, dtype=complex))

    p_cols: list[np.ndarray] = []
    d_diag: list[float] = []
    for lam in unique_eigvals:
        M = A - lam * np.eye(n)
        _, _, _, null_basis = rank_and_basis(M)

        for vec in null_basis:
            v = np.array(vec, dtype=float).reshape(-1)
            norm = float(np.linalg.norm(v))
            if norm <= 1e-12:
                continue
            v = v / norm

            if _is_independent(p_cols, v):
                p_cols.append(v)
                d_diag.append(lam)
            if len(p_cols) == n:
                break
        if len(p_cols) == n:
            break

    if len(p_cols) < n:
        raise ValueError(f"Matrix is not diagonalizable (found {len(p_cols)} independent eigenvectors, need {n}).")

    P = np.column_stack(p_cols)
    D = np.diag(d_diag)

    cond_p = float(np.linalg.cond(P))
    if (not np.isfinite(cond_p)) or cond_p > cond_threshold:
        raise ValueError(f"Matrix is not diagonalizable or numerically unstable (cond(P)={cond_p:.3e}).")

    P_inv = inverse(P)
    if P_inv is None:
        raise ValueError("Failed to invert P via Part 1 inverse implementation.")

    return P, D, np.array(P_inv, dtype=float)


def verify_diagonalization(A, P, D, P_inv, atol: float = 1e-5, rtol: float = 1e-5):
    A = np.array(A, dtype=float)
    A_hat = P @ D @ P_inv
    max_abs_error = float(np.max(np.abs(A - A_hat)))
    ok = bool(np.allclose(A, A_hat, atol=atol, rtol=rtol))
    return ok, max_abs_error


def matrix_power_via_diagonalization(A, k: int, cond_threshold: float = 1e8):
    if k < 0:
        raise ValueError("k must be a non-negative integer.")
    P, D, P_inv = diagonalize_matrix(A, cond_threshold=cond_threshold)
    Dk = np.diag(np.diag(D) ** k)
    return P @ Dk @ P_inv


class TestDiagonalization(unittest.TestCase):
    def test_tc1_spd_3x3(self):
        A = np.array([[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]])
        P, D, P_inv = diagonalize_matrix(A)
        ok, _ = verify_diagonalization(A, P, D, P_inv)
        self.assertTrue(ok)

    def test_tc2_diagonal(self):
        A = np.array([[5.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, 7.0]])
        P, D, P_inv = diagonalize_matrix(A)
        ok, _ = verify_diagonalization(A, P, D, P_inv)
        self.assertTrue(ok)

    def test_tc3_regular_2x2(self):
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        P, D, P_inv = diagonalize_matrix(A)
        ok, _ = verify_diagonalization(A, P, D, P_inv)
        self.assertTrue(ok)

    def test_tc4_jordan_not_diagonalizable(self):
        A = np.array([[1.0, 1.0], [0.0, 1.0]])
        with self.assertRaises(ValueError):
            diagonalize_matrix(A)

    def test_tc5_non_square(self):
        A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        with self.assertRaises(ValueError):
            diagonalize_matrix(A)

    def test_tc6_degree_ge_5_use_eigvals_path(self):
        np.random.seed(42)
        M = np.random.rand(5, 5)
        A = M @ M.T
        P, D, P_inv = diagonalize_matrix(A)
        ok, _ = verify_diagonalization(A, P, D, P_inv)
        self.assertTrue(ok)


class TestMatrixPower(unittest.TestCase):
    def test_tc1_power_spd(self):
        A = np.array([[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]])
        A_k = matrix_power_via_diagonalization(A, 3)
        self.assertTrue(np.allclose(A_k, np.linalg.matrix_power(A, 3), atol=1e-5, rtol=1e-5))

    def test_tc2_power_diagonal(self):
        A = np.array([[2.0, 0.0], [0.0, 3.0]])
        A_k = matrix_power_via_diagonalization(A, 5)
        self.assertTrue(np.allclose(A_k, np.linalg.matrix_power(A, 5), atol=1e-5, rtol=1e-5))

    def test_tc3_power_zero(self):
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        A_k = matrix_power_via_diagonalization(A, 0)
        self.assertTrue(np.allclose(A_k, np.eye(2), atol=1e-5, rtol=1e-5))

    def test_tc4_power_negative(self):
        with self.assertRaises(ValueError):
            matrix_power_via_diagonalization([[4.0, 1.0], [2.0, 3.0]], -2)

    def test_tc5_power_not_diagonalizable(self):
        with self.assertRaises(ValueError):
            matrix_power_via_diagonalization([[1.0, 1.0], [0.0, 1.0]], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
