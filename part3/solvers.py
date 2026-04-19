import os
import sys
import unittest
import math
from numbers import Real

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from part1.gaussian import gaussian_eliminate
from part1.matrix_utils import matmul, matvec, to_matrix, to_vector, transpose
from part2.decomposition import cholesky_custom


def forward_substitution(L, b):
    n = len(b)
    y = [0.0] * n
    eps = 1e-12
    for i in range(n):
        if abs(L[i][i]) <= eps:
            raise ValueError("ma tran tam giac duoi suy bien")
        s = 0.0
        for j in range(i):
            s += L[i][j] * y[j]
        y[i] = (b[i] - s) / L[i][i]
    return y


def backward_substitution(U, y):
    n = len(y)
    x = [0.0] * n
    eps = 1e-12
    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) <= eps:
            raise ValueError("ma tran tam giac tren suy bien")
        s = 0.0
        for j in range(i + 1, n):
            s += U[i][j] * x[j]
        x[i] = (y[i] - s) / U[i][i]
    return x


def solve_via_gauss(A, b):
    A_list = to_matrix(A, error_message="Ma tran dau vao phai khong rong va co dang chu nhat.")
    b_list = to_vector(b)
    _, x, _ = gaussian_eliminate(A_list, b_list, verbose=False)
    n_cols = len(A_list[0])
    # gaussian_eliminate tra ve bieu dien tham so cho he khong co nghiem duy nhat.
    # Trong Phan 3, solver nay chi chap nhan vector nghiem so duy nhat.
    if (
        x is None
        or not isinstance(x, list)
        or len(x) != n_cols
        or any(not isinstance(v, Real) for v in x)
    ):
        raise ValueError("he khong co nghiem duy nhat")
    return [float(v) for v in x]


def solve_via_cholesky(A, b):
    A_list = to_matrix(A, require_square=True, error_message="Ma tran dau vao phai la ma tran vuong khong rong.")
    b_list = to_vector(b)
    if len(b_list) != len(A_list):
        raise ValueError("kich thuoc b khong phu hop voi A")
    L = cholesky_custom(A_list)
    y = forward_substitution(L, b_list)
    x = backward_substitution(transpose(L), y)
    return x


def solve_via_normal_equations(A, b):
    A_list = to_matrix(A, error_message="Ma tran dau vao phai khong rong va co dang chu nhat.")
    b_list = to_vector(b)
    if len(b_list) != len(A_list):
        raise ValueError("kich thuoc b khong phu hop voi A")

    A_t = transpose(A_list)
    M = matmul(A_t, A_list)
    c = matvec(A_t, b_list)

    L = cholesky_custom(M)
    y = forward_substitution(L, c)
    x = backward_substitution(transpose(L), y)
    return x


def _is_strictly_diagonally_dominant(A, eps=1e-12):
    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        off_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= off_sum + eps:
            return False
    return True


def solve_gauss_seidel(
    A,
    b,
    x0=None,
    tolerance=1e-10,
    max_iterations=1000,
    require_convergence_check=True,
    strict_convergence=False,
    verbose=True,
):
    """
    Giai he phuong trinh tuyen tinh Ax = b bang phuong phap lap Gauss-Seidel.
    (Phien ban thuan Python, khong su dung thu vien ngoai)
    """
    A_list = to_matrix(A, require_square=True, error_message="Ma tran dau vao phai la ma tran vuong khong rong.")
    b_list = to_vector(b)
    n = len(A_list)
    if len(b_list) != n:
        raise ValueError("kich thuoc b khong phu hop voi A")

    eps = 1e-12
    for i in range(n):
        if abs(A_list[i][i]) <= eps:
            raise ValueError("he co phan tu duong cheo bang 0, khong the ap dung Gauss-Seidel")

    if require_convergence_check and not _is_strictly_diagonally_dominant(A_list):
        msg = "Gauss-Seidel khong duoc dam bao hoi tu (ma tran khong cheo troi chat)."
        if strict_convergence:
            raise ValueError(msg)
        if verbose:
            print(f"[Gauss-Seidel] Canh bao: {msg}")

    # 1. Khoi tao vector nghiem ban dau
    if x0 is None:
        x = [0.0] * n
    else:
        x = to_vector(x0)
        if len(x) != n:
            raise ValueError("kich thuoc x0 khong phu hop voi A")
        if any(not math.isfinite(value) for value in x):
            raise ValueError("x0 phai chua cac gia tri huu han")
    
    for k in range(max_iterations):
        max_diff = 0.0

        for i in range(n):
            row_i = A_list[i]
            lower_sum = 0.0
            for j in range(i):
                lower_sum += row_i[j] * x[j]

            upper_sum = 0.0
            for j in range(i + 1, n):
                upper_sum += row_i[j] * x[j]

            old_xi = x[i]
            new_xi = (b_list[i] - lower_sum - upper_sum) / row_i[i]
            if not math.isfinite(new_xi):
                raise OverflowError("Gauss-Seidel phan ky hoac tran so")
            x[i] = new_xi

            diff = abs(new_xi - old_xi)
            if diff > max_diff:
                max_diff = diff

        if not math.isfinite(max_diff):
            raise OverflowError("Gauss-Seidel phan ky hoac tran so")
        
        if max_diff < tolerance:
            if verbose:
                print(f"[Gauss-Seidel] Da hoi tu sau {k+1} vong lap.")
            return x

        if any(not math.isfinite(value) for value in x):
            raise OverflowError("Gauss-Seidel phan ky hoac tran so")
            
    if verbose:
        print("[Gauss-Seidel] Canh bao: Vuot qua so vong lap toi da ma chua hoi tu.")
    return x

