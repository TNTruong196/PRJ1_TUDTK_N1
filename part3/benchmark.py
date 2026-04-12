import numpy as np
import random
import time

# --- 1. IMPORT THUẬT TOÁN GAUSS-SEIDEL ---
from gauss_seidel import solve_gauss_seidel 

# --- 2. CÁC HÀM TẠO MA TRẬN (DỮ LIỆU TEST) ---
def generate_hilbert(n):
    """Tạo ma trận Hilbert (Số điều kiện lớn - Rất khó giải)"""
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

def generate_spd(n):
    """Tạo ma trận Đối xứng Xác định dương (Số điều kiện nhỏ - Dễ giải)"""
    M = np.array([[random.uniform(0, 1) for _ in range(n)] for _ in range(n)])
    A = np.dot(M.T, M) # M^T * M
    # Cộng thêm n*I vào đường chéo chính
    np.fill_diagonal(A, A.diagonal() + n)
    return A

# --- 3. HÀM CHẠY BENCHMARK HOÀN CHỈNH ---
def run_benchmark():
    n = 100 # Kích thước ma trận (có thể đổi)
    
    print(f"========== BẮT ĐẦU BENCHMARK HỆ PHƯƠNG TRÌNH {n}x{n} ==========\n")

    # Kịch bản 1: Test với ma trận "Đẹp" (SPD)
    print(">>> KỊCH BẢN 1: Ma trận Đối xứng Xác định dương (SPD)")
    A_spd = generate_spd(n)
    b_spd = np.random.rand(n) # Tạo vector b ngẫu nhiên

    # Cách 1: Gauss-Seidel tự code
    start = time.time()
    x_gs_spd = solve_gauss_seidel(A_spd, b_spd)
    time_gs_spd = time.time() - start
    print(f" - Thời gian Gauss-Seidel: {time_gs_spd:.6f} s")

    # Cách 2: Numpy Solve (Thư viện chuẩn)
    start = time.time()
    x_np_spd = np.linalg.solve(A_spd, b_spd)
    time_np_spd = time.time() - start
    print(f" - Thời gian Numpy Solve : {time_np_spd:.6f} s")
    
    error_spd = np.linalg.norm(x_gs_spd - x_np_spd, ord=np.inf)
    print(f" -> Sai số giữa 2 cách   : {error_spd:.2e}\n")

    # -----------------------------------------------------------
    # Kịch bản 2: Test với ma trận "Ác mộng" (Hilbert)
    print(">>> KỊCH BẢN 2: Ma trận Hilbert (Ill-conditioned)")
    A_hilbert = generate_hilbert(n)
    b_hilbert = np.random.rand(n)

    # Cách 1: Gauss-Seidel tự code
    start = time.time()
    x_gs_hilb = solve_gauss_seidel(A_hilbert, b_hilbert, max_iterations=2000)
    time_gs_hilb = time.time() - start
    print(f" - Thời gian Gauss-Seidel: {time_gs_hilb:.6f} s")

    # Cách 2: Numpy Solve (Thư viện chuẩn)
    start = time.time()
    x_np_hilb = np.linalg.solve(A_hilbert, b_hilbert)
    time_np_hilb = time.time() - start
    print(f" - Thời gian Numpy Solve : {time_np_hilb:.6f} s")

    error_hilb = np.linalg.norm(x_gs_hilb - x_np_hilb, ord=np.inf)
    print(f" -> Sai số giữa 2 cách   : {error_hilb:.2e}\n")

if __name__ == "__main__":
    run_benchmark()