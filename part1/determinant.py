try:
    from .gaussian import gaussian_eliminate
except ImportError:
    from gaussian import gaussian_eliminate

def determinant(A):
    """
    Tính định thức của ma trận vuông A thông qua phép khử Gauss.
    """
    n = len(A)
    # Tạo vector b toàn số 0 vì hàm gaussian_eliminate cần đầu vào
    dummy_b = [0.0] * n
    
    # Lấy ma trận U và số lần hoán đổi dòng
    U, _, swaps = gaussian_eliminate(A, dummy_b)
    
    # Định thức đổi dấu nếu số lần hoán đổi là số lẻ
    det = 1.0 if swaps % 2 == 0 else -1.0
    
    # Định thức ma trận tam giác trên bằng tích đường chéo chính
    for i in range(n):
        det *= U[i][i]
        
    return det