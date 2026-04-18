## Báo cáo phần công việc 2
Người phụ trách: Nguyễn Thanh Nhật

Các công việc phụ trách:
- Cài đặt part1/inverse.py: Hàm tìm ma trận nghịch đảo bằng Gauss-Jordan
- Cài đặt part1/rank_basis.py: Tính hạng và tìm cơ sở cho 3 không gian cột, dòng, nghiệm
- Viết part1/part1_demo.ipynb: Viết hàm verify_solution và thực hiện test toàn bộ Phần 1
- Viết part3/benchmark.py: Bổ sung 2 hàm sinh Ma trận SPD ngẫu nhiên và Ma trận Hilbert 

---

### Báo cáo:

1. Tìm ma trận nghịch đảo bằng phương pháp Gauss-Jordan (`part1/inverse.py`)

- Input: Ma trận $A$.
- Output: Ma trận nghịch đảo $A^{-1}$ nếu $A$ khả nghịch.
- Ý tưởng thuật toán: Sử dụng ma trận bổ sung $[A|I]$ với $I$ là ma trận đơn vị cấp $n$. Thực hiện các phép biến đổi sơ cấp trên dòng để đưa vế trái ($A$) về dạng ma trận đơn vị $I$. Khi đó, vế phải ($I$) sẽ chuyển thành ma trận nghịch đảo $A^{-1}$.
- Các bước thuật toán chi tiết:
    1.  Khởi tạo: Tạo ma trận mở rộng $M = [A|I]$ kích thước $n \times 2n$.
    2.  Khử xuôi và rút gọn (Gauss-Jordan Elimination): Duyệt qua từng cột $j$ từ $0$ đến $n-1$:
        -   Chọn phần tử trục (Pivot): Tìm dòng $i \ge j$ có $|M_{i,j}|$ lớn nhất để thực hiện hoán vị dòng (giảm thiểu sai số làm tròn).
        -   Kiểm tra tính khả nghịch: Nếu $|M_{j,j}| < \epsilon$ (với $\epsilon$ rất nhỏ), kết luận ma trận suy biến và dừng.
        -   Chuẩn hóa dòng pivot: Chia toàn bộ dòng $j$ cho $M_{j,j}$ để đưa phần tử pivot về $1$.
        -   Khử các phần tử khác 0: Với mọi dòng $k \in \{0, \dots, n-1\}$ và $k \neq j$, thực hiện phép thay thế dòng: $R_k = R_k - M_{k,j} \cdot R_j$. Bước này triệt tiêu tất cả các phần tử trên và dưới pivot của cột $j$.
    3.  Trích xuất kết quả: Trả về ma trận bên phải (Ma trận I đã được biến đổi).

---

2. Tính Hạng và Tìm Cơ sở không gian (`part1/rank_basis.py`)

- Input: Ma trận $A$ kích thước $m \times n$.
- Output: Giá trị `rank`, cơ sở không gian cột, cơ sở không gian dòng, và cơ sở không gian nghiệm.
- Ý tưởng thuật toán: Đưa ma trận về dạng bậc thang (REF) hoặc bậc thang rút gọn (RREF). Dựa vào vị trí các cột chứa pivot để xác định hạng và các tập cơ sở tương ứng.
- Các bước thuật toán chi tiết:
    1.  Biến đổi REF/RREF: Thực hiện khử Gauss để đưa $A$ về dạng bậc thang. Lưu trữ chỉ số các cột chứa pivot.
    2.  Tính Rank: Hạng của ma trận bằng số lượng các cột chứa pivot (hoặc số dòng khác 0 trong REF).
    3.  Cơ sở không gian cột (Column Space): Là tập hợp các cột của ma trận gốc $A$ tại các vị trí chỉ số cột pivot đã tìm thấy.
    4.  Cơ sở không gian dòng (Row Space): Là tập hợp các dòng khác 0 của ma trận sau khi đã đưa về dạng REF.
    5.  Cơ sở không gian nghiệm (Null Space):
        -   Tiếp tục đưa ma trận về dạng RREF.
        -   Xác định các biến tự do (free variables) - các biến tương ứng với cột không có pivot.
        -   Giải hệ phương trình thuần nhất $Ax = 0$. Mỗi vector cơ sở của không gian nghiệm được tìm bằng cách gán lần lượt một biến tự do bằng $1$ và các biến tự do còn lại bằng $0$.

