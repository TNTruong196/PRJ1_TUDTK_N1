# PRJ1_TUDTK_N1: Ma trận và Cơ sở của Tính toán Khoa học

## Giới thiệu

Đồ án này là một dự án học tập toàn diện về **lý thuyết ma trận** và **ứng dụng tính toán khoa học**. Dự án bao gồm các phần đặc biệt như phép khử Gauss, phân rã ma trận, chéo hóa, cùng với các so sánh hiệu năng (benchmark) và trực quan hóa toán học bằng video.

**Khóa học:** Toán Ứng dụng và Thống kê  
**Ngôn ngữ lập trình:** Python  
**Phiên bản Python được yêu cầu:** 3.10+

---

## Thông tin nhóm

| Thông tin | Chi tiết |
|-----------|---------|
| **Nhóm** | Nhóm 3 |
| **Lớp** | 24CTT1 |
| **Thành viên** | 24120486 - Trần Nhật Trường<br>24120111 - Nguyễn Thanh Nhật<br>24120215 - Nguyễn Ngọc Phúc<br>24120245 - Trần Lê Đức Việt<br>24120438 - Trần Nguyên Tân |
| **GVHD** |  ThS. Lê Nhựt Nam<br>ThS. Võ Nam Thục Đoan|
| **Ngày nộp** | 18/4/2026 |

---

## Cấu trúc đồ án

Dự án được chia thành **3 phần chính**, mỗi phần giải quyết một tập hợp các vấn đề cụ thể:

### 📦 Phần 1: Phép khử Gauss và các ứng dụng (`part1/`)

Thực hiện các phép toán cơ bản trên ma trận và các ứng dụng:
- **`gaussian.py`** - Thuật toán khử Gauss (Gaussian Elimination)
- **`determinant.py`** - Tính định thức ma trận
- **`inverse.py`** - Tìm ma trận nghịch đảo
- **`rank_basis.py`** - Tính hạng ma trận và cơ sở không gian
- **`matrix_utils.py`** - Các hàm tiện ích xử lý ma trận
- **`part1_demo.ipynb`** - Notebook demo các chức năng của Phần 1
- **`Nhat_report.md`** - Báo cáo chi tiết Phần 1

### 🎥 Phần 2: Chéo hóa ma trận và mô phỏng Manim (`part2/`)

Thực hiện chéo hóa ma trận và tạo video mô phỏng toán học:
- **`diagonalization.py`** - Thuật toán chéo hóa ma trận
- **`decomposition.py`** - Các phương pháp phân rã ma trận (SVD, QR, v.v.)
- **`manim_scene.py`** - Các scene Manim để trực quan hóa quá trình toán học
- **`manim_report.md`** - Báo cáo về video Manim
- **`guide_run_manim_scene1.md`** - Hướng dẫn chạy các scene Manim
- **`tasks.md`** - Các nhiệm vụ cần hoàn thành

### 📊 Phần 3: Phân tích hiệu năng và ứng dụng (`part3/`)

Phân tích, so sánh hiệu năng và các ứng dụng thực tế:
- **`solvers.py`** - Các solver và phương pháp giải khác nhau
- **`benchmark.py`** - Chương trình benchmark so sánh hiệu năng
- **`analysis.ipynb`** - Notebook phân tích kết quả và vẽ biểu đồ
- **`report_p3.md`** - Báo cáo chi tiết Phần 3

### 📄 Các file tài liệu chính

- **`requirements.txt`** - Danh sách thư viện phụ thuộc
- **`README.md`** - File hướng dẫn này
- **`report/`** - Thư mục chứa báo cáo cuối cùng, dữ liệu, và hình ảnh

---

## Yêu cầu môi trường

Trước khi bắt đầu, hãy đảm bảo hệ thống của bạn có:

### ✅ Python

- **Phiên bản tối thiểu:** Python 3.10
- **Cách kiểm tra:** Mở terminal/cmd và chạy:
  ```bash
  python --version
  ```
  hoặc
  ```bash
  python3 --version
  ```

### ✅ pip (Package Manager)

- `pip` thường được cài đặt cùng với Python
- **Cách kiểm tra:**
  ```bash
  pip --version
  ```

### ✅ Git (tùy chọn, nhưng được khuyến nghị)

