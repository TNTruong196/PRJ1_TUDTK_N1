def _to_matrix(mat):
    try:
        rows = [list(row) for row in mat]
    except TypeError:
        return None

    if not rows:
        return None

    n_cols = len(rows[0])
    if n_cols == 0 or any(len(row) != n_cols for row in rows):
        return None

    try:
        return [[float(x) for x in row] for row in rows]
    except (TypeError, ValueError):
        return None


def inverse(mat):
    """Tra ve ma tran nghich dao, neu khong kha nghich thi tra ve None."""
    a = _to_matrix(mat)
    if a is None:
        return None

    n = len(a)
    if n != len(a[0]):
        return None

    eps = 1e-12
    inv = [[0.0] * n for _ in range(n)]
    for i in range(n):
        inv[i][i] = 1.0

    for i in range(n):
        max_id = i
        max_val = abs(a[i][i])
        for r in range(i + 1, n):
            v = abs(a[r][i])
            if v > max_val:
                max_val = v
                max_id = r

        if max_val <= eps:
            return None

        if max_id != i:
            a[i], a[max_id] = a[max_id], a[i]
            inv[i], inv[max_id] = inv[max_id], inv[i]

        pivot = a[i][i]
        for c in range(n):
            a[i][c] /= pivot
            inv[i][c] /= pivot

        for r in range(n):
            if r == i:
                continue
            factor = a[r][i]
            if abs(factor) <= eps:
                continue
            for c in range(n):
                a[r][c] -= factor * a[i][c]
                inv[r][c] -= factor * inv[i][c]

    return inv