---

3. Demo và Kiểm chứng (`part1/part1_demo.ipynb`)

- Ta thực hiện việc kiểm thử cho các thuật toán ở phần I thông qua hàm `verify_solution(A, x, b)` với input và output như sau:
    - Input: Ma trận A, ma trận b và nghiệm x muốn kiểm chứng.
    - Output: True hoặc False ứng với việc $x$ có phải là nghiệm của phương trình $Ax=b$ hay không.
- Quá trình kiểm thử:
    - Tạo các trường hợp riêng biệt để kiểm thử như trường hợp phương trình vô nghiệm, có nghiệm duy nhất hay có vô số nghiệm.
    - Tìm nghiệm $x$ của hệ $Ax=b$ thông qua hàm `gaussian_eliminate(A, b)`.
    - Kiểm tra xem $x$ có phải là kết quả chính xác không thông qua hàm `verify_solution(A, x, b)`.
    - In ra kết quả kiểm thử.

---

4. Sinh ma trận Hilbert và Ma trận SPD (`part3/benchmark.py`)  
Phân tích thực nghiệm tính ổn định và hiệu năng của các phương pháp giải hệ phương trình. Việc sử dụng ma trận Hilbert và SPD giúp đánh giá tác động của số điều kiện đến sai số và thời gian thực thi trên nhiều quy mô khác nhau..
- Input: Kích thước ma trận $n$.
- Output: Ma trận Hilbert hoặc ma trận Xác định dương (SPD).
- Ý tưởng & Thuật toán:
    -   Ma trận Hilbert: Sử dụng công thức $H_{i,j} = \frac{1}{i + j + 1}$ (với $0 \le i, j < n$). Đây là ma trận cực kỳ nhạy cảm với sai số (ill-conditioned), dùng để thử độ chính xác của hàm `inverse.py`.
    -   Ma trận SPD: 1. Sinh ma trận ngẫu nhiên $M$.
        2. Tính $A = M^T M$ (tạo ma trận đối xứng nửa xác định dương).
        3. Cộng thêm $n \cdot I$ (với $I$ là ma trận đơn vị) vào $A$ để đảm bảo tất cả các trị riêng đều dương, tạo ra ma trận xác định dương.
        

### Bài học rút ra
- Biết cách đưa các thuật toán của đại số tuyến tính vào Python.
- Biết cách kiểm thử độ chính xác của cài đặt thuật toán.
- Hiểu rõ tầm quan trọng của việc chọn phần tử trục (pivoting) trong việc giảm thiểu sai số làm tròn khi làm việc với số thực trên máy tính.
- Nhận thức được sự khác biệt giữa lý thuyết toán học thuần túy và tính toán số học thực tế, đặc biệt là khái niệm "số không" (epsilon) trong lập trình.
- Thấy được tác động của số điều kiện thông qua ma trận Hilbert đối với độ chính xác của các thuật toán giải hệ phương trình tuyến tính.

### Khó khăn gặp phải
- Xử lý sai số dấu phẩy động: Trong quá trình khử Gauss-Jordan, các phép chia và trừ liên tục dẫn đến sai số tích lũy, khiến các phần tử lẽ ra bằng 0 lại mang một giá trị cực nhỏ, yêu cầu xác định ngưỡng ϵ phù hợp.
- Cài đặt logic tìm cơ sở không gian nghiệm (Null Space): Việc truy hồi từ ma trận RREF để xác định các biến tự do và biểu diễn các biến phụ thuộc theo biến tự do dưới dạng vector đòi hỏi tư duy thuật toán phức tạp hơn so với các không gian còn lại.

### Tài liệu tham khảo
- [1] G. Strang, Introduction to Linear Algebra, 5th ed. Wellesley, MA: Wellesley-Cambridge Press, 2016.
- [2] H. Anton và C. Rorres, Elementary Linear Algebra: Applications Version, 11th ed. Hoboken, NJ: Wiley, 2013.
- [3] D. C. Lay, S. R. Lay, và J. J. McDonald, Linear Algebra and Its Applications, 5th ed. Boston, MA: Pearson, 2015.