- Để clone hoặc quản lý phiên bản: [Tải Git](https://git-scm.com/)

---

## Hướng dẫn cài đặt

### Bước 1: Clone hoặc tải dự án

Nếu dự án được lưu trên Git:
```bash
git clone <đường_dẫn_repository>
cd PRJ1_TUDTK_N1
```

Hoặc nếu tải trực tiếp, hãy giải nén và vào thư mục dự án:
```bash
cd PRJ1_TUDTK_N1
```

### Bước 2: Tạo môi trường ảo (Virtual Environment) - được khuyến nghị

Tạo môi trường ảo để tránh xung đột phiên bản thư viện:

**Trên Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Trên macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện phụ thuộc

Cài đặt tất cả các thư viện được liệt kê trong `requirements.txt`:

```bash
pip install -r requirements.txt
```

Cách này sẽ tự động cài đặt:
- `numpy==2.4.4`
- `manim==0.20.1`
- `matplotlib>=3.8.0`
- Và các thư viện hỗ trợ khác

### Bước 4: Xác minh cài đặt

Kiểm tra xem các thư viện chính đã được cài đặt thành công:

```bash
python -c "import numpy; import manim; print('✓ Cài đặt thành công!')"
```

---

## Hướng dẫn chạy dự án

### 🚀 Chạy Phần 1: Các phép toán cơ bản

**Chạy demo trực tiếp:**
```bash
cd part1
python gaussian.py
```

**Xem demo trong Jupyter Notebook:**
```bash
cd part1
jupyter notebook part1_demo.ipynb
```

Bạn có thể chạy từng cell để thực hành các phép khử Gauss, tính định thức, tìm ma trận nghịch đảo, v.v.

---

### 🎬 Chạy Phần 2: Video Manim

**Xem hướng dẫn chi tiết:**
Trước tiên, hãy đọc file hướng dẫn:
```bash
cd part2
cat guide_run_manim_scene1.md
```

**Render video từ scene Manim:**

Render với chất lượng cao (HD):
```bash
cd part2
manim -pql manim_scene.py <TenClass>
```

Render với chất lượng thấp để test nhanh:
```bash
manim -pql manim_scene.py <TenClass>
```

**Ví dụ cụ thể:**
```bash
manim -pql manim_scene.py GaussianEliminationScene
```

Các tùy chọn phổ biến:
- `-p` : Chạy và xem video sau khi render
- `-q` : Chất lượng (l=low, m=medium, h=high, p=production)
- `-n <số>` : Chỉ render frame từ số thứ n

---

### 📊 Chạy Phần 3: Benchmark và Phân tích

**Chạy benchmark so sánh hiệu năng:**
```bash
cd part3
python benchmark.py
```

Chương trình sẽ tạo ra các dữ liệu so sánh về thời gian thực thi các thuật toán khác nhau.

**Xem phân tích và biểu đồ:**
```bash
cd part3
jupyter notebook analysis.ipynb
```

File Notebook này sẽ đọc dữ liệu từ benchmark, phân tích và vẽ biểu đồ so sánh.

---

## 📚 Cấu trúc thư mục chi tiết

```
PRJ1_TUDTK_N1/
├── part1/                      # Phần 1: Phép khử Gauss
│   ├── gaussian.py
│   ├── determinant.py
│   ├── inverse.py
│   ├── rank_basis.py
│   ├── matrix_utils.py
│   ├── part1_demo.ipynb
│   └── Nhat_report.md
├── part2/                      # Phần 2: Chéo hóa & Manim
│   ├── diagonalization.py
│   ├── decomposition.py
│   ├── manim_scene.py
│   ├── manim_report.md
│   ├── guide_run_manim_scene1.md
│   └── tasks.md
├── part3/                      # Phần 3: Benchmark & Phân tích
│   ├── solvers.py
│   ├── benchmark.py
│   ├── analysis.ipynb
│   └── report_p3.md
├── report/                     # Thư mục báo cáo cuối cùng
│   ├── report.tex
│   ├── data.txt
│   ├── data2.txt
│   └── images/
├── requirements.txt            # Danh sách thư viện
├── README.md                   # File này
├── debai.md                    # Đề bài dự án
├── manim.md                    # Tài liệu về Manim
└── reportP2_Truong.md         # Báo cáo bổ sung
```

---

## 🔧 Khắc phục sự cố thường gặp

### 1. Lỗi "ModuleNotFoundError" khi import numpy hoặc manim

**Giải pháp:**
- Đảm bảo bạn đã kích hoạt virtual environment
- Chạy lại `pip install -r requirements.txt`

### 2. Manim render chậm hoặc lỗi

**Giải pháp:**
- Sử dụng chất lượng thấp để test: `manim -ql manim_scene.py <TenClass>`
- Đảm bảo đã cài đặt ffmpeg (Manim yêu cầu)
- Xem chi tiết trong `part2/guide_run_manim_scene1.md`

### 3. Jupyter Notebook không nhận ra các module

**Giải pháp:**
- Cài đặt jupyter trong virtual environment:
  ```bash
  pip install jupyter
  ```
- Chạy notebook từ trong thư mục dự án

---

## 📖 Tài liệu tham khảo

- **NumPy Documentation:** https://numpy.org/
- **Manim Documentation:** https://docs.manim.community/
- **SciPy Documentation:** https://docs.scipy.org/
- **SymPy Documentation:** https://docs.sympy.org/

---

## 📝 Ghi chú

- Tất cả code được viết bằng Python 3.10+
- Dự án tuân theo quy chuẩn PEP 8 về style code
- Các Notebook sử dụng Jupyter Notebook hoặc JupyterLab
- Báo cáo cuối cùng được lưu trong thư mục `report/`

---

## 📞 Liên hệ & Hỗ trợ

Nếu gặp bất kỳ vấn đề nào trong quá trình thực hiện dự án, vui lòng liên hệ với nhóm hoặc giáo viên hướng dẫn.

---

**Tài liệu được cập nhật lần cuối:** April 2026  
**Phiên bản:** 1.0
