import copy
from gaussian import gaussian_eliminate

EPSILON = 1e-9

def rank_and_basis(A):
    if not A or not A[0]:
        return 0, [], [], []

    a = copy.deepcopy(A)
    m = len(A)
    n = len(A[0])

    # Tạo vector b toàn số 0
    b = [0.0] * m

    # Dùng hàm khử Gauss có sẵn để tìm ma trận tam giác trên
    ref, x, _ = gaussian_eliminate(a, b)

    # Xác định các cột chứa pivot
    pivot_cols = []
    curr_row = 0
    for j in range(n):
        if curr_row < m:
            # Nếu đây là cột chứa pivot thì thêm vào pivot_cols
            if abs(ref[curr_row][j]) > EPSILON:
                pivot_cols.append(j)
                curr_row += 1

    rank = len(pivot_cols)
    
    # Cơ sở không gian cột
    col_space = [[row[j] for row in A] for j in pivot_cols]

    # Cơ sở không gian dòng
    row_space = [ref[i] for i in range(rank)]

    # Cơ sở không gian nghiệm (hệ Ax=0 luôn có nghiệm)
    null_space = []
    if x == None:
        # Vô nghiệm, không tồn tại cơ sở
        null_space = None
    elif isinstance(x, list):
        # Có 1 nghiệm, cơ sở rỗng
        pass
    elif isinstance(x, dict) and 'basis' in x:
        # Vô số nghiệm
        null_space = x['basis']

    return rank, col_space, row_space, null_space
