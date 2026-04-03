import copy

def back_substitution(U, c):
    """
    Giải hệ phương trình tam giác trên Ux = c.
    """
    n = len(U)
    x = [0.0] * n
    
    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) < 1e-9:
            raise ValueError(f"Lỗi: Hệ không có nghiệm duy nhất (pivot tại dòng {i} bằng 0).")
            
        sum_ax = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - sum_ax) / U[i][i]
        
    return x

def gaussian_eliminate(A, b):
    """
    Thực hiện khử Gauss có chọn phần tử chốt (Partial Pivoting).
    """
    n = len(A)
    M = copy.deepcopy(A)
    c = copy.deepcopy(b)
    swaps = 0
    
    for k in range(n):
        # Chọn phần tử chốt
        p = k
        max_val = abs(M[k][k])
        for i in range(k + 1, n):
            if abs(M[i][k]) > max_val:
                max_val = abs(M[i][k])
                p = i
                
        if max_val < 1e-9:
            print(f"Cảnh báo: Pivot tại cột {k} gần bằng 0, hệ có thể bị ill-conditioned.")
            
        # Hoán đổi dòng
        if p != k:
            M[k], M[p] = M[p], M[k]
            c[k], c[p] = c[p], c[k]
            swaps += 1
            
        # Khử Gauss
        for i in range(k + 1, n):
            if abs(M[k][k]) < 1e-9:
                continue 
            
            l_ik = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= l_ik * M[k][j]
            c[i] -= l_ik * c[k]
            
    try:
        x = back_substitution(M, c)
    except ValueError as e:
        print(e)
        x = None
        
    return M, x, swaps