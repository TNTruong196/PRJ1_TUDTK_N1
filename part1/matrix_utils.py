def to_matrix(mat, *, require_square: bool = False, error_message: str = "Invalid matrix."):
    try:
        rows = [list(row) for row in mat]
    except TypeError as exc:
        raise ValueError(error_message) from exc

    if not rows:
        raise ValueError(error_message)

    n_cols = len(rows[0])
    if n_cols == 0 or any(len(row) != n_cols for row in rows):
        raise ValueError(error_message)

    if require_square and len(rows) != n_cols:
        raise ValueError(error_message)

    try:
        return [[float(x) for x in row] for row in rows]
    except (TypeError, ValueError) as exc:
        raise ValueError(error_message) from exc


def to_vector(vec):
    values = list(vec)
    if values and isinstance(values[0], (list, tuple)):
        flat = []
        for row in values:
            flat.extend(row)
        values = flat
    try:
        return [float(value) for value in values]
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid vector.") from exc


def transpose(A):
    return [list(row) for row in zip(*A)]


def matmul(A, B):
    rows = len(A)
    shared = len(B)
    cols = len(B[0])
    result = [[0.0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(shared):
            aval = A[i][k]
            if aval == 0.0:
                continue
            for j in range(cols):
                result[i][j] += aval * B[k][j]
    return result


def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def infinity_norm(A):
    return max(sum(abs(x) for x in row) for row in A)