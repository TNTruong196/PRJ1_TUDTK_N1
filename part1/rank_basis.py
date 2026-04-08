import numpy as np
from gaussian import gaussian_eliminate

# LƯU Ý:
# Hàm này mặc định gaussian_eliminate(A, b) trả về x đúng cho cả 3 trường hợp
# (vô nghiệm, nghiệm duy nhất, vô số nghiệm)
# Nếu vô nghiệm: trả về x = None
# Nếu nghiệm duy nhất: trả về x là vector
# Nếu vô số nghiệm: trả về x là dictionary { 'particular', 'basis' }
# với basis là matrix chứa các vector cơ sở

EPSILON = 1e-9

def rank_and_basis(A: np.array):
    a = A.astype(float).copy()
    # Tạo vector b toàn số 0
    m, n = A.shape
    b = np.zeros(m)

    # Dùng hàm khử Gauss có sẵn để tìm ma trận tam giác trên
    ref, x, _ = gaussian_eliminate(a, b)

    # Xác định các cột chứa pivot
    pivot_cols = []
    curr_row = 0
    for j in range(n):
        if curr_row < m:
            # Nếu đây là cột chứa pivot thì thêm vào pivot_cols
            if abs(ref[curr_row][j]) > EPSILON:
                pivot_cols.append(j)
                curr_row += 1

    rank = len(pivot_cols)
    
    # Cơ sở không gian cột
    col_space = [A[:, j] for j in pivot_cols]

    # Cơ sở không gian dòng
    row_space = [ref[i] for i in range(rank)]

    # Cơ sở không gian nghiệm (hệ Ax=0 luôn có nghiệm)
    null_space = []
    if isinstance(x, np.ndarray):
        # Có 1 nghiệm, cơ sở rỗng
        pass
    elif isinstance(x, dict):
        # Vô số nghiệm
        null_space = x['basis']

    return rank, col_space, row_space, null_space


arr = np.array([[1, 2, 3], [4, 5, 6]])
um = rank_and_basis(arr)