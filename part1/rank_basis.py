def _to_matrix(mat):
    rows = [list(row) for row in mat]
    if not rows:
        raise ValueError("Input matrix must be non-empty.")
    n = len(rows[0])
    if n == 0 or any(len(row) != n for row in rows):
        raise ValueError("Input matrix must be rectangular.")
    return [[float(x) for x in row] for row in rows]


def rank_and_basis(mat):
    """Tra ve (rank, column_space_basis, row_space_basis, null_space_basis)."""
    a = _to_matrix(mat)
    m = len(a)
    n = len(a[0])
    rref = [row[:] for row in a]

    eps = 1e-12
    pivot_row = 0
    pivot_cols = []

    for col in range(n):
        if pivot_row >= m:
            break

        max_id = pivot_row
        max_val = abs(rref[pivot_row][col])
        for r in range(pivot_row + 1, m):
            v = abs(rref[r][col])
            if v > max_val:
                max_val = v
                max_id = r

        if max_val <= eps:
            continue

        if max_id != pivot_row:
            rref[pivot_row], rref[max_id] = rref[max_id], rref[pivot_row]

        pivot = rref[pivot_row][col]
        for c in range(n):
            rref[pivot_row][c] /= pivot

        for r in range(m):
            if r == pivot_row:
                continue
            factor = rref[r][col]
            if abs(factor) <= eps:
                continue
            for c in range(n):
                rref[r][c] -= factor * rref[pivot_row][c]

        pivot_cols.append(col)
        pivot_row += 1

    rank = len(pivot_cols)
    col_space = [[a[r][j] for r in range(m)] for j in pivot_cols]
    row_space = [rref[i][:] for i in range(rank)]

    free_vars = [j for j in range(n) if j not in pivot_cols]
    null_space = []
    for f in free_vars:
        vec = [0.0] * n
        vec[f] = 1.0
        for i, p_col in enumerate(pivot_cols):
            vec[p_col] = -rref[i][f]
        null_space.append(vec)

    return rank, col_space, row_space, null_space