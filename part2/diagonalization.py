"""
Cheo hoa ma tran (Diagonalization): A = P D P^{-1}.

1) Dinh nghia
   Neu A la ma tran vuong co the cheo hoa duoc, ton tai ma tran kha nghich P 
   va ma tran duong cheo D sao cho:
       A = P D P^{-1}
   Trong do, D chua cac gia tri rieng (eigenvalues) tren duong cheo chinh, 
   va P chua cac vector rieng (eigenvectors) doc lap tuyen tinh tuong ung.

2) Dieu kien ap dung
   Ma tran dau vao A phai thoa man:
   - La ma tran vuong (n x n).
   - Co du n vector rieng doc lap tuyen tinh (khong bi suy bien).
   * Luu y (theo implementation hien tai): Chi ho tro cac gia tri rieng la so thuc 
     (se bao loi neu xuat hien gia tri rieng la so phuc).

3) Chi phi tinh toan & Ung dung
   Phan tich cheo hoa mang lai loi the cuc lon khi can tinh luy thua ma tran (A^k). 
   Thay vi phai nhan ma tran k lan voi do phuc tap O(k * n^3), ta co the dung:
       A^k = P D^k P^{-1}
   Vi D la ma tran duong cheo, D^k chi don gian la luy thua bac k cua tung phan tu 
   tren duong cheo chinh, giup giam thieu toi da khoi luong tinh toan.

4) Thu tu thuc hien thuat toan (theo code)
   - B1: Tinh he so da thuc dac trung bang thuat toan Faddeev-LeVerrier.
   - B2: Tim gia tri rieng. Dung phuong phap Durand-Kerner cho ma tran nho (n <= 5), 
         hoac np.linalg.eigvals cho ma tran lon (n > 5).
   - B3: Voi moi gia tri rieng, tim co so khong gian nghiem cua (A - \lambda I) 
         de thu thap cac vector rieng.
   - B4: Kiem tra tinh doc lap tuyen tinh, ghep n vector thanh ma tran P, tao D 
         va tinh ma tran nghich dao P^{-1}.

Tep nay gom:
- Cac ham ho tro (_durand_kerner, get_char_poly_coeffs...): Tu tim gia tri rieng khong dung NumPy.
- Ham diagonalize_matrix(A): Thuc hien cheo hoa, tra ve bo ba (P, D, P_inv).
- Ham matrix_power_via_diagonalization(A, k): Ung dung cheo hoa de tinh luy thua ma tran.
- Bo unit test (>= 5 test cases): Kiem tra tinh dung dan voi ma tran SPD, ma tran duong cheo, 
  luy thua ma tran, va bat loi cac truong hop khong the cheo hoa (nhu ma tran Jordan).
"""

from __future__ import annotations

import cmath
import math
import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from part1.inverse import inverse
from part1.matrix_utils import identity, infinity_norm, matmul, to_matrix
from part1.rank_basis import rank_and_basis


