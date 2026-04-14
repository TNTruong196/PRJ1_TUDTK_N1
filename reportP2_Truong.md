# Báo Cáo Tính Toán Khoa Học: Phân Tích Chéo Hóa Ma Trận, Phân Rã Cholesky Và Ứng Dụng Giải Phương Trình

Báo cáo này trình bày nền tảng lý thuyết và chi tiết cài đặt của hai phương pháp phân tích ma trận quan trọng trong tính toán khoa học: Chéo hóa ma trận và Phân rã Cholesky. Báo cáo cũng phân tích cách ứng dụng các phương pháp này vào việc tối ưu hóa tính toán lũy thừa và giải hệ phương trình tuyến tính.

## Phần 1: Chéo hóa ma trận và ứng dụng (Diagonalization)

### 1.1. Cơ sở lý thuyết
Một ma trận vuông $A \in \mathbb{R}^{n \times n}$ được gọi là chéo hóa được nếu tồn tại một ma trận khả nghịch $P$ và một ma trận đường chéo $D$ sao cho:
$$A = P D P^{-1}$$
Trong đó, $D = \text{diag}(\lambda_1, \lambda_2, \dots, \lambda_n)$ chứa các giá trị riêng của $A$, và các cột của $P$ là các vector riêng tương ứng độc lập tuyến tính. Điều kiện cần và đủ để ma trận $A$ chéo hóa được là nó phải có đúng $n$ vector riêng độc lập tuyến tính.

### 1.2. Chi tiết triển khai mã nguồn (Implementation Details)

Việc triển khai chéo hóa ma trận trong tệp `diagonalization.py` không chỉ đơn thuần là gọi thư viện mà là một sự kết hợp giữa việc tự cài đặt các thuật toán nền tảng (from scratch) và sử dụng thư viện tối ưu khi cần thiết.

#### A. Tại sao lại triển khai như vậy? (Rationale)
1. **Tính giáo khoa và kiểm soát:** Việc tự cài đặt phương pháp Faddeev-LeVerrier và Durand-Kerner giúp hiểu rõ bản chất của đa thức đặc trưng và cách tìm nghiệm số trị thay vì coi chúng là một "hộp đen".
2. **Sự cân bằng giữa thủ công và hiệu suất:** Thuật toán tự cài đặt hoạt động tốt cho các ma trận nhỏ ($n \le 5$). Tuy nhiên, với ma trận lớn hơn, các vấn đề về sai số làm tròn và độ ổn định số trị (như hiện tượng Wilkinson) trở nên nghiêm trọng, do đó mã nguồn chuyển sang sử dụng NumPy (`np.linalg.eigvals`) để đảm bảo độ chính xác.
3. **Đảm bảo tính ổn định:** Sử dụng số điều kiện (Condition Number) để đánh giá ma trận $P$ giúp ngăn chặn việc trả về các kết quả sai lệch do ma trận gần suy biến.

#### B. Chức năng chi tiết của từng hàm

| Tên hàm | Chức năng chính | Ý nghĩa/Tại sao cần |
| :--- | :--- | :--- |
| `get_char_poly_coeffs` | Tính các hệ số của đa thức đặc trưng $p(\lambda) = \det(A - \lambda I)$ bằng phương pháp Faddeev-LeVerrier. | Tránh việc tính định thức bằng đệ quy (vốn rất chậm). Phương pháp này chỉ dùng nhân ma trận và tính vết (trace), phù hợp để lập trình. |
| `_durand_kerner` | Tìm tất cả các nghiệm (giá trị riêng) của đa thức đặc trưng cùng một lúc. | Đây là thuật toán tìm nghiệm đồng thời cho số phức, không cần tính đạo hàm như Newton-Raphson, giúp tìm đủ các giá trị riêng. |
| `_get_eigenvalues` | Hàm điều phối việc tìm giá trị riêng dựa trên kích thước ma trận. | Quyết định khi nào dùng thuật toán tự viết ($n \le 5$) và khi nào dùng thư viện NumPy ($n > 5$) để tối ưu độ ổn định. |
| `rank_and_basis` | (Hàm bổ trợ) Tính hạng và tìm cơ sở cho không gian nghiệm (null space). | Dùng để tìm các vector riêng bằng cách giải hệ phương trình tuyến tính $(A - \lambda I)v = 0$. |
| `_is_independent` | Kiểm tra tính độc lập tuyến tính của các vector riêng mới tìm được. | Đảm bảo ma trận $P$ được xây dựng từ các cột độc lập tuyến tính, đây là điều kiện bắt buộc để $P$ khả nghịch. |
| `diagonalize_matrix` | Hàm thực thi chính: Tổng hợp $P, D, P^{-1}$. | Thực hiện quy trình: Tìm giá trị riêng $\rightarrow$ Tìm vector riêng tương ứng $\rightarrow$ Kiểm tra số lượng vector $\rightarrow$ Nghịch đảo $P$. Nếu không đủ $n$ vector, hàm sẽ báo lỗi ma trận không chéo hóa được. |
| `matrix_power_via_diagonalization` | Tính $A^k$ dựa trên phân tích $P D^k P^{-1}$. | Ứng dụng thực tế của chéo hóa để tăng tốc độ tính toán lũy thừa từ $O(n^3 \log k)$ xuống còn $O(n^2)$. |

