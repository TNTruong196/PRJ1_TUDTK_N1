import numpy as np

def inverse(mat: np.array):
    """
    Trả về ma trận nghịch đảo, nếu không khả nghịch 
    thì trả về None
    """
    if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
        return None

    n = mat.shape[0]
    a = mat.astype(float).copy()
    inversed = np.eye(n)
    
    for i in range(n):
        # Tìm số lớn nhất trong cột làm pivot để đảm bảo pivot 
        # khác 0, và giảm sai số khi tính toán với số thực
        max_id = np.argmax(np.abs(a[i:, i])) + i
        if np.isclose(a[max_id, i], 0):
            return None

        # Hoán vị dòng
        a[[i, max_id]] = a[[max_id, i]]
        inversed[[i, max_id]] = inversed[[max_id, i]]

        # Chuẩn hóa để pivot về 1
        pivot = a[i, i]
        a[i] /= pivot
        inversed[i] /= pivot
        
        # Triệt tiêu các dòng khác
        for j in range(n):
            if j != i:
                factor = a[j, i]
                a[j] -= factor * a[i]
                inversed[j] -= factor * inversed[i]

    return inversed