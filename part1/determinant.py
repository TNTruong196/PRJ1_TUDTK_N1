try:
    from .gaussian import gaussian_eliminate
except ImportError:
    from gaussian import gaussian_eliminate

def determinant(A):
    """
    Tính định thức của ma trận vuông A thông qua phép khử Gauss.
    """
    try:
        m = len(A)
        n = len(A[0])
        if m != n:
            raise ValueError("Khong the tinh dinh thuc cho ma tran khong vuong")
    except (TypeError, IndexError):
        raise ValueError("Du lieu dau vao khong phai ma tran hop le")
    dummy_b = [0.0] * n
    
    U, _, swaps = gaussian_eliminate(A, dummy_b, verbose=False)
    
    # Kiểm tra nếu sau khi khử có dòng toàn số 0 trên đường chéo -> det = 0
    eps = 1e-9
    for i in range(n):
        if abs(U[i][i]) <= eps:
            return 0.0
            
    # Định thức đổi dấu nếu số lần hoán đổi là số lẻ
    det = 1.0 if swaps % 2 == 0 else -1.0
    
    # Định thức ma trận tam giác trên bằng tích đường chéo chính
    for i in range(n):
        det *= U[i][i]
        
    return det