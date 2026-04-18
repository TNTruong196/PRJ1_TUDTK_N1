import re

def _print_inf(U, c, p_cols, n):
    """Ham ho tro de tinh va in ra nghiem khi co vo so nghiem"""
    free = [j for j in range(n) if j not in p_cols]
    sol = [{} for _ in range(n)]
    for f in free: 
        sol[f] = {f: 1.0, 'c': 0.0}
    
    for r in range(len(p_cols) - 1, -1, -1):
        pc = p_cols[r]
        ex = {'c': c[r]}
        for j in range(pc + 1, n):
            for k, v in sol[j].items(): 
                ex[k] = ex.get(k, 0.0) - U[r][j] * v
        for k in ex: 
            ex[k] /= U[r][pc]
        sol[pc] = ex

    for i, d in enumerate(sol):
        const = d.get('c', 0.0)
        res = f"{const:.4g}" if abs(const) > 1e-9 or len(d) == 1 else ""
        for f in free:
            val = d.get(f, 0.0)
            if abs(val) > 1e-9:
                sign = ("+" if val > 0 else "-") if res else ("" if val > 0 else "-")
                res += f" {sign} {abs(val):.4g}*t_{f+1}"
        print(f"x_{i+1} = {res.strip() or '0'}")

def back_substitution(U, c):
    """Giai he tam giac tren"""
    n = len(U)
    if any(len(row) != n for row in U):
        raise ValueError("Ma tran U phai la ma tran vuong")
    
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) < 1e-9:
            raise ValueError("Ma tran suy bien")
        s = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - s) / U[i][i]
    return x

def gaussian_eliminate(A, b, verbose=False):
    """
    Khu Gausss - Tra ve ma tran da khu, nghiem va co so cac
    khong gian cot, dong, nghiem.
    In ra dang tong quat neu co vo so nghiem.
    """
    M = [row[:] for row in A]
    c = b[:]
    m, n = len(M), len(M[0])
    swaps = 0
    p_row = 0
    p_cols = []
    eps = 1e-9

    for col in range(n):
        if p_row >= m: break
        # Tim pivot
        p = max(range(p_row, m), key=lambda r: abs(M[r][col]))
        if abs(M[p][col]) <= eps: continue

        M[p_row], M[p] = M[p], M[p_row]
        c[p_row], c[p] = c[p], c[p_row]
        if p != p_row: swaps += 1

        for r in range(p_row + 1, m):
            f = M[r][col] / M[p_row][col]
            for j in range(col, n):
                M[r][j] -= f * M[p_row][j]
            c[r] -= f * c[p_row]
        
        p_cols.append(col)
        p_row += 1

    # Kiem tra vo nghiem
    for r in range(m):
        if all(abs(M[r][j]) < eps for j in range(n)) and abs(c[r]) > eps:
            if verbose: print("He vo nghiem")
            return M, None, swaps

    # Kiem tra vo so nghiem
    if len(p_cols) < n:
        if verbose: 
            print("He co vo so nghiem")
            _print_inf(M, c, p_cols, n)
        return M, None, swaps

    # Nghiem duy nhat
    x = back_substitution([row[:n] for row in M[:n]], c[:n])
    return M, x, swaps