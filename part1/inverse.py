import copy

EPSILON = 1e-9

def inverse(A):
    """
    Tra ve ma tran nghich dao, neu khong kha nghich
    thi tra ve None
    """
    try:
        n = len(A)
        if n == 0 or any(len(row) != n for row in A):
            return None
    except (TypeError, IndexError):
        return None

    a = copy.deepcopy(A)
    inv = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    for i in range(n):
        # Tim so lon nhat trong cot lam pivot de dam bao pivot
        # khac 0, va giam sai so khi tinh toan voi so thuc (Partial Pivoting)
        max_val = abs(a[i][i])
        max_id = i
        for r in range(i + 1, n):
            if abs(a[r][i]) > max_val:
                max_val = abs(a[r][i])
                max_id = r
        # Kiem tra ma tran suy bien
        if abs(a[max_id][i]) < EPSILON:
            return None

        # Hoan vi dong
        a[i], a[max_id] = a[max_id], a[i]
        inv[i], inv[max_id] = inv[max_id], inv[i]

        # Chuan hoa dong de pivot ve 1
        pivot = a[i][i]
        a[i] = [x / pivot for x in a[i]]
        inv[i] = [x / pivot for x in inv[i]]
        
        # Dua a ve ma tran don vi
        for r in range(n):
            if r != i:
                factor = a[r][i]
                # dj = dj - factor * di
                a[r] = [x - factor * y for x, y in zip(a[r], a[i])]
                inv[r] = [x - factor * y for x, y in zip(inv[r], inv[i])]

    return inv
