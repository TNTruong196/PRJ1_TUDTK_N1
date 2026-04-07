import copy


def _back_substitution_square(U, c, eps=1e-9):
    n = len(U)
    x = [0.0] * n

    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) <= eps:
            raise ValueError("he khong co nghiem duy nhat")

        s = 0.0
        for j in range(i + 1, n):
            s += U[i][j] * x[j]
        x[i] = (c[i] - s) / U[i][i]

    return x


def gaussian_eliminate(A, b):
    """Khử Gauss partial pivot cho ma trận m x n.

    Tra ve (M, x, swaps):
    - M: ma tran sau khử.
    - x: nghiem duy nhat neu ton tai.
    - swaps: so lan hoan vi dong.
    """
    if not A or not isinstance(A, list) or not isinstance(b, list):
        raise ValueError("du lieu dau vao khong hop le")

    m = len(A)
    if not isinstance(A[0], list) or len(A[0]) == 0:
        raise ValueError("ma tran A phai co it nhat 1 cot")

    n = len(A[0])
    if any(len(row) != n for row in A):
        raise ValueError("ma tran A phai la ma tran chu nhat")
    if len(b) != m:
        raise ValueError("kich thuoc b khong phu hop voi so dong cua A")

    M = copy.deepcopy([[float(v) for v in row] for row in A])
    c = copy.deepcopy([float(v) for v in b])
    eps = 1e-9
    swaps = 0

    pivot_row = 0
    pivot_cols = []

    for col in range(n):
        if pivot_row >= m:
            break

        p = pivot_row
        max_val = abs(M[pivot_row][col])
        for r in range(pivot_row + 1, m):
            v = abs(M[r][col])
            if v > max_val:
                max_val = v
                p = r

        if max_val <= eps:
            print(f"khong co pivot tai cot {col}")
            continue

        if p != pivot_row:
            M[pivot_row], M[p] = M[p], M[pivot_row]
            c[pivot_row], c[p] = c[p], c[pivot_row]
            swaps += 1

        for r in range(pivot_row + 1, m):
            factor = M[r][col] / M[pivot_row][col]
            if abs(factor) <= eps:
                continue
            for j in range(col, n):
                M[r][j] -= factor * M[pivot_row][j]
            c[r] -= factor * c[pivot_row]

        pivot_cols.append(col)
        pivot_row += 1

    for r in range(m):
        if all(abs(M[r][j]) <= eps for j in range(n)) and abs(c[r]) > eps:
            raise ValueError("he vo nghiem")

    if len(pivot_cols) < n or m < n:
        raise ValueError("he khong co nghiem duy nhat")

    U = [M[i][:n] for i in range(n)]
    c_top = c[:n]
    x = _back_substitution_square(U, c_top, eps=eps)
    return M, x, swaps