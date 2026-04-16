import os
import sys
import time
import random
import math

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from solvers import (
    solve_via_gauss,
    solve_via_cholesky,
    solve_via_normal_equations,
    solve_gauss_seidel,
)


# =====================================================================
# 1. Pure Python helpers
# =====================================================================
def mat_vec_mult(A, x):
    n = len(A)
    return [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]


def vec_sub(u, v):
    return [u_i - v_i for u_i, v_i in zip(u, v)]


def norm_2(v):
    return math.sqrt(sum(v_i * v_i for v_i in v))


def calc_relative_error(A, x_hat, b):
    if x_hat is None:
        return float("inf")
    Ax = mat_vec_mult(A, x_hat)
    residual = vec_sub(Ax, b)
    b_norm = norm_2(b)
    if b_norm == 0.0:
        return norm_2(residual)
    return norm_2(residual) / b_norm


# =====================================================================
# 2. Random matrix generators
# =====================================================================
import random

def generate_diagonally_dominant_matrix(n, low=-10.0, high=10.0):
    """
    Tạo ma trận chéo trội chặt (Strictly Diagonally Dominant) 
    đảm bảo phương pháp Gauss-Seidel luôn hội tụ.
    Độ phức tạp: O(n^2) - Chạy rất nhanh kể cả với n=1000.
    """
    A = [[random.uniform(low, high) for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        # 1. Tính tổng trị tuyệt đối của các phần tử ngoài đường chéo trên hàng i
        off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        
        # 2. Ép phần tử đường chéo phải lớn hơn tổng này
        # Cộng thêm một giá trị dương ngẫu nhiên (vd: 1.0 đến 5.0) làm khoảng đệm an toàn
        A[i][i] = off_diag_sum + random.uniform(1.0, 5.0)
        
        # 3. (Tùy chọn) Lật dấu ngẫu nhiên để test cases đa dạng hơn (có số âm/dương)
        if random.choice([True, False]):
            A[i][i] = -A[i][i]
            
    return A


def generate_random_vector(n, low=-10.0, high=10.0):
    return [random.uniform(low, high) for _ in range(n)]


def generate_spd_pure_python(n):
    """Tạo ma trận SPD"""
    M = [[random.uniform(0, 1) for _ in range(n)] for _ in range(n)]
    A = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                A[i][j] += M[k][i] * M[k][j]
    for i in range(n):
        A[i][i] += n
    return A

def generate_hilbert_pure_python(n):
    """Tạo ma trận Hilbert"""
    return [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]

# =====================================================================
# 3. Benchmark runner (Đã cập nhật tên hàm gọi)
# =====================================================================
def _build_cases(n_list, num_runs):
    cases = {}
    for n in n_list:
        runs = []
        for _ in range(num_runs):
            # Gọi hàm sinh ma trận chéo trội thay vì ma trận ngẫu nhiên thuần
            A = generate_diagonally_dominant_matrix(n)
            b = generate_random_vector(n)
            runs.append((A, b))
        cases[n] = runs
    return cases


def run_benchmark(verbose=True):
    # Theo rubric Phan 3: n = {50, 100, 200, 500, 1000}, trung binh 5 lan chay.
    n_list = [50, 100, 200, 500, 1000]
    num_runs = 5
    random.seed(42)

    # Gauss-Seidel dung cau hinh im lang khi benchmark.
    gauss_seidel_for_benchmark = lambda A, b: solve_gauss_seidel(
        A,
        b,
        tolerance=1e-8,
        max_iterations=400,
        require_convergence_check=False,
        verbose=False,
    )

    methods = [
        ("Khử Gauss", solve_via_gauss),
        ("Phân rã Cholesky", solve_via_cholesky),
        ("Hệ PT Chuẩn (Cholesky)", solve_via_normal_equations),
        ("Lặp Gauss-Seidel", gauss_seidel_for_benchmark),
    ]

    cases = _build_cases(n_list, num_runs)
    results = {name: {} for name, _ in methods}

    if verbose:
        print("========== BENCHMARK RANDOM ==========")
        print("Ma tran su dung trong benchmark nay la ma tran ngau nhien thuong (khong rang buoc SPD).")
        print("Sai so tuong doi: ||A x_hat - b||_2 / ||b||_2")

    for n in n_list:
        if verbose:
            print(f"\n[{'=' * 10} n = {n} {'=' * 10}]")

        run_cases = cases[n]

        for name, func in methods:
            total_time = 0.0
            total_error = 0.0
            success_runs = 0
            failed_runs = 0
            last_error = ""

            for A, b in run_cases:
                A_copy = [row[:] for row in A]
                b_copy = b[:]

                start = time.perf_counter()
                try:
                    x_hat = func(A_copy, b_copy)
                    elapsed = time.perf_counter() - start
                    total_time += elapsed
                    total_error += calc_relative_error(A, x_hat, b)
                    success_runs += 1
                except Exception as exc:
                    failed_runs += 1
                    last_error = str(exc)

            avg_time = (total_time / success_runs) if success_runs > 0 else None
            avg_err = (total_error / success_runs) if success_runs > 0 else None
            results[name][n] = {
                "avg_time": avg_time,
                "avg_error": avg_err,
                "success_runs": success_runs,
                "failed_runs": failed_runs,
                "last_error": last_error,
            }

            if verbose:
                if success_runs > 0:
                    print(
                        f" - {name:25}: {avg_time:8.4f}s | Sai so: {avg_err:.2e} "
                        f"| Thanh cong: {success_runs}/{num_runs}"
                    )
                    if failed_runs > 0:
                        print(f"   Canh bao: {failed_runs} lan loi. Vi du loi: {last_error}")
                else:
                    print(f" - {name:25}: THAT BAI (0/{num_runs}). Vi du loi: {last_error}")

    return results


def run_benchmark_stability(verbose=True, n=10, num_runs=5):
    """
    Thực thi YÊU CẦU 3: Phân tích tính ổn định số (Numerical Stability).
    """
    A_hilbert = generate_hilbert_pure_python(n)
    A_spd = generate_spd_pure_python(n)
    
    x_true = [1.0] * n
    b_hilbert = mat_vec_mult(A_hilbert, x_true)
    b_spd = mat_vec_mult(A_spd, x_true)

    gauss_seidel_for_benchmark = lambda A, b: solve_gauss_seidel(
        A, b, tolerance=1e-8, max_iterations=400, require_convergence_check=False, verbose=False
    )

    methods = [
        ("Khử Gauss", solve_via_gauss),
        ("Phân rã Cholesky", solve_via_cholesky),
        ("Hệ PT Chuẩn (Cholesky)", solve_via_normal_equations),
        ("Lặp Gauss-Seidel", gauss_seidel_for_benchmark),
    ]

    results = {'SPD': {}, 'Hilbert': {}}

    if verbose:
        print("\n\n========== BENCHMARK TÍNH ỔN ĐỊNH SỐ ==========")
        print("Muc tieu: So sanh do chinh xac tren ma tran Tot (SPD) va ma tran Xau (Hilbert).")
        print(f"Kich thuoc thu nghiem: n = {n}. So lan chay: {num_runs}")
        print("Sai so tuong doi: ||A x_hat - b||_2 / ||b||_2")

    def _test_matrix(matrix_name, A, b):
        if verbose:
            print(f"\n[========== Ma tran: {matrix_name} ==========]")
        
        matrix_results = {}
        for name, func in methods:
            total_time = 0.0
            total_error = 0.0
            success_runs = 0
            failed_runs = 0
            last_error = ""

            for _ in range(num_runs):
                A_copy = [row[:] for row in A]
                b_copy = b[:]

                start = time.perf_counter()
                try:
                    x_hat = func(A_copy, b_copy)
                    elapsed = time.perf_counter() - start
                    total_time += elapsed
                    total_error += calc_relative_error(A, x_hat, b)
                    success_runs += 1
                except Exception as exc:
                    failed_runs += 1
                    last_error = str(exc)

            avg_time = (total_time / success_runs) if success_runs > 0 else None
            avg_err = (total_error / success_runs) if success_runs > 0 else None
            
            matrix_results[name] = {
                "avg_time": avg_time,
                "avg_error": avg_err,
                "success_runs": success_runs,
            }

            if verbose:
                if success_runs > 0:
                    print(
                        f" - {name:25}: {avg_time:8.4f}s | Sai so: {avg_err:.2e} "
                        f"| Thanh cong: {success_runs}/{num_runs}"
                    )
                else:
                    print(f" - {name:25}: THAT BAI (0/{num_runs}). Vi du loi: {last_error}")
                    
        return matrix_results

    results['SPD'] = _test_matrix("SPD (Well-conditioned)", A_spd, b_spd)
    results['Hilbert'] = _test_matrix("Hilbert (Ill-conditioned)", A_hilbert, b_hilbert)

    return results
    

if __name__ == "__main__":
    # run_benchmark(verbose=True)
    
    run_benchmark_stability(verbose=True, n=10, num_runs=5)
