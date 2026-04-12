import numpy as np

def solve_gauss_seidel(A, b, tolerance=1e-10, max_iterations=1000):
    """
    Giải hệ phương trình tuyến tính Ax = b bằng phương pháp lặp Gauss-Seidel.
    """
    n = len(A)
    # Khởi tạo vector nghiệm x ban đầu là vector 0
    x = np.zeros_like(b, dtype=np.double)
    
    for k in range(max_iterations):
        x_old = x.copy()
        
        for i in range(n):
            # Tính tổng các phần tử đã được cập nhật trong bước lặp hiện tại (k+1)
            sum_new = sum(A[i][j] * x[j] for j in range(i))
            # Tính tổng các phần tử chưa được cập nhật (đang ở bước k)
            sum_old = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            
            # Cập nhật x[i]
            x[i] = (b[i] - sum_new - sum_old) / A[i][i]
            
        # Kiểm tra điều kiện hội tụ (sai số tuyệt đối lớn nhất)
        if np.linalg.norm(x - x_old, ord=np.inf) < tolerance:
            print(f"[Gauss-Seidel] Đã hội tụ sau {k+1} vòng lặp.")
            return x
            
    print("[Gauss-Seidel] Cảnh báo: Vượt quá số vòng lặp tối đa mà chưa hội tụ.")
    return x