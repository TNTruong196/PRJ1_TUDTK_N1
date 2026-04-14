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
    A_list = to_matrix(A, error_message="Input matrix must be non-empty and rectangular.")
    b_list = to_vector(b)
    _, x, _ = gaussian_eliminate(A_list, b_list, verbose=False)
    n_cols = len(A_list[0])
    # gaussian_eliminate returns a parametric expression for non-unique systems.
    # In Part 3, this solver only accepts a unique numeric solution vector.
    if (
        x is None
        or not isinstance(x, list)
        or len(x) != n_cols
        or any(not isinstance(v, Real) for v in x)
    ):
        raise ValueError("he khong co nghiem duy nhat")
    return [float(v) for v in x]


def solve_via_cholesky(A, b):
    A_list = to_matrix(A, require_square=True, error_message="Input matrix must be a non-empty square matrix.")
    b_list = to_vector(b)
    if len(b_list) != len(A_list):
        raise ValueError("kich thuoc b khong phu hop voi A")
    L = cholesky_custom(A_list)
    y = forward_substitution(L, b_list)
    x = backward_substitution(transpose(L), y)
    return x


def solve_via_normal_equations(A, b):
    A_list = to_matrix(A, error_message="Input matrix must be non-empty and rectangular.")
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


class TestCholeskySolvers(unittest.TestCase):
    def setUp(self):
        self.A_spd = [[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]]
        self.b_spd = [1.0, 2.0, 3.0]

        self.A_diag = [[2.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 10.0]]
        self.b_diag = [4.0, 10.0, -20.0]

        self.b_zero = [0.0, 0.0, 0.0]

        self.A_large = [[value * 10000.0 for value in row] for row in self.A_spd]
        self.b_large = [value * 10000.0 for value in self.b_spd]

        self.A_square = [[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]]
        self.b_square = [5.0, -2.0, 9.0]

        self.A_rect = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
        self.b_rect = [1.0, 2.0, 3.0]

        self.A_dependent = [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]
        self.b_dependent = [1.0, 2.0, 3.0]

    def test_01_cholesky_standard(self):
        import numpy as np

        x = solve_via_cholesky(self.A_spd, self.b_spd)
        np.testing.assert_allclose(np.matmul(self.A_spd, x), self.b_spd, atol=1e-5)

    def test_02_cholesky_diagonal(self):
        import numpy as np

        x = solve_via_cholesky(self.A_diag, self.b_diag)
        np.testing.assert_allclose(np.matmul(self.A_diag, x), self.b_diag, atol=1e-5)

    def test_03_cholesky_zero_b(self):
        import numpy as np

        x = solve_via_cholesky(self.A_spd, self.b_zero)
        np.testing.assert_allclose(np.matmul(self.A_spd, x), self.b_zero, atol=1e-5)

    def test_04_cholesky_large_values(self):
        import numpy as np

        x = solve_via_cholesky(self.A_large, self.b_large)
        np.testing.assert_allclose(np.matmul(self.A_large, x), self.b_large, atol=1e-5)

    def test_05_cholesky_fail_non_spd(self):
        with self.assertRaises(ValueError):
            solve_via_cholesky(self.A_square, self.b_square)

    def test_06_normal_eq_square(self):
        import numpy as np

        x = solve_via_normal_equations(self.A_square, self.b_square)
        np.testing.assert_allclose(np.matmul(self.A_square, x), self.b_square, atol=1e-5)

    def test_07_normal_eq_rect(self):
        import numpy as np

        x = solve_via_normal_equations(self.A_rect, self.b_rect)
        left = np.matmul(np.matmul(np.transpose(self.A_rect), self.A_rect), x)
        right = np.matmul(np.transpose(self.A_rect), self.b_rect)
        np.testing.assert_allclose(left, right, atol=1e-5)

    def test_08_normal_eq_spd(self):
        import numpy as np

        x = solve_via_normal_equations(self.A_spd, self.b_spd)
        np.testing.assert_allclose(np.matmul(self.A_spd, x), self.b_spd, atol=1e-5)

    def test_09_normal_eq_zero_b(self):
        import numpy as np

        x = solve_via_normal_equations(self.A_square, self.b_zero)
        np.testing.assert_allclose(np.matmul(self.A_square, x), self.b_zero, atol=1e-5)

    def test_10_normal_eq_fail_dependent_cols(self):
        with self.assertRaises(ValueError):
            solve_via_normal_equations(self.A_dependent, self.b_dependent)

    def test_11_gauss_square(self):
        import numpy as np

        x = solve_via_gauss(self.A_square, self.b_square)
        np.testing.assert_allclose(np.matmul(self.A_square, x), self.b_square, atol=1e-5)

    def test_12_gauss_requires_pivot(self):
        import numpy as np

        A_pivot = [[0.0, 2.0], [3.0, 4.0]]
        b_pivot = [4.0, 11.0]
        x = solve_via_gauss(A_pivot, b_pivot)
        np.testing.assert_allclose(np.matmul(A_pivot, x), b_pivot, atol=1e-5)

    def test_13_gauss_spd(self):
        import numpy as np

        x = solve_via_gauss(self.A_spd, self.b_spd)
        np.testing.assert_allclose(np.matmul(self.A_spd, x), self.b_spd, atol=1e-5)

    def test_14_gauss_zero_b(self):
        import numpy as np

        x = solve_via_gauss(self.A_square, self.b_zero)
        np.testing.assert_allclose(np.matmul(self.A_square, x), self.b_zero, atol=1e-5)

    def test_15_gauss_singular(self):
        with self.assertRaises(ValueError):
            solve_via_gauss(self.A_dependent, self.b_dependent)

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
    Giải hệ phương trình tuyến tính Ax = b bằng phương pháp lặp Gauss-Seidel.
    (Phiên bản thuần Python, không sử dụng thư viện ngoài)
    """
    A_list = to_matrix(A, require_square=True, error_message="Input matrix must be a non-empty square matrix.")
    b_list = to_vector(b)
    n = len(A_list)
    if len(b_list) != n:
        raise ValueError("kich thuoc b khong phu hop voi A")

    eps = 1e-12
    for i in range(n):
        if abs(A_list[i][i]) <= eps:
            raise ValueError("he co phan tu duong cheo bang 0, khong the ap dung Gauss-Seidel")

    if require_convergence_check and not _is_strictly_diagonally_dominant(A_list):
        msg = "Gauss-Seidel convergence is not guaranteed (matrix is not strictly diagonally dominant)."
        if strict_convergence:
            raise ValueError(msg)
        if verbose:
            print(f"[Gauss-Seidel] Canh bao: {msg}")

    # 1. Khởi tạo vector nghiệm ban đầu
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
                raise OverflowError("Gauss-Seidel diverged or overflowed")
            x[i] = new_xi

            diff = abs(new_xi - old_xi)
            if diff > max_diff:
                max_diff = diff

        if not math.isfinite(max_diff):
            raise OverflowError("Gauss-Seidel diverged or overflowed")
        
        if max_diff < tolerance:
            if verbose:
                print(f"[Gauss-Seidel] Đã hội tụ sau {k+1} vòng lặp.")
            return x

        if any(not math.isfinite(value) for value in x):
            raise OverflowError("Gauss-Seidel diverged or overflowed")
            
    if verbose:
        print("[Gauss-Seidel] Cảnh báo: Vượt quá số vòng lặp tối đa mà chưa hội tụ.")
    return x

if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
