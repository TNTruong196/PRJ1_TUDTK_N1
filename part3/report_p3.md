# BÁO CÁO PHẦN 3: PHƯƠNG PHÁP LẶP GAUSS-SEIDEL VÀ BENCHMARK

**Người thực hiện:** Trần Lê Đức Việt

## 1. Cài đặt thuật toán Gauss-Seidel

**Cơ sở lý thuyết:**
Phương pháp Gauss-Seidel là một phương pháp lặp để giải hệ phương trình tuyến tính $Ax=b$. Cải tiến hơn so với phương pháp Jacobi, Gauss-Seidel sử dụng ngay lập tức các giá trị $x_j^{(k+1)}$ vừa được tính ở bước hiện tại để tính các giá trị $x_i^{(k+1)}$ tiếp theo, giúp tăng tốc độ hội tụ.

**Công thức cập nhật:**
$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij} x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij} x_j^{(k)} \right)$$

**Triển khai thực tế:**
- Thuật toán được nhóm lập trình **thuần bằng Python (Pure Python)**, hoàn toàn không phụ thuộc vào bất kỳ thư viện toán học nào (kể cả trong việc khởi tạo mảng hay tính chuẩn sai số). Điều này giúp nhóm bám sát và thể hiện rõ việc nắm vững bản chất toán học của từng vòng lặp trong thuật toán.
- **Điều kiện hội tụ:** Sử dụng chuẩn vô cùng (infinity norm) để kiểm tra độ chênh lệch lớn nhất giữa vector nghiệm ở hai bước lặp liên tiếp. Vòng lặp dừng lại khi $\max |x^{(k+1)}_i - x^{(k)}_i| < \text{tolerance}$ (mặc định $10^{-10}$).
- Hàm được trang bị tham số `max_iterations` để chủ động dừng chương trình và cảnh báo nếu hệ phương trình quá xấu, không thể hội tụ.

## 2. Thiết lập kịch bản Benchmark

Đoạn mã `benchmark.py` được xây dựng để đối chiếu hiệu suất và độ chính xác của hàm Gauss-Seidel tự code với hàm giải trực tiếp chuẩn của thư viện `numpy.linalg.solve`.

Để đánh giá toàn diện, nhóm sử dụng hai bộ dữ liệu test đặc thù (với ma trận kích thước $N \times N$):
1. **Ma trận Đối xứng Xác định dương (SPD - Symmetric Positive Definite):** Được sinh ngẫu nhiên theo công thức $A = M^T M + nI$. Đây là dạng ma trận có tính chất cực kỳ ổn định (well-conditioned), đảm bảo thuật toán Gauss-Seidel chắc chắn hội tụ theo lý thuyết.
2. **Ma trận Hilbert:** Sinh theo công thức $H_{ij} = \frac{1}{i+j+1}$. Đây là dạng ma trận có "số điều kiện" (condition number) khổng lồ, đại diện cho các hệ phương trình rất xấu (ill-conditioned) để ép giới hạn (stress-test) các thuật toán tính toán số.

## 3. Kết quả đánh giá và Nhận xét

* **Kiểm thử trên ma trận SPD (Kịch bản chuẩn):**
  - **Về độ chính xác:** Thuật toán tự code hoạt động hoàn toàn chính xác. Sai số tuyệt đối lớn nhất giữa phương pháp Gauss-Seidel và thư viện Numpy là cực kỳ nhỏ (thường ở mức $10^{-14}$ đến $10^{-15}$).
  - **Về thời gian thực thi:** Phương pháp lặp tự code có thời gian chạy chậm hơn một chút so với hàm của Numpy. Nguyên nhân là do Numpy được biên dịch bằng C/Fortran ở tầng dưới, trong khi đoạn code của nhóm đang sử dụng vòng lặp `for` lồng nhau của Python nên chịu độ trễ của ngôn ngữ thông dịch.

* **Kiểm thử trên ma trận Hilbert (Kịch bản ép lỗi):**
  - Trái ngược với sự mượt mà ở trên, khi gặp ma trận Hilbert, thuật toán Gauss-Seidel hội tụ cực kỳ chậm, thường xuyên chạm ngưỡng `max_iterations` hoặc cho ra sai số lớn hơn đáng kể so với phương pháp giải trực tiếp của Numpy.
  - **Nhận xét:** Điều này không phải do code sai, mà phản ánh đúng bản chất toán học: các phương pháp lặp rất nhạy cảm và dễ bị khuếch đại sai số làm tròn khi đối mặt với ma trận ill-conditioned. 

**Kết luận chung:** Hàm `solve_gauss_seidel` do nhóm xây dựng hoạt động chính xác, ổn định và hội tụ tốt đối với các hệ phương trình có cấu trúc ma trận chuẩn. Để tối ưu hóa thời gian chạy cho các hệ cực lớn trong tương lai, thuật toán cần được cải tiến bằng cách vector hóa (vectorization) các phép tính mảng thay vì dùng vòng lặp thuần.