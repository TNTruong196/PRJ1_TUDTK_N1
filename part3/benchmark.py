import random

def generate_hilbert(n):
    """
    Tạo ma trận có số điều kiện lớn H bằng cách cho phân tử
    H_ij bằng 1/(i + j + 1)
    """
    return [[1 / (i + j + 1) for j in range(n)] for i in range(n)]

def generate_spd(n):
    """
    Tạo ma trận có số điều kiện nhỏ A bằng công thức
    A = M^T * M + nI
    """
    # Tạo ma trận ngẫu nhiên M kích thước n x n
    M = [[random.uniform(0, 1) for _ in range(n)] for _ in range(n)]
    
    # Tính A = M^T * M (đảm bảo đối xứng và xác định không âm)
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                A[i][j] += M[k][i] * M[k][j]
    
    # Cộng thêm n*I vào đường chéo chính để đảm bảo xác định dương 
    # và cải thiện tính ổn định (well-conditioned) 
    for i in range(n):
        A[i][i] += n
        
    return A