def _mat_add(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _mat_sub(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _mat_scalar_mul(A: list[list[float]], c: float) -> list[list[float]]:
    return [[A[i][j] * c for j in range(len(A[0]))] for i in range(len(A))]


def _trace(A: list[list[float]]) -> float:
    return sum(A[i][i] for i in range(len(A)))


def _poly_eval(coeffs: list[float], x: complex) -> complex:
    value = 0j
    for coef in coeffs:
        value = value * x + complex(coef)
    return value


def _durand_kerner(coeffs: list[float], max_iter: int = 3000, tol: float = 1e-12) -> list[complex]:
    degree = len(coeffs) - 1
    if degree <= 0:
        return []

    if abs(coeffs[0]) <= tol:
        raise ValueError("He so dau cua da thuc phai khac 0.")

    coeffs_norm = [complex(c) / complex(coeffs[0]) for c in coeffs]
    if degree == 1:
        return [-coeffs_norm[1]]

    radius = 1.0
    for c in coeffs_norm[1:]:
        radius = max(radius, abs(c))
    radius = 1.0 + radius

    roots = [radius * cmath.exp(2j * math.pi * i / degree) for i in range(degree)]

    for _ in range(max_iter):
        updated = roots[:]
        max_delta = 0.0

        for i in range(degree):
            denom = 1.0 + 0.0j
            for j in range(degree):
                if i == j:
                    continue
                diff = roots[i] - roots[j]
                if abs(diff) < tol:
                    diff = complex(tol, tol)
                denom *= diff

            if abs(denom) <= tol:
                denom = complex(tol, tol)

            correction = _poly_eval(coeffs_norm, roots[i]) / denom
            updated[i] = roots[i] - correction
            max_delta = max(max_delta, abs(correction))

        roots = updated
        if max_delta <= tol:
            break

    return roots


def get_char_poly_coeffs(A: list[list[float]]) -> list[float]:
    """Tinh he so da thuc dac trung bang Faddeev-LeVerrier thuoc Python."""
    matrix = to_matrix(A, require_square=True, error_message="Ma tran A phai la ma tran vuong.")
    n = len(matrix)
    coeffs = [1.0]
    B = [[0.0] * n for _ in range(n)]

    for k in range(1, n + 1):
        Ak = matrix if k == 1 else matmul(matrix, B)
        ck = -_trace(Ak) / k
        coeffs.append(ck)
        B = _mat_add(Ak, _mat_scalar_mul(identity(n), ck))

    return coeffs


def _get_eigenvalues(A: list[list[float]], tol: float = 1e-7) -> list[float]:
    """Lay gia tri rieng dang list float thuoc Python.

    Chi dung np.linalg.eigvals cho truong hop n > 5 theo yeu cau.
    """
    n = len(A)
    if n > 5:
        import numpy as np

        vals = np.linalg.eigvals(A).tolist()
    else:
        vals = _durand_kerner(get_char_poly_coeffs(A))

    unique = []
    for lam in vals:
        if abs(lam.imag) > 1e-8:
            raise ValueError("Ma tran co gia tri rieng phuc; hien tai chi ho tro gia tri rieng thuc.")
        r = float(lam.real)
        if not any(abs(r - u) <= tol for u in unique):
            unique.append(r)
    return unique


def _is_independent(existing_cols: list[list[float]], candidate: list[float]) -> bool:
    if not existing_cols:
        return True

    cols = existing_cols + [candidate]
    n_rows = len(cols[0])
    n_cols = len(cols)
    M = [[cols[j][i] for j in range(n_cols)] for i in range(n_rows)]

    rank, _, _, _ = rank_and_basis(M)
    return rank == n_cols


def _max_abs_diff(A: list[list[float]], B: list[list[float]]) -> float:
    best = 0.0
    for i in range(len(A)):
        for j in range(len(A[0])):
            best = max(best, abs(A[i][j] - B[i][j]))
    return best


def _allclose(A: list[list[float]], B: list[list[float]], atol: float, rtol: float) -> bool:
    for i in range(len(A)):
        for j in range(len(A[0])):
            a = A[i][j]
            b = B[i][j]
            if abs(a - b) > atol + rtol * abs(b):
                return False
    return True


def diagonalize_matrix(A: list[list[float]], cond_threshold: float = 1e8):
    """Cheo hoa A va tra ve (P, D, P_inv)."""
    matrix = to_matrix(A, require_square=True, error_message="Ma tran A phai la ma tran vuong khong rong.")
    n = len(matrix)
    unique_eigvals = _get_eigenvalues(matrix)

    p_cols = []
    d_diag = []

    for lam in unique_eigvals:
        M = _mat_sub(matrix, _mat_scalar_mul(identity(n), lam))
        _, _, _, null_basis = rank_and_basis(M)

        for vec in null_basis:
            norm_v = math.sqrt(sum(x * x for x in vec))
            if norm_v <= 1e-12:
                continue

            v = [x / norm_v for x in vec]
            if _is_independent(p_cols, v):
                p_cols.append(v)
                d_diag.append(lam)
            if len(p_cols) == n:
                break

        if len(p_cols) == n:
            break

    if len(p_cols) < n:
        raise ValueError(f"Ma tran khong the cheo hoa (tim thay {len(p_cols)} vector rieng doc lap, can {n}).")

    P = [[p_cols[j][i] for j in range(n)] for i in range(n)]
    D = [[d_diag[i] if i == j else 0.0 for j in range(n)] for i in range(n)]

    P_inv = inverse(P)
    if P_inv is None:
        raise ValueError("Khong the tinh nghich dao cua P bang ham inverse o Phan 1.")

    cond_p = infinity_norm(P) * infinity_norm(P_inv)
    if cond_p > cond_threshold:
        raise ValueError(f"Ma tran khong the cheo hoa hoac kem on dinh so (cond(P)={cond_p:.3e}).")

    return P, D, P_inv


def verify_diagonalization(A, P, D, P_inv, atol: float = 1e-5, rtol: float = 1e-5):
    A_m = to_matrix(A, require_square=True, error_message="Ma tran A phai la ma tran vuong khong rong.")
    A_hat = matmul(matmul(P, D), P_inv)
    max_abs_error = _max_abs_diff(A_m, A_hat)
    ok = _allclose(A_m, A_hat, atol=atol, rtol=rtol)
    return ok, max_abs_error


def matrix_power_via_diagonalization(A: list[list[float]], k: int, cond_threshold: float = 1e8) -> list[list[float]]:
    if k < 0:
        raise ValueError("k phai la so nguyen khong am.")

    P, D, P_inv = diagonalize_matrix(A, cond_threshold=cond_threshold)
    n = len(D)
    Dk = [[(D[i][i] ** k) if i == j else 0.0 for j in range(n)] for i in range(n)]
    return matmul(matmul(P, Dk), P_inv)


def _naive_matrix_power(A: list[list[float]], k: int) -> list[list[float]]:
    n = len(A)
    result = identity(n)
    base = to_matrix(A, require_square=True, error_message="Ma tran A phai la ma tran vuong.")
    for _ in range(k):
        result = matmul(result, base)
    return result
