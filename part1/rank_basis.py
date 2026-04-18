import copy
try:
    from .gaussian import gaussian_eliminate
except ImportError:
    from gaussian import gaussian_eliminate

EPSILON = 1e-9

def rank_and_basis(A):
    if not A or not A[0]:
        return 0, [], [], []

    a = copy.deepcopy(A)
    m = len(A)
    n = len(A[0])

    # Tao vector b toan so 0
    b = [0.0] * m

    # Dung ham khu Gauss co san de tim ma tran tam giac tren
    ref, x, _ = gaussian_eliminate(a, b,verbose=False)

    # Xac dinh cac cot chua pivot
    pivot_cols = []
    curr_row = 0
    for j in range(n):
        if curr_row < m:
            # Neu day la cot chua pivot thi them vao pivot_cols
            if abs(ref[curr_row][j]) > EPSILON:
                pivot_cols.append(j)
                curr_row += 1

    rank = len(pivot_cols)
    
    # Co so khong gian cot
    col_space = [[row[j] for row in A] for j in pivot_cols]

    # Co so khong gian dong
    row_space = [ref[i] for i in range(rank)]

    # Co so khong gian nghiem (he Ax=0 luon co nghiem)
    null_space = []
    # if x == None:
    #     # Vo nghiem, khong ton tai co so
    #     null_space = None
    # elif isinstance(x, list):
    #     # Co 1 nghiem, co so rong
    #     pass
    # elif isinstance(x, dict) and 'basis' in x:
    #     # Vo so nghiem
    #     null_space = x['basis']

    # return rank, col_space, row_space, null_space
    # Cac bien tu do la cac cot khong chua pivot
    free_cols = [j for j in range(n) if j not in pivot_cols]
    
    for free_var in free_cols:
        # Khoi tao vector nghiem toan so 0
        vector = [0.0] * n
        # Gan bien tu do hien tai = 1
        vector[free_var] = 1.0
        
        # The nguoc tu duoi len de tim gia tri cua cac bien pivot
        for i in range(rank - 1, -1, -1):
            p_col = pivot_cols[i]
            # Tinh tong (ref[i][j] * vector[j]) cho cac phan tu phia sau pivot
            s = sum(ref[i][j] * vector[j] for j in range(p_col + 1, n))
            # Giai bien pivot
            vector[p_col] = -s / ref[i][p_col]
            
        null_space.append(vector)

    return rank, col_space, row_space, null_space
