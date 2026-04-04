import numpy as np

def rank_and_basis(mat: np.array):
    """
    Trả về tuple chứa hạng, cơ sở của không gian cột, không gian 
    dòng, không gian nghiệm
    """
    m, n = mat.shape
    rref = mat.astype(float).copy()
    pivot_row = 0
    # Lưu trữ vị trí của các cột chứa pivot
    pivot_cols = []

    # Đưa về dạng bậc thang rút gọn
    for j in range(n):
        if pivot_row >= m: break
        
        # Tìm số lớn nhất trong cột làm pivot để đảm bảo pivot 
        # khác 0, và giảm sai số khi tính toán với số thực
        max_id = np.argmax(np.abs(rref[pivot_row:, j])) + pivot_row
        if np.isclose(rref[max_id, j], 0):
            continue # Cột này không có pivot, bỏ qua
            
        # Hoán vị dòng
        rref[[pivot_row, max_id]] = rref[[max_id, pivot_row]]
        pivot_cols.append(j)
        
        # Đưa pivot về 1
        rref[pivot_row] /= rref[pivot_row, j]
        
        # Triệt tiêu các dòng khác
        for i in range(m):
            if i != pivot_row:
                rref[i] -= rref[i, j] * rref[pivot_row]
        
        pivot_row += 1

    # Hạng
    rank = len(pivot_cols)

    # Không gian cột (column space) - lấy từ ma trận gốc
    col_space = [mat[:, j] for j in pivot_cols]

    # Không gian dòng (row space) - các dòng khác 0 trong RREF
    row_space = [rref[i] for i in range(rank)]

    # Không gian nghiệm (null space) - giải Ax = 0
    null_space = []
    free_vars = [j for j in range(n) if j not in pivot_cols]
    for f in free_vars:
        vec = np.zeros(n)
        vec[f] = 1 # Biến tự do f = 1
        for i, p_col in enumerate(pivot_cols):
            # Tính các biến còn lại dựa trên biến tự do
            vec[p_col] = -rref[i, f]
        null_space.append(vec)

    return rank, col_space, row_space, null_space