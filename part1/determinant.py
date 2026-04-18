try:
    from .gaussian import gaussian_eliminate
except ImportError:
    from gaussian import gaussian_eliminate

def determinant(A):
    """
    Tinh dinh thuc cua ma tran vuong A thong qua phep khu Gauss.
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
    
    # Kiem tra neu sau khi khu co dong toan so 0 tren duong cheo -> det = 0
    eps = 1e-9
    for i in range(n):
        if abs(U[i][i]) <= eps:
            return 0.0
            
    # Dinh thuc doi dau neu so lan hoan doi la so le
    det = 1.0 if swaps % 2 == 0 else -1.0
    
    # Dinh thuc ma tran tam giac tren bang tich duong cheo chinh
    for i in range(n):
        det *= U[i][i]
        
    return det