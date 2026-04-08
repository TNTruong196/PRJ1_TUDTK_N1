import copy

EPSILON = 1e-9

def inverse(A):
    """
    Trả về ma trận nghịch đảo, nếu không khả nghịch 
    thì trả về None
    """
    try:
        n = len(A)
        if n == 0 or n != len(A[0]):
            return None
    except (TypeError, IndexError):
        return None

    a = copy.deepcopy(A)
    inv = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    for i in range(n):
        # Tìm số lớn nhất trong cột làm pivot để đảm bảo pivot 
        # khác 0, và giảm sai số khi tính toán với số thực (Partial Pivoting)
        max_val = abs(a[i][i])
        max_id = i
        for j in range(i + 1, n):
            if abs(a[j][i]) > max_val:
                max_val = abs(a[j][i])
                max_id = j
        # Kiểm tra ma trận suy biến
        if abs(a[max_id][i]) < EPSILON:
            return None

        # Hoán vị dòng
        a[i], a[max_id] = a[max_id], a[i]
        inv[i], inv[max_id] = inv[max_id], inv[i]

        # Chuẩn hóa dòng để pivot về 1
        pivot = a[i][i]
        a[i] = [x / pivot for x in a[i]]
        inv[i] = [x / pivot for x in inv[i]]
        
        # Đưa a về ma trận đơn vị
        for j in range(n):
            if j != i:
                factor = a[j][i]
                # dj = dj - factor * di
                a[j] = [x - factor * y for x, y in zip(a[j], a[i])]
                inv[j] = [x - factor * y for x, y in zip(inv[j], inv[i])]

    return inv