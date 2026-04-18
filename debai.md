# ĐỒ ÁN 1: Ma Trận và Cơ Sở của Tính Toán Khoa Học

**ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH**
**TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN**
**KHOA CÔNG NGHỆ THÔNG TIN**

| Thông tin | Chi tiết |
| :--- | :--- |
| **Môn học:** | Toán Ứng Dụng và Thống Kê |
| **Mã môn:** | MTH00051 |
| **Học kỳ:** | HỌC KỲ 2, 2025-2026 |

**Thông tin giảng viên (GV Thực hành):**
* ThS. Võ Nam Thục Đoan, ThS. Lê Nhựt Nam
* E-mail: `{vntdoan, lnnam}@fit.hcmus.edu.vn`

*(Tài liệu này dành riêng cho mục đích học thuật)*

---

## Mục lục
1. [Giới Thiệu Đồ Án](#giới-thiệu-đồ-án)
2. [Phần 1: Phép khử Gauss và Các Ứng Dụng](#1-phần-1-phép-khử-gauss-và-các-ứng-dụng)
3. [Phần 2: Phân Rã Ma Trận và Trực Quan Hóa với Manim](#2-phần-2-phân-rã-ma-trận-và-trực-quan-hóa-với-manim)
4. [Phần 3: Giải Hệ Phương Trình và Phân Tích Hiệu Năng (Điểm cộng)](#3-phần-3-giải-hệ-phương-trình-và-phân-tích-hiệu-năng-điểm-cộng)
5. [Yêu Cầu Chung và Hướng Dẫn Nộp Bài](#4-yêu-cầu-chung-và-hướng-dẫn-nộp-bài)
6. [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

## Giới Thiệu Đồ Án

### Mục tiêu tổng quát
Đồ án này tập trung vào ba nhóm kỹ thuật cốt lõi của đại số tuyến tính số trên máy tính:
1. **Phép khử Gauss:** nền tảng của việc giải hệ phương trình tuyến tính, tính định thức, nghịch đảo và hạng ma trận.
2. **Phân rã ma trận (Matrix Decompositions) và Chéo hóa (Diagonalization):** hiểu bản chất hình học và ứng dụng trực quan hóa.
3. **Ổn định số học và chi phí tính toán:** đánh giá thực nghiệm các phương pháp số trong thực tế.

Sinh viên được kỳ vọng không chỉ hiểu lý thuyết mà còn có khả năng cài đặt từ đầu (from scratch) bằng Python, trực quan hóa bằng Manim, và phân tích thực nghiệm về hiệu năng thuật toán.

### Các công cụ cho phép sử dụng trong đồ án:
* **Python:** Ngôn ngữ cài đặt chính. Khuyến khích sinh viên sử dụng phiên bản 3.10 hoặc cao hơn.
* **NumPy, SciPy, SymPy:** Kiểm chứng và so sánh kết quả (không dùng để cài đặt thuật toán).
* **math, fractions:** Hỗ trợ xử lý sai số, hiển thị kết quả tính toán (không bắt buộc, không dùng để cài đặt thuật toán).
* **Manim Community:** Trực quan hóa và tạo video demo. Khuyến khích sinh viên sử dụng phiên bản stable v.20.1.
* **Matplotlib:** Vẽ biểu đồ phân tích hiệu năng.
* **Jupyter Notebook:** Trình bày kết quả thực nghiệm.

### ⚠️ Lưu ý Quan Trọng:
* **Cấm sử dụng `numpy.array`:** Phần `numpy.array` bị cấm ở toàn bộ quá trình cài đặt thuật toán. Sinh viên không được xài mảng NumPy mà chỉ sử dụng kiểu dữ liệu cơ bản (ví dụ: `list` trong Python) để cài đặt thuật toán cốt lõi.
* **Sử dụng cho Verify:** Ở một số yêu cầu kiểm chứng (verification) kết quả, sinh viên có thể dùng các hàm từ NumPy để xác minh. Khi gọi hàm, hệ thống sẽ tự động chuyển đổi `list` -> `numpy.array` (hoặc sinh viên tự ép kiểu sang NumPy array để truyền vào hàm kiểm chứng).
* Tuyệt đối không được sử dụng trực tiếp các hàm có sẵn như `numpy.linalg.solve`, `numpy.linalg.inv`, `scipy.linalg.qr`, `scipy.linalg.lu`, `sympy.linsolve`, hay các phương thức có sẵn như `echelon_form`, `rref`, v.v... cho phần cài đặt thuật toán. **Các thư viện này chỉ được dùng để kiểm chứng kết quả.**
* phần cài đặt thuật toán bắt buộc là tự cài chứ không được dùng thư viện có sẵn.
---
* được dùng np.linalg.eigvals để tìm trị riêng trong part2 trong TH n>5
* đối với hàm gauss ở part1 với TH vô số nghiệm in ra nghiệm tổng quảt và trả về None

## 1. Phần 1: Phép khử Gauss và Các Ứng Dụng

**Tóm tắt yêu cầu Phần 1:** Cài đặt phép khử Gauss có partial pivoting từ đầu bằng Python, rồi sử dụng để: (1) giải hệ phương trình tuyến tính, (2) tính định thức, (3) tìm ma trận nghịch đảo, (4) tính hạng và tìm cơ sở.

### 1.1. Cơ Sở Lý Thuyết

#### 1.1.1. Phương pháp khử Gauss và Gauss-Jordan
Xét hệ phương trình tuyến tính $Ax=b$ với $A\in\mathbb{R}^{m\times n}$, $x\in\mathbb{R}^{n}$, $b\in\mathbb{R}^{m}$.

**Định nghĩa 1.1 (Ma trận tăng cường).** Ma trận tăng cường (augmented matrix) của hệ $Ax=b$ là:
$$[A|b]=\begin{pmatrix}a_{11}&a_{12}&\dots&a_{1n}&b_{1}\\a_{21}&a_{22}&\dots&a_{2n}&b_{2}\\\vdots&\vdots&\ddots&\vdots&\vdots\\a_{m1}&a_{m2}&\dots&a_{mn}&b_{m}\end{pmatrix}$$

**Định nghĩa 1.2 (Các phép biến đổi dòng sơ cấp).** Ba phép biến đổi dòng sơ cấp (elementary row operations) trên ma trận:
1. $R_{i}\leftrightarrow R_{j}$: Hoán đổi dòng $i$ và dòng $j$.
2. $R_{i}\leftarrow c\cdot R_{i}$, với $c\ne0$: Nhân dòng $i$ với hằng số $c$.
3. $R_{i}\leftarrow R_{i}+c\cdot R_{j}$: Cộng $c$ lần dòng $j$ vào dòng $i$.
Ba phép biến đổi này không làm thay đổi tập nghiệm của hệ phương trình.

**Định nghĩa 1.3 (Dạng bậc thang dòng - REF).** Ma trận $U$ ở dạng bậc thang dòng (Row Echelon Form, viết tắt REF) nếu:
1. Mọi dòng toàn số 0 nằm phía dưới các dòng khác 0.
2. Phần tử chỉ huy (pivot) của mỗi dòng khác 0 nằm bên phải pivot của dòng ngay trên nó.

**Định nghĩa 1.4 (Dạng bậc thang dòng rút gọn - RREF).** Ma trận $R$ ở dạng bậc thang dòng rút gọn (Reduced REF, viết tắt RREF) nếu ngoài điều kiện REF còn có:
3. Mỗi pivot bằng 1.
4. Mỗi cột chứa pivot có tất cả các phần tử còn lại bằng 0.

#### 1.1.2. Khử Gauss có chọn phần tử chốt (Partial Pivoting)
Trong cài đặt thực tế, cần áp dụng khử Gauss có chọn phần tử chốt hay partial pivoting để đảm bảo tính ổn định số học.

**Định lý 1.1 (Partial Pivoting).** Tại bước khử thứ $k$, chọn hàng $p$ sao cho:
$$|a_{pk}^{(k)}|=\max_{k\le i\le m}|a_{ik}^{(k)}|$$
rồi hoán đổi dòng $k$ và dòng $p$ trước khi thực hiện khử. Kỹ thuật này giảm thiểu đáng kể sai số làm tròn (round-off error) phát sinh trong tính toán dấu phẩy động.

#### 1.1.3. Tính Định Thức qua Khử Gauss
Sau khi đưa ma trận $A$ về dạng tam giác trên $U$ bằng phép khử Gauss với $s$ lần hoán đổi dòng, định thức được tính theo công thức:
$$\det(A)=(-1)^{s}\cdot\prod_{i=1}^{n}u_{ii}$$

#### 1.1.4. Ma Trận Nghịch Đảo bằng Gauss-Jordan
**Định lý 1.2.** Ma trận $A\in\mathbb{R}^{n\times n}$ khả nghịch khi và chỉ khi $\det(A)\ne0$. Nghịch đảo $A^{-1}$ được tìm bằng cách thực hiện biến đổi dòng đồng thời trên ma trận ghép $[A|I_{n}]$ cho đến khi đạt dạng $[I_{n}|A^{-1}]$.

#### 1.1.5. Hạng Ma Trận và Cơ Sở
**Định nghĩa 1.5 (Hạng ma trận).** Hạng (rank) của ma trận $A$, ký hiệu $\text{rank}(A)$, bằng số dòng khác 0 trong dạng REF của $A$, hoặc tương đương, bằng số cột pivot.

Từ dạng RREF, ta xác định được ba không gian con quan trọng:
* **Không gian cột (column space)** $\mathcal{C}(A)$: sinh bởi các cột pivot của $A$ gốc.
* **Không gian dòng (row space)** $\mathcal{R}(A)$: sinh bởi các dòng khác 0 trong RREF.
* **Không gian nghiệm (null space)** $\mathcal{N}(A)$: tập nghiệm của $Ax=0$.

### 1.2. Thuật Toán

**Thuật toán 1.1 (Phép khử Gauss với Partial Pivoting)**
* **Đầu vào:** Ma trận $A\in\mathbb{R}^{m\times n}$, vector $b\in\mathbb{R}^{m}$.
* **Đầu ra:** Nghiệm $x$, số lần hoán đổi $s$, danh sách chỉ số pivot.

1. Tạo ma trận tăng cường $M=[A|b]$, đặt $s=0$.
2. Với $k=1,2,...,\min(m, n)$:
   a. Tìm $p=\arg\max_{k\le i\le m}|M_{ik}|$.
      * Nếu $|M_{pk}|=0$: In ra `"không có pivot tại cột k"` hoặc `"hệ không có nghiệm duy nhất"`.
      * Nếu $|M_{pk}|<\epsilon$: Cảnh báo pivot gần bằng 0, hệ có thể không ổn định số học (ill-conditioned).
   b. Nếu $p\ne k$: hoán đổi dòng $k\leftrightarrow p$, tăng $s\leftarrow s+1$.
   c. Với $i=k+1,...,m$: tính nhân tử $l_{ik}=M_{ik}/M_{kk}$, cập nhật $M_{i,\cdot}\leftarrow M_{i,\cdot}-l_{ik}\cdot M_{k,\cdot}$
3. Thế ngược: Giải hệ tam giác trên $Ux=c$ từ dưới lên:
   $$x_{i}=\frac{1}{M_{ii}}\left(M_{i,n+1}-\sum_{j=i+1}^{n}M_{ij}x_{j}\right), \quad i=n,n-1,...,1$$
   *Lưu ý:* Với trường hợp vô số nghiệm, sinh viên cần đưa ra công thức nghiệm tổng quát.

### 1.3. Yêu Cầu Cài Đặt Python

Sinh viên cài đặt từ đầu (không dùng NumPy/SciPy/SymPy) các hàm sau:
1. `gaussian_eliminate(A, b)`: Trả về ma trận sau khi khử, nghiệm $x$, số lần hoán đổi.
2. `back_substitution(U, c)`: Giải hệ tam giác trên.
3. `determinant(A)`: Tính $\det(A)$ qua khử Gauss.
4. `inverse(A)`: Tính $A^{-1}$ bằng phương pháp Gauss-Jordan.
5. `rank_and_basis(A)`: Tính hạng và cơ sở của các không gian cột, dòng, nghiệm.
6. `verify_solution(A, x, b)`: Kiểm chứng kết quả bằng NumPy.

### 1.4. Tiêu Chí Đánh Giá - Phần 1

| Tiêu chí | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Cài đặt Gauss cơ bản** | Chạy đúng, có kiểm thử rõ ràng | 1.5 |
| **Partial Pivoting** | Xử lý đúng khi pivot nhỏ hoặc bằng 0 | 0.5 |
| **Tính định thức** | Đúng dấu và giá trị | 0.5 |
| **Ma trận nghịch đảo** | Gauss-Jordan, kiểm thử $AA^{-1}=I$ | 1.0 |
| **Hạng và cơ sở** | Đúng rank, trả về cơ sở các không gian | 1.0 |
| **Kiểm chứng** | So sánh kết quả với NumPy/SciPy | 0.5 |
| **Tổng Phần 1** | | **5.0** |

---

## 2. Phần 2: Phân Rã Ma Trận và Trực Quan Hóa với Manim

**Tóm tắt yêu cầu Phần 2:** Sinh viên chọn một kỹ thuật phân rã ma trận (QR, LU, SVD hoặc Cholesky), cài đặt bằng Python, và tạo video demo bằng Manim trực quan hóa quá trình phân rã cùng với chéo hóa ma trận.

### 2.1. Chéo Hóa Ma Trận (Diagonalizable Matrix)
**Định nghĩa 2.1 (Ma trận chéo hóa được).** Ma trận $A\in\mathbb{R}^{n\times n}$ chéo hóa được (diagonalizable) nếu tồn tại ma trận $P$ khả nghịch và ma trận đường chéo $D$ sao cho:
$$A=P D P^{-1}$$
$$D=\text{diag}(\lambda_{1},\lambda_{2},...,\lambda_{n})$$
trong đó $\lambda_{i}$ là các giá trị riêng (eigenvalues) và các cột của $P$ là các vector riêng tương ứng.

**Định lý 2.1 (Điều kiện chéo hóa).** Ma trận $A\in\mathbb{R}^{n\times n}$ chéo hóa được khi và chỉ khi $A$ có $n$ vector riêng độc lập tuyến tính. Điều kiện đủ: $A$ có $n$ giá trị riêng phân biệt.

Ứng dụng quan trọng của chéo hóa trong tính toán khoa học:
$$A^{k}=P D^{k}P^{-1}, \quad D^{k}=\text{diag}(\lambda_{1}^{k},...,\lambda_{n}^{k})$$
Điều này giúp giảm chi phí tính lũy thừa ma trận từ $O(n^{3}\log k)$ xuống $O(n^{2})$ sau khi đã có phân tích chéo hoá.

### 2.2. Các Kỹ Thuật Phân Rã – Chọn Một
Sinh viên tìm hiểu và chọn **một** trong các kỹ thuật phân rã ma trận được giới thiệu dưới đây:

**Tùy chọn A: Phân rã LU (LU Decomposition)**
* Dạng tổng quát: $PA=LU$
* $P$: Ma trận hoán vị (permutation matrix)
* $L$: Ma trận tam giác dưới với đường chéo bằng 1
* $U$: Ma trận tam giác trên
* Ý nghĩa: LU chính là phép khử Gauss được viết dưới dạng ma trận. Các nhân tử $l_{ik}$ dùng trong bước khử chính là các phần tử của $L$.
* Ứng dụng: Giải hiệu quả nhiều hệ $Ax_{1}=b_{1}, Ax_{2}=b_{2},...$ với cùng một ma trận $A$. Chi phí tính toán: $O(n^{3})$ cho bước phân rã, $O(n^{2})$ cho mỗi lần giải hệ.

**Tùy chọn B: Phân rã QR (QR Decomposition)**
* Dạng tổng quát: $A=QR$
* $A\in\mathbb{R}^{m\times n}$
* $Q\in\mathbb{R}^{m\times n}$: Ma trận trực chuẩn ($Q^{T}Q=I$)
* $R\in\mathbb{R}^{n\times n}$: Ma trận tam giác trên với các phần tử trên đường chéo chính đều dương, khả nghịch.
* Phương pháp cài đặt: Gram-Schmidt cổ điển (CGS) hoặc Householder reflections. Công thức Gram-Schmidt:
  $$q_{k}=\frac{a_{k}-\sum_{j=1}^{k-1}(a_{k}^{T}q_{j})q_{j}}{\left\|a_{k}-\sum_{j=1}^{k-1}(a_{k}^{T}q_{j})q_{j}\right\|}$$
* Ứng dụng: Bài toán bình phương tối thiểu (least squares), thuật toán tìm giá trị riêng (QR algorithm).

**Tùy chọn C: Phân rã SVD (Singular Value Decomposition)**
* Dạng tổng quát: $A=U\Sigma V^{T}$
* $U\in\mathbb{R}^{m\times m}$: Ma trận trực giao (left singular vectors)
* $\Sigma\in\mathbb{R}^{m\times n}$: Ma trận đường chéo $\Sigma=\text{diag}(\sigma_{1},\sigma_{2},\dots,\sigma_{p})$, với $\sigma_{i}$ là singular value của $A$
* $V\in\mathbb{R}^{n\times n}$: Ma trận trực giao (right singular vectors)
* Liên hệ với chéo hóa: $\sigma_{i}=\sqrt{\lambda_{i}(A^{T}A)}$ và SVD tương đương chéo hóa của $A^{T}A$.
* Ứng dụng: Nén dữ liệu, PCA, xấp xỉ hạng thấp: $A_{k}=\sum_{i=1}^{k}\sigma_{i}u_{i}v_{i}^{T}$ (xấp xỉ tốt nhất hạng $k$).

**Tùy chọn D: Phân rã Cholesky**
* Điều kiện áp dụng: $A$ đối xứng xác định dương (Symmetric Positive Definite - SPD).
* Dạng tổng quát: $A=LL^{T}$ với $L$ là ma trận tam giác dưới có đường chéo dương.
* Công thức tính lặp:
  $$L_{jj}=\sqrt{A_{jj}-\sum_{k=1}^{j-1}L_{jk}^{2}}$$
  $$L_{ij}=\frac{1}{L_{jj}}\left(A_{ij}-\sum_{k=1}^{j-1}L_{ik}L_{jk}\right), \quad i>j$$
* Chi phí tính toán: Chỉ bằng $\approx \frac{1}{2}$ chi phí LU, đây là ưu điểm lớn khi làm việc với ma trận SPD trong thực tế.

### 2.3. Yêu Cầu Trực Quan Hóa với Manim

Video demo Manim (tối thiểu 2 phút, tối đa 30 phút) phải bao gồm:
1. **Giới thiệu bài toán:** Hiển thị ma trận $A$ cụ thể, nêu rõ bài toán phân rã cần thực hiện.
2. **Trực quan hóa quá trình phân rã** (tùy theo phương pháp đã chọn):
   * LU: Minh họa từng bước khử Gauss, nhân tử $l_{ij}$, hình thành $L$ và $U$.
   * QR: Trực quan Gram-Schmidt trong không gian 2D/3D, biểu diễn vector trực giao hóa.
   * SVD: Trực quan hóa phép biến đổi hình học rotate-scale-rotate trên hình tròn đơn vị.
   * Cholesky: Hiển thị tính chất SPD của $A$, từng bước tính $L$.
3. **Chéo hóa:** Hiển thị giá trị riêng, vector riêng và phép phân tích $A=PDP^{-1}$.

### 2.4. Tiêu Chí Đánh Giá - Phần 2

| Tiêu chí | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Lý thuyết phân rã** | Trình bày đầy đủ, chính xác công thức | 0.5 |
| **Cài đặt Python** | Đúng, có kiểm chứng bằng NumPy | 1.5 |
| **Chéo hóa ma trận** | Cài đặt giá trị riêng và chéo hóa | 0.5 |
| **Video Manim** | Hoạt ảnh rõ ràng, đủ nội dung | 2.5 |
| **Tổng Phần 2** | | **5.0** |

*(Ghi chú: Nếu sinh viên cài đặt LU +0.5đ, SVD +1đ, Cholesky +1đ)*

---

## 3. Phần 3: Giải Hệ Phương Trình và Phân Tích Hiệu Năng (Điểm cộng)

**Tóm tắt yêu cầu Phần 3:** So sánh các phương pháp giải $Ax=b$, bao gồm Gauss (Phần 1), phân rã (Phần 2) và ít nhất một phương pháp lặp. Phân tích tính ổn định số và chi phí tính toán qua thực nghiệm.

### 3.1. Lý Thuyết Sai Số và Tính Ổn Định Số

#### 3.1.1. Số Điều Kiện (Condition Number)
**Định nghĩa 3.1 (Số điều kiện).** Số điều kiện của ma trận $A$ đối với chuẩn $p$ là:
$$\kappa_{p}(A)=\|A\|_{p}\cdot\|A^{-1}\|_{p}$$
Đối với chuẩn spectral (chuẩn 2): $\kappa_{2}(A)=\frac{\sigma_{\max}(A)}{\sigma_{\min}(A)}$.

**Định lý 3.1 (Phân tích sai số nghiệm).** Nếu $x$ là nghiệm đúng và $\hat{x}$ là nghiệm tính với nhiễu dữ liệu, thì:
$$\frac{\|\hat{x}-x\|}{\|x\|}\le\kappa(A)\cdot\frac{\|\delta b\|}{\|b\|}$$
Khi $\kappa(A)$ lớn, hệ bị điều kiện kém (ill-conditioned): sai số nhỏ trong dữ liệu đầu vào gây ra sai số lớn trong nghiệm.

#### 3.1.2. So Sánh Các Phương Pháp

| Phương pháp | Loại | Điều kiện áp dụng | Chi phí | Ổn định |
| :--- | :--- | :--- | :--- | :--- |
| Gauss (Partial Pivot) | Trực tiếp | Mọi $A$ khả nghịch | $O(n^{3})$ | Cao |
| LU với pivot | Trực tiếp | Mọi $A$ khả nghịch | $O(n^{3})$ | Cao |
| QR (Householder) | Trực tiếp | Mọi $A$ (kể cả chữ nhật) | $O(n^{3})$ | Rất cao |
| Cholesky | Trực tiếp | $A$ đối xứng xác định dương | $O(n^{3}/6)$ | Rất cao |
| Gauss-Seidel | Lặp | Chéo trội hàng / SPD | $O(k n^{2})$ | Trung bình |

#### 3.1.3. Phương Pháp Lặp Gauss-Seidel
Phân rã $A=D+L+U$ (đường chéo $D$, tam giác dưới thuần $L$, tam giác trên thuần $U$). Ta có công thức lặp:
$$x^{(k+1)}=-(D+L)^{-1}Ux^{(k)}+(D+L)^{-1}b$$

Viết theo từng thành phần:
$$x_{i}^{(k+1)}=\frac{1}{a_{ii}}\left(b_{i}-\sum_{j=1}^{i-1}a_{ij}x_{j}^{(k+1)}-\sum_{j=i+1}^{n}a_{ij}x_{j}^{(k)}\right), \quad i=1,...,n$$
Điều kiện hội tụ: $A$ chéo trội chặt hàng, tức $|a_{ii}|>\sum_{j\ne i}|a_{ij}|$ với mọi $i$.

### 3.2. Yêu Cầu Cài Đặt và Phân Tích
1. Cài đặt ít nhất 3 phương pháp giải $Ax=b$ (bao gồm Gauss từ Phần 1 và phân rã từ Phần 2).
2. Thực nghiệm với ma trận ngẫu nhiên kích thước $n\in\{50,100,200,500,1000\}$:
   * Đo thời gian thực thi (trung bình 5 lần chạy).
   * Đo sai số tương đối: $\|A\hat{x}-b\|_{2}/\|b\|_{2}$.
   * Vẽ đồ thị log-log: thời gian vs $n$ và so sánh với đường lý thuyết $O(n^{3})$.
3. Phân tích ổn định với hai loại ma trận:
   * Ma trận Hilbert $H_{n}$ (số điều kiện rất lớn - ill-conditioned).
   * Ma trận ngẫu nhiên SPD (số điều kiện nhỏ - well-conditioned).
4. Báo cáo: Trình bày trong Jupyter Notebook với bảng số liệu, biểu đồ có chú thích đầy đủ.

### 3.3. Tiêu Chí Đánh Giá - Phần 3

| Tiêu chí | Mô tả | Điểm |
| :--- | :--- | :--- |
| **Cài đặt phương pháp lặp** | Đúng, có kiểm tra điều kiện hội tụ | 0.5 |
| **Thực nghiệm thời gian** | Đủ kích thước, có đồ thị log-log | 0.5 |
| **Phân tích ổn định số** | Ma trận Hilbert vs ma trận ngẫu nhiên | 0.5 |
| **Nhận xét và kết luận** | Phân tích có chiều sâu, có số liệu | 0.25 |
| **Trình bày Notebook** | Rõ ràng, có visualization đầy đủ | 0.25 |
| **Tổng Phần 3** | | **2.0** |

---

## 4. Yêu Cầu Chung và Hướng Dẫn Nộp Bài

### 4.1. Cấu Trúc Báo Cáo
Báo cáo viết bằng LaTeX hoặc Markdown (xuất ra PDF), bao gồm các mục:
1. Trang bìa: Họ và tên, MSSV, nhóm, giảng viên hướng dẫn.
2. Mục lục.
3. Phần 1, 2, 3: Theo cấu trúc đã nêu ở trên.
4. Kết luận: Tóm tắt kết quả đạt được, bài học rút ra, khó khăn gặp phải.
5. Tài liệu tham khảo: Ít nhất 5 tài liệu (sách, bài báo hoặc tài liệu chính thống).
6. Phụ lục (nếu có): Bảng số liệu chi tiết, code bổ sung.

### 4.2. Cấu Trúc Thư Mục Nộp Bài
Sinh viên có thể cấu trúc đồ án theo gợi ý như sau:

```text
Group_<ID>/
|-- README.md
|-- requirements.txt
|-- report/
|   |-- report.pdf
|   |-- report.tex
|-- part1/
|   |-- gaussian.py
|   |-- determinant.py
|   |-- inverse.py
|   |-- rank_basis.py
|   |-- part1_demo.ipynb
|-- part2/
|   |-- decomposition.py
|   |-- diagonalization.py
|   |-- manim_scene.py
|   |-- demo_video.mp4
|-- part3/
|   |-- solvers.py
|   |-- benchmark.py
|   |-- analysis.ipynb
```

### 4.3. Yêu Cầu Kỹ Thuật
* Sử dụng ngôn ngữ lập trình Python, viết code rõ ràng dễ hiểu (clean code), có chú thích và giải thích cho việc cài đặt thuật toán. *(Nhắc lại: cấm sử dụng cấu trúc `numpy.array` để làm lõi thuật toán).*
* Sử dụng Manim để trực quan hóa và minh họa các bước thuật toán thông qua video.
* Sinh viên sử dụng `requirements.txt` để quản lý dependencies (nếu sử dụng pip) hoặc `*.yml` (nếu sử dụng conda).
* Video: Định dạng MP4, độ phân giải phù hợp 720p, thời lượng $\ge2$ phút.
* Kiểm thử/đánh giá: Mỗi hàm có ít nhất 5 test cases, bao gồm các trường hợp đặc biệt (edge cases).

### 4.4. Phân Công Nhóm và Đạo Đức Học Thuật
* Báo cáo phải ghi rõ phân công công việc của từng thành viên trong nhóm.
* Giảng viên sẽ chọn lựa một số nhóm để vấn đáp nếu cần thiết.
* Nghiêm cấm sao chép code hoặc báo cáo từ nhóm khác hay từ Internet mà không trích dẫn nguồn.
* Sử dụng công cụ AI (ChatGPT, GitHub Copilot, v.v.) để gợi ý là được phép, nhưng sinh viên phải hiểu và giải thích được toàn bộ code mình nộp.
* **Vi phạm đạo đức học thuật dẫn đến điểm 0 toàn bộ đồ án.**

### 4.5. Thang Điểm Tổng Hợp

| Phần | Nội dung | Điểm tối đa | Trọng số |
| :--- | :--- | :--- | :--- |
| **1** | Phép khử Gauss và ứng dụng | 5.0 | 38.5% |
| **2** | Phân rã ma trận + Video Manim | 6.0 | 46.2% |
| **3** | Phân tích hiệu năng và ổn định | 2.0 | 15.4% |
| **Tổng cộng** | | **13.0** | **100%** |

Điểm cuối cùng sẽ được quy về thang điểm 10.
Gọi P1, P2, P3 lần lượt là điểm phần 1, 2 và 3 (trong đó Phần 3 là điểm cộng thêm). Điểm cuối cùng:
$$\xi=\min\left(\frac{P1+P2}{11}\times 10+P3, 10\right)$$

---

### Tóm Tắt Sản Phẩm Nộp Bài
* [ ] Báo cáo `report.pdf` (bắt buộc)
* [ ] Source code đầy đủ kèm `README.md` và `requirements.txt`
* [ ] Video Manim `demo_video.mp4` (Phần 2, bắt buộc)
* [ ] Jupyter Notebooks: `part1_demo.ipynb` và `analysis.ipynb`

**Nộp qua:** Moodle của Khoa
**Hạn nộp:** ngày 20/4/2025, trước 23:59

---

## Tài Liệu Tham Khảo
[1] Gilbert Strang. Introduction to Linear Algebra, 6th ed. Wellesley-Cambridge Press, 2023.
[2] Lloyd N. Trefethen & David Bau III. Numerical Linear Algebra. SIAM, 1997.
[3] Gene H. Golub & Charles F. Van Loan. Matrix Computations, 4th ed. Johns Hopkins University Press, 2013.
[4] Cleve Moler. Numerical Computing with MATLAB. SIAM, 2004. Truy cập miễn phí: https://www.mathworks.com/moler/chapters.html
[5] Manim Community Developers. Manim-Mathematical Animation Framework, v0.18. 2024. https://docs.manim.community
[6] Jake VanderPlas. Python Data Science Handbook. O'Reilly, 2016. https://jakevdp.github.io/PythonDataScienceHandbook/
[7] 3Blue1Brown. Essence of Linear Algebra (chuỗi video). YouTube, 2016. https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab