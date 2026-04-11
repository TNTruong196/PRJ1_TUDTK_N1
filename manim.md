## ràng buộc:
Các công cụ cho phép sử dụng trong đồ án:
- Python: Ngôn ngữ cài đặt chính. Khuyến khích sinh viên sử dụng phiên bản 3.10 hoặc
cao hơn.
-  NumPy, SciPy, SymPy: Kiểm chứng và so sánh kết quả (không dùng để cài đặt thuật
toán).
-  math, fractions: Hỗ trợ xử lý sai số, hiển thị kết quả tính toán (không bắt buộc, không
dùng để cài đặt thuật toán).
-  ManimCommunity:Trựcquanhóavàtạovideodemo.Khuyếnkhíchsinhviênsửdụng
phiên bản stable v.20.1.
-  Matplotlib: Vẽ biểu đồ phân tích hiệu năng.
-  Jupyter Notebook: Trình bày kết quả thực nghiệm.
**lưu ý: ** không dùng numpy.array cho các hàm thông thường kh phải hàm kiểm thử.

## Phần 1: Giới thiệu bài toán (Khoảng 2 - 3 phút)
Mục tiêu: Giới thiệu định nghĩa phân rã Cholesky và chọn một ma trận $A$ cụ thể.
Scene 1 (Tiêu đề): Hiển thị Text "Phân rã Cholesky (Cholesky Decomposition)".
Scene 2 (Dạng tổng quát): Dùng hiệu ứng viết (Write) để hiển thị công thức: $A = LL^T$.
Làm nổi bật chữ $L$ và hiện dòng chú thích: "L là ma trận tam giác dưới có đường chéo dương".
Có thể vẽ minh họa hình dáng ma trận tam giác dưới (các phần tử phía trên đường chéo bằng 0) để người xem dễ hình dung.
Scene 3 (Khởi tạo bài toán): Đưa ra một ma trận vuông $A$ cụ thể có kích thước $3 \times 3$ (khuyến nghị dùng $3 \times 3$ để vừa đủ trực quan, không quá dài dòng).
Ví dụ ma trận SPD: $A = \begin{bmatrix} 4 & 12 & -16 \\ 12 & 37 & -43 \\ -16 & -43 & 98 \end{bmatrix}$
## Phần 2: Hiển thị tính chất SPD của ma trận A (Khoảng 3 - 5 phút)
Mục tiêu: Thỏa mãn yêu cầu "Hiển thị tính chất SPD của A" trong đề bài đồ án.
Scene 1 (Tính đối xứng - Symmetric): * Hiển thị ma trận $A$.
Tạo bản sao $A^T$ và sử dụng hiệu ứng lật (flip/rotate) qua đường chéo chính.
Cho hai ma trận trùng khớp vào nhau để khẳng định $A = A^T$.
Scene 2 (Tính xác định dương - Positive Definite):
Sử dụng tiêu chuẩn Sylvester (các định thức con chính - leading principal minors phải $> 0$).
Bước 1: Highlight phần tử $A_{11}$, tính $\Delta_1 = 4 > 0$.
Bước 2: Highlight ma trận con $2 \times 2$ ở góc trái trên, tính $\Delta_2 = (4)(37) - (12)(12) = 148 - 144 = 4 > 0$.
Bước 3: Hiển thị công thức tính định thức ma trận $3 \times 3$ của $A$, tính $\Delta_3 > 0$.
Kết luận $\implies A$ là ma trận đối xứng xác định dương (SPD), đủ điều kiện phân rã Cholesky.
## Phần 3: Trực quan hóa từng bước tính L (Khoảng 7 - 10 phút)
Mục tiêu: Thể hiện rõ sự áp dụng "Công thức tính lặp" để lấp đầy ma trận $L$.
Scene 1 (Chuẩn bị không gian làm việc): * Thu nhỏ ma trận $A$ để sang một góc.
Hiển thị công thức lặp (từ hình 1 của bạn) ở một góc khác.
Tạo một khung ma trận $L$ ($3 \times 3$) trống, với các phần tử phía trên đường chéo đã được điền số $0$.
Scene 2 (Tính Cột 1 của L):
Tính $L_{11}$: Highlight $A_{11}$. Áp dụng công thức $L_{11} = \sqrt{A_{11}}$. Hiện phép tính $\sqrt{4} = 2$. Di chuyển (Transform) số $2$ vào vị trí $L_{11}$.
Tính $L_{21}$: Highlight $A_{21}$ và $L_{11}$. Áp dụng công thức $L_{i1} = \frac{A_{i1}}{L_{11}}$. Hiện phép tính $12 / 2 = 6$. Bay số $6$ vào vị trí $L_{21}$.
Tính $L_{31}$: Tương tự, $\frac{-16}{2} = -8$. Bay số $-8$ vào vị trí $L_{31}$.
Scene 3 (Tính Cột 2 của L):
Tính $L_{22}$: Highlight $A_{22}$ và $L_{21}$. Áp dụng công thức $L_{22} = \sqrt{A_{22} - L_{21}^2}$. Hiện phép tính $\sqrt{37 - 6^2} = \sqrt{1} = 1$. Điền vào $L_{22}$.
Tính $L_{32}$: Áp dụng công thức $L_{32} = \frac{1}{L_{22}}(A_{32} - L_{31}L_{21})$. Làm nổi bật (highlight) các biến tương ứng đổi màu, hiện phép tính và kết quả, bay số vào ô $L_{32}$.
Scene 4 (Tính Cột 3 của L):
Tính $L_{33}$: Áp dụng công thức $L_{33} = \sqrt{A_{33} - (L_{31}^2 + L_{32}^2)}$. Đưa kết quả vào $L_{33}$.
Scene 5 (Nghiệm thu):
Hiển thị đầy đủ ma trận $L$ và $L^T$.
Thực hiện phép nhân $L \times L^T$ bằng animation nhân ma trận để chứng minh kết quả trả về đúng bằng ma trận $A$ ban đầu.
## Phần 4: Ưu điểm của Cholesky (Khoảng 1 - 2 phút)
Mục tiêu: Nêu bật chi phí tính toán (yêu cầu trong hình 1).
Scene 1: Đưa ra dòng text: "Chi phí tính toán".
Scene 2: Tạo một biểu đồ Bar Chart đơn giản hoặc hai khối hộp cạnh nhau: Khối "LU Decomposition" và khối "Cholesky".
Hiển thị animation khối lượng phép tính của Cholesky thu nhỏ lại chỉ còn bằng một nửa (1/2) khối LU.
Hiện dòng chú thích: "Chỉ bằng $\approx \frac{1}{2}$ chi phí LU, đây là ưu điểm lớn khi làm việc với ma trận SPD".
## Phần 5: Chéo hóa ma trận (Khoảng 5 - 8 phút)
Mục tiêu: Thỏa mãn yêu cầu số 3 của đề bài (Hiển thị giá trị riêng, vector riêng và phép phân tích $A = PDP^{-1}$). Lưu ý: Vì A là ma trận đối xứng, phân tích này thường được viết là $A = Q \Lambda Q^T$, nhưng bạn cứ bám sát ký hiệu $PDP^{-1}$ của đề.
Scene 1 (Tìm Giá trị riêng - Eigenvalues):
Hiển thị phương trình đặc trưng $\det(A - \lambda I) = 0$.
(Không cần giải tay bước này trên Manim vì rất dài) Hiển thị trực tiếp các nghiệm $\lambda_1, \lambda_2, \lambda_3$.
Mẹo nhỏ: Nhấn mạnh rằng vì $A$ là ma trận SPD, toàn bộ các $\lambda_i$ đều là số thực và $> 0$.
Scene 2 (Tìm Vector riêng - Eigenvectors & Ma trận P):
Hiển thị các vector riêng $v_1, v_2, v_3$ tương ứng với từng $\lambda$.
Gộp các vector riêng này thành các cột để tạo nên ma trận $P$. (Dùng animation các vector di chuyển lại gần nhau tạo thành khung ma trận).
Scene 3 (Ma trận đường chéo D):
Tạo ma trận $D$ với các phần tử trên đường chéo chính là $\lambda_1, \lambda_2, \lambda_3$. Các phần tử còn lại bằng 0.
Scene 4 (Tổng hợp công thức):
Tính ma trận nghịch đảo $P^{-1}$. (Có thể hiện kết quả trực tiếp).
Hiển thị công thức tổng quát: $A = PDP^{-1}$.
Xếp 4 ma trận $A$, $P$, $D$, $P^{-1}$ lên màn hình để thể hiện sự tương quan.
Lời khuyên kỹ thuật Manim:
Sử dụng thư viện MathTex hoặc Matrix của Manim để render các ma trận và công thức đẹp mắt.
Dùng VGroup để gom nhóm các phần tử của ma trận, giúp bạn dễ dàng .animate màu sắc của từng ô (ví dụ: dùng hàm get_entries() để đổi màu ô đang được tính toán).
Nên tạo các hàm hỗ trợ (helper functions) trong Python cho việc highlight phần tử ma trận (ví dụ: highlight_cell(matrix, row, col, color)) để tái sử dụng nhiều lần trong Phần 3.
<!-- # Kịch bản Trực quan hóa Phân rã Cholesky bằng Manim

