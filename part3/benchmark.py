import os
import sys
import time
import random
import math  # Thư viện chuẩn của Python, được phép dùng để tính căn bậc 2

# Thiết lập đường dẫn để import được từ các thư mục khác
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from solvers import (
    solve_via_gauss,
    solve_via_cholesky,
    solve_via_normal_equations,
    solve_gauss_seidel
)

# =====================================================================
# 1. CÁC HÀM TOÁN HỌC THUẦN PYTHON (Thay thế Numpy)
# =====================================================================
def mat_vec_mult(A, x):
    """Nhân ma trận A với vector x"""
    n = len(A)
    return [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]

def vec_sub(u, v):
    """Trừ hai vector u - v"""
    return [u_i - v_i for u_i, v_i in zip(u, v)]

def norm_2(v):
    """Tính chuẩn 2 (Euclidean norm) của vector"""
    return math.sqrt(sum(v_i**2 for v_i in v))

def calc_relative_error(A, x_hat, b):
    """Tính sai số tương đối: ||Ax_hat - b||_2 / ||b||_2"""
    if x_hat is None:
        return float('inf')
    Ax = mat_vec_mult(A, x_hat)
    residual = vec_sub(Ax, b)
    b_norm = norm_2(b)
    if b_norm == 0.0:
        # Neu b = 0, dung residual norm de danh gia do chinh xac tuyet doi
        return norm_2(residual)
    return norm_2(residual) / b_norm

# =====================================================================
# 2. HAI HÀM SINH MA TRẬN DỮ LIỆU (THUẦN PYTHON)
# =====================================================================
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
# 3. HÀM CHẠY BENCHMARK
# =====================================================================
def run_benchmark():
    # Yêu cầu của đề bài: n in {50, 100, 200, 500, 1000}
    # CẢNH BÁO: Vì code thuần Python, n=1000 sẽ chạy khá lâu.
    n_list = [50, 100, 200, 500, 1000]
    num_runs = 5
    
    methods = [
        ("Khử Gauss", solve_via_gauss),
        ("Phân rã Cholesky", solve_via_cholesky),
        ("Hệ PT Chuẩn (Normal Eq)", solve_via_normal_equations),
        ("Lặp Gauss-Seidel", solve_gauss_seidel)
    ]

    print("========== BẮT ĐẦU BENCHMARK ==========\n")
    print("Sai số tương đối sử dụng công thức: ||A x_hat - b||_2 / ||b||_2")

    for n in n_list:
        print(f"\n[{'='*10} ĐANG XỬ LÝ KÍCH THƯỚC N = {n} {'='*10}]")
        
        # --- KỊCH BẢN 1: SPD ---
        print(">>> Ma trận SPD (Well-conditioned)")
        for name, func in methods:
            total_time = 0.0
            total_error = 0.0
            success_runs = 0
            failed_runs = 0
            last_error = ""
            
            for _ in range(num_runs):
                A = generate_spd_pure_python(n)
                b = [random.uniform(0, 1) for _ in range(n)]
                
                # Copy để tránh thay đổi ma trận gốc
                A_copy = [row[:] for row in A]
                b_copy = b[:]
                
                start = time.time()
                try:
                    x_hat = func(A_copy, b_copy)
                    total_time += (time.time() - start)
                    total_error += calc_relative_error(A, x_hat, b)
                    success_runs += 1
                except Exception as exc:
                    failed_runs += 1
                    last_error = str(exc)
            
            if success_runs > 0:
                avg_time = total_time / success_runs
                avg_err = total_error / success_runs
                print(
                    f" - {name:25}: {avg_time:8.4f}s | Sai số: {avg_err:.2e} "
                    f"| Thanh cong: {success_runs}/{num_runs}"
                )
                if failed_runs > 0:
                    print(f"   Canh bao: {failed_runs} lan loi. Vi du loi: {last_error}")
            else:
                print(f" - {name:25}: THAT BAI (0/{num_runs}). Vi du loi: {last_error}")

        # --- KỊCH BẢN 2: HILBERT ---
        print("\n>>> Ma trận Hilbert (Ill-conditioned)")
        for name, func in methods:
            total_time = 0.0
            total_error = 0.0
            success_runs = 0
            failed_runs = 0
            last_error = ""
            
            for _ in range(num_runs):
                A = generate_hilbert_pure_python(n)
                b = [random.uniform(0, 1) for _ in range(n)]
                
                A_copy = [row[:] for row in A]
                b_copy = b[:]
                
                start = time.time()
                try:
                    x_hat = func(A_copy, b_copy)
                    total_time += (time.time() - start)
                    total_error += calc_relative_error(A, x_hat, b)
                    success_runs += 1
                except Exception as exc:
                    failed_runs += 1
                    last_error = str(exc)
            
            if success_runs > 0:
                avg_time = total_time / success_runs
                avg_err = total_error / success_runs
                print(
                    f" - {name:25}: {avg_time:8.4f}s | Sai số: {avg_err:.2e} "
                    f"| Thanh cong: {success_runs}/{num_runs}"
                )
                if failed_runs > 0:
                    print(f"   Canh bao: {failed_runs} lan loi. Vi du loi: {last_error}")
            else:
                print(f" - {name:25}: THAT BAI (0/{num_runs}). Vi du loi: {last_error}")

if __name__ == "__main__":
    run_benchmark()