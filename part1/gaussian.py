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
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    M = copy.deepcopy(A)
    c = copy.deepcopy(b)
    swaps = 0

    if m == 0 or n == 0:
        print("Cảnh báo: Ma trận rỗng, không thể thực hiện khử Gauss.")
        return M, None, swaps

    if len(c) != m:
        print("Cảnh báo: Kích thước vector b không khớp số dòng của ma trận A.")
        return M, None, swaps

    for row in M:
        if len(row) != n:
            print("Cảnh báo: Ma trận A không hợp lệ (số cột không đồng nhất).")
            return M, None, swaps
    
    for k in range(min(m, n)):
        # Chọn phần tử chốt
        p = k
        max_val = abs(M[k][k])
        for i in range(k + 1, m):
            if abs(M[i][k]) > max_val:
                max_val = abs(M[i][k])
                p = i
                
        if max_val < 1e-9:
            print(f"Cảnh báo: Pivot tại cột {k} gần bằng 0, bỏ qua bước khử tại cột này.")
            continue
            
        # Hoán đổi dòng
        if p != k:
            M[k], M[p] = M[p], M[k]
            c[k], c[p] = c[p], c[k]
            swaps += 1
            
        # Khử Gauss
        for i in range(k + 1, m):
            l_ik = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= l_ik * M[k][j]
            c[i] -= l_ik * c[k]

    if m != n:
        print("Cảnh báo: Ma trận không vuông nên không thể back substitution để tìm nghiệm duy nhất.")
        return M, None, swaps
            
    try:
        x = back_substitution(M, c)
    except ValueError as e:
        print(e)
        x = None
        
    return M, x, swaps