### 1.3. Ứng dụng: Lũy thừa ma trận
Một trong những ứng dụng quan trọng của chéo hóa là tính lũy thừa ma trận bậc cao với công thức:
$$A^k = P D^k P^{-1}$$
Trong đó $D^k = \text{diag}(\lambda_1^k, \dots, \lambda_n^k)$. Cài đặt trong hàm `matrix_power_via_diagonalization` cho phép giảm độ phức tạp từ $O(n^3 \log k)$ xuống còn $O(n^2)$ cho các phép nhân ma trận sau khi đã có kết quả phân tích.

---

## Phần 2: Phân rã Cholesky (Cholesky Decomposition)

### 2.1. Nền tảng toán học
Phân rã Cholesky được áp dụng cho ma trận đối xứng xác định dương (Symmetric Positive Definite - SPD). Ma trận $A$ được phân tích thành:
$$A = L L^T$$
Với $L$ là ma trận tam giác dưới có các phần tử đường chéo dương.

Công thức truy hồi được cài đặt bao gồm:
* **Phần tử đường chéo:** $L_{jj} = \sqrt{A_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}$
* **Phần tử ngoài đường chéo ($i > j$):** $L_{ij} = \frac{1}{L_{jj}} \left( A_{ij} - \sum_{k=1}^{j-1} L_{ik} L_{jk} \right)$

Phương pháp này tối ưu hơn phân rã LU thông thường khi chỉ tiêu tốn khoảng $1/2$ chi phí tính toán nhờ tận dụng tính đối xứng của ma trận SPD.

### 2.2. Chi tiết mã nguồn `cholesky_custom`
Hàm `cholesky_custom` thực hiện các bước kiểm tra nghiêm ngặt:
* Kiểm tra tính vuông và tính đối xứng của ma trận đầu vào với sai số $10^{-12}$.
* Kiểm tra tính xác định dương: Nếu trong quá trình tính toán, giá trị dưới dấu căn ($diag\_value$) $\le 0$, chương trình sẽ báo lỗi vì ma trận không phải là SPD.

---

## Phần 3: Ứng dụng giải hệ phương trình tuyến tính bằng phân rã

Việc sử dụng ma trận tam giác $L$ thu được từ phân rã Cholesky giúp giải các hệ phương trình tuyến tính một cách hiệu quả thông qua hai bước trung gian.

### 3.1. Giải hệ phương trình trực tiếp (Hàm `solve_via_cholesky`)
Đối với hệ phương trình vuông $Ax = b$, ta chuyển đổi thành $LL^Tx = b$ và giải theo quy trình:
1. **Thế tiến (Forward Substitution):** Giải hệ $Ly = b$ để tìm $y$. Vì $L$ là ma trận tam giác dưới, việc tìm $y_i$ chỉ phụ thuộc vào các giá trị $y_1, \dots, y_{i-1}$ đã tính trước đó.
2. **Thế lùi (Backward Substitution):** Giải hệ $L^Tx = y$ để tìm nghiệm cuối cùng $x$. Do $L^T$ là ma trận tam giác trên, ta giải ngược từ $x_n$ lên $x_1$.

### 3.2. Phương pháp bình phương tối thiểu (Hàm `solve_via_normal_equations`)
Trong trường hợp hệ phương trình có ma trận $A$ hình chữ nhật (thường là hệ vượt chuẩn), ta tìm nghiệm xấp xỉ tốt nhất thông qua phương trình chuẩn (Normal Equations):
$$A^TAx = A^Tb$$
Quy trình thực hiện trong code:
* Đặt $M = A^TA$ và $c = A^Tb$. Ma trận $M$ lúc này trở thành ma trận vuông, đối xứng xác định dương.
* Áp dụng `cholesky_custom(M)` để phân rã $M = LL^T$.
* Giải hệ $LL^Tx = c$ bằng phương pháp thế tiến và thế lùi tương tự như mục 3.1.

Cách tiếp cận này đảm bảo tính ổn định và tận dụng tối đa tốc độ của phân rã Cholesky cho các bài toán xấp xỉ dữ liệu thực tế.