**Đồ án:** Ma trận và Tính toán Khoa học (FIT-HCMUS)
**Chủ đề:** Phân rã Cholesky ($A = LL^T$)

---

## 1. Giới thiệu bài toán (Introduction)
* **Mục tiêu:** Định nghĩa bài toán và thiết lập mục tiêu.
* **Nội dung hiển thị:**
    * Tiêu đề: **Phân rã Cholesky (Cholesky Decomposition)**.
    * Công thức tổng quát: $A = LL^T$.
    * Chú thích: $L$ là ma trận tam giác dưới (lower triangular matrix) có các phần tử đường chéo dương ($L_{ii} > 0$).
    * Khởi tạo ma trận ví dụ $A$ (kích thước $3 \times 3$):
        $$A = \begin{bmatrix} 4 & 12 & -16 \\ 12 & 37 & -43 \\ -16 & -43 & 98 \end{bmatrix}$$

---

## 2. Kiểm tra điều kiện áp dụng (SPD Verification)
* **Mục tiêu:** Chứng minh $A$ là ma trận đối xứng xác định dương (Symmetric Positive Definite - SPD).
* **Các bước trực quan:**
    1.  **Tính đối xứng ($A = A^T$):** Sử dụng animation lật ma trận qua đường chéo chính để thấy sự trùng khớp.
    2.  **Tính xác định dương (Tiêu chuẩn Sylvester):**
        * $\Delta_1 = \det([4]) = 4 > 0$.
        * $\Delta_2 = \det\left(\begin{bmatrix} 4 & 12 \\ 12 & 37 \end{bmatrix}\right) = 148 - 144 = 4 > 0$.
        * $\Delta_3 = \det(A) = \dots > 0$.
    * **Kết luận:** $A$ là SPD $\implies$ Có thể phân rã Cholesky.

---

## 3. Trực quan hóa quá trình phân rã (Step-by-step L Calculation)
* **Mục tiêu:** Sử dụng công thức lặp để tìm các phần tử của $L$.
* **Công thức lặp:**
    * $L_{jj} = \sqrt{A_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}$
    * $L_{ij} = \frac{1}{L_{jj}} \left( A_{ij} - \sum_{k=1}^{j-1} L_{ik}L_{jk} \right), \quad i > j$

* **Tiến trình thực hiện trên Manim:**
    * **Cột 1:**
        * $L_{11} = \sqrt{A_{11}} = \sqrt{4} = 2$.
        * $L_{21} = A_{21}/L_{11} = 12/2 = 6$.
        * $L_{31} = A_{31}/L_{11} = -16/2 = -8$.
    * **Cột 2:**
        * $L_{22} = \sqrt{A_{22} - L_{21}^2} = \sqrt{37 - 6^2} = 1$.
        * $L_{32} = \frac{1}{L_{22}}(A_{32} - L_{31}L_{21}) = \frac{1}{1}(-43 - (-8)(6)) = 5$.
    * **Cột 3:**
        * $L_{33} = \sqrt{A_{33} - (L_{31}^2 + L_{32}^2)} = \sqrt{98 - ((-8)^2 + 5^2)} = \sqrt{98 - 89} = 3$.

* **Hiệu ứng:** Khi tính mỗi phần tử, highlight các ô tương ứng trong ma trận $A$ và các ô đã tính trong $L$. Sau đó "bay" giá trị kết quả vào vị trí tương ứng trong ma trận $L$ trống.

---

## 4. Phân tích Chi phí tính toán (Computational Cost)
* **Mục tiêu:** Giải thích lý do Cholesky tối ưu hơn LU cho ma trận SPD.
* **Nội dung:**
    * Hiển thị biểu đồ hoặc văn bản so sánh:
        * **LU Decomposition:** $\approx \frac{2}{3}n^3$ flops.
        * **Cholesky Decomposition:** $\approx \frac{1}{3}n^3$ flops.
    * **Kết luận:** Chi phí tính toán của Cholesky chỉ bằng khoảng **1/2** so với LU.

---

## 5. Chéo hóa ma trận (Diagonalization)
* **Mục tiêu:** Phân tích $A = PDP^{-1}$.
* **Các thành phần:**
    * **Giá trị riêng ($\lambda$):** Giải phương trình đặc trưng $\det(A - \lambda I) = 0$.
    * **Vector riêng ($v$):** Tìm không gian nghiệm tương ứng với mỗi $\lambda$.
    * **Ma trận $P$:** Tập hợp các vector riêng làm cột.
    * **Ma trận $D$:** Ma trận đường chéo chứa các giá trị riêng.
* **Animation:** Hiển thị sự liên kết giữa các giá trị riêng và ma trận đường chéo thông qua các hiệu ứng màu sắc tương ứng.

---

## 6. Tổng kết (Conclusion)
* Kiểm tra lại kết quả: Hiển thị phép nhân $L \cdot L^T$ để quay về ma trận $A$.
* Thông tin sinh viên/nhóm thực hiện. --> -->