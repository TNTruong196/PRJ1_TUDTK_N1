import copy

def _back_substitution_general(U, c, pivot_cols, n, eps=1e-9):
    # Biến tự do là những cột không chứa phần tử pivot
    free_vars = [j for j in range(n) if j not in pivot_cols]

    # Khởi tạo nghiệm dưới dạng dictionary
    # Mỗi biến x_i là một dict, ví dụ x_i = 5 - 2*t_j -> {'const': 5.0, j: -2.0}
    x_dict = [{} for _ in range(n)]
    for f in free_vars:
        x_dict[f] = {f: 1.0, 'const': 0.0} # x_f = 1 * t_f

    m_eq = len(pivot_cols)
    # Thế ngược từ dưới lên cho các biến cơ sở (pivot variables)
    for r in range(m_eq - 1, -1, -1):
        p_col = pivot_cols[r]
        expr = {'const': c[r]}

        for j in range(p_col + 1, n):
            coef = U[r][j]
            if abs(coef) > eps:
                # Trừ đi coef * x[j]
                for key, val in x_dict[j].items():
                    expr[key] = expr.get(key, 0.0) - coef * val

        # Chia tất cả cho phần tử pivot
        pivot_val = U[r][p_col]
        for key in expr:
            expr[key] /= pivot_val

        x_dict[p_col] = expr

    # Chuyển đổi dict thành chuỗi để in ra công thức
    x_str = []
    for i in range(n):
        if i in free_vars:
            x_str.append(f"t_{i+1} (biến tự do)")
        else:
            terms = []
            const = x_dict[i].get('const', 0.0)
            if abs(const) > eps or len(x_dict[i]) == 1:
                terms.append(f"{const:.4g}")
            
            for f in free_vars:
                coef = x_dict[i].get(f, 0.0)
                if abs(coef) > eps:
                    val = abs(coef)
                    # SỬA LỖI 4 TẠI ĐÂY: Nếu mảng terms rỗng (đứng đầu) và hệ số dương thì bỏ dấu +
                    if not terms and coef > 0:
                        terms.append(f"{val:.4g}*t_{f+1}")
                    else:
                        sign = "+" if coef > 0 else "-"
                        terms.append(f"{sign} {val:.4g}*t_{f+1}")
                    
            if not terms:
                terms.append("0")
            x_str.append(" ".join(terms))
    return x_str

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


def gaussian_eliminate(A, b, verbose=True):
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
            if verbose: # Kẹp điều kiện verbose vào đây
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
            if verbose:
                print("hệ không có nghiệm")
            return M, None, swaps

    # In ra hệ không có nghiệm duy nhất nếu có biến tự do
    if len(pivot_cols) < n:
        if verbose:
            print("hệ không có nghiệm duy nhất")

    U = [M[i][:n] for i in range(m)]

    # Nếu hệ vuông và đủ rank -> nghiệm duy nhất
    if len(pivot_cols) == n:
        x = _back_substitution_square(U[:n], c[:n], eps=eps)
    else:
        # Nếu vô số nghiệm -> trả về công thức tổng quát
        x = _back_substitution_general(U, c, pivot_cols, n, eps=eps)

    return M, x, swaps