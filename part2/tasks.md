# Ke hoach trien khai Part 2 (Task doc lap)

## Muc tieu
Hoan thanh manim_scene.py va demo_video.mp4 theo dung requirement.md, dam bao cac task doc lap de giam anh huong cheo khi sua.

## Nguyen tac chia task doc lap
- Moi task co dau vao/ra ro rang.
- Moi task co Definition of Done (DoD) rieng.
- Scene nao xong scene do co the render rieng.
- Khong doi du lieu chuan sau khi da khoa o pha dau.

## [x] Pha A - Khoa du lieu chuan va checklist rubric
### [x] Task A1 - Chot bo du lieu demo
- Dau vao: requirement.md, task2.md, decomposition.py, diagonalization.py.
- Dau ra: bo du lieu A, L, eigenvalues, eigenvectors, P, D, P_inv su dung nhat quan.
- DoD: bo du lieu duoc khai bao mot cho duy nhat trong manim_scene.py.

### [x] Task A2 - Chot quy tac hien thi so
- Dau vao: bo du lieu A1.
- Dau ra: quy tac lam tron khi hien thi (khong anh huong tinh toan noi bo).
- DoD: co helper format so duoc dung nhat quan trong scene.

### [x] Task A3 - Lap checklist nghiem thu theo rubric
- Dau vao: requirement.md + task2.md.
- Dau ra: checklist gom scene, cong thuc, verification, video format, thoi luong.
- DoD: checklist duoc dat o cuoi file tasks.md de doi chieu khi chot video.

## [x] Pha B - Scene 1 (Intro) doc lap
### [x] Task B1 - Dung khung Scene 1
- Noi dung: hien thi ma tran A va phat bieu bai toan.
- DoD: co class Scene1Introduction render doc lap.

### [x] Task B2 - Hien thi cong thuc muc tieu
- Noi dung: A = LL^T va A = PDP^{-1}.
- DoD: cong thuc hien thi ro, timing doc duoc.

### [x] Task B3 - Render thu Scene 1
- Lenh tham chieu: manim -pql manim_scene.py Scene1Introduction
- DoD: scene chay khong loi.

## [x] Pha C - Scene 2A (SPD proof) doc lap
### [x] Task C1 - Truc quan tinh doi xung
- Noi dung: highlight cap A_ij va A_ji.
- DoD: nguoi xem nhin thay duoc A = A^T.

### [x] Task C2 - Truc quan tinh xac dinh duong
- Noi dung: tinh eigenvalues bang numpy.linalg.eig va hien thi > 0.
- DoD: ket luan SPD xuat hien ro rang.

### [x] Task C3 - Render thu Scene 2A
- DoD: phan SPD proof chay doc lap, khong can phan thay so L.

## [x] Pha D - Scene 2B (Cholesky step-by-step) doc lap
### [x] Task D1 - Tao data step Cholesky
- Noi dung: luu tung buoc tinh l11, l21, l31, l22, l32, l33.
- DoD: du lieu buoc tinh tach rieng khoi animation.

### [x] Task D2 - Dung animation thay so va dien L
- Noi dung: hien thi cong thuc tong quat + thay so tung buoc.
- DoD: ma tran L duoc dien day du va theo thu tu dung.

### [x] Task D3 - Verify LL^T = A
- Noi dung: dung numpy.linalg.cholesky de doi chieu va hien thi ket qua.
- DoD: ket luan Cholesky hoan tat hien thi ro.

### [x] Task D4 - Render thu Scene 2 day du
- Lenh tham chieu: manim -pql manim_scene.py Scene2CholeskyProcess
- DoD: scene chay khong loi, nhin ro cac buoc.

## [ ] Pha E - Scene 3A (Eigen data) doc lap
### [ ] Task E1 - Hien thi gia tri rieng
- Noi dung: tinh bang numpy.linalg.eig, hien thi danh sach lambda.
- DoD: danh sach gia tri rieng ro, de doc.

### [ ] Task E2 - Hien thi vector rieng
- Noi dung: hien thi tung cot cua P va gan nhan v1, v2, v3.
- DoD: nguoi xem thay duoc lien he giua vector rieng va P.

### [ ] Task E3 - Render thu Scene 3A
- DoD: phan hien thi eigen data chay doc lap.

## [ ] Pha F - Scene 3B (Lap rap diagonalization) doc lap
### [ ] Task F1 - Dung D va P
- Noi dung: tao D tu eigenvalues, P tu eigenvectors.
- DoD: D va P hien thi dung cau truc.

### [ ] Task F2 - Dung bieu thuc A = P D P^{-1}
- Noi dung: hien thi cong thuc va ket qua phuc hoi A.
- DoD: ket qua phuc hoi khop A trong dung sai cho phep.

### [ ] Task F3 - Render thu Scene 3 day du
- Lenh tham chieu: manim -pql manim_scene.py Scene3DiagonalizationProcess
- DoD: scene chay khong loi.

## [ ] Pha G - Tich hop an toan (han che sua cheo)
### [ ] Task G1 - Tich hop Scene 1 -> 2 -> 3
- Noi dung: chi noi scene, khong sua logic noi bo scene.
- DoD: render duoc chuoi scene day du.

### [ ] Task G2 - Chuan hoa style dung chung
- Noi dung: gom mau, font size, spacing vao hang so.
- DoD: thong nhat giao dien, khong sua logic tinh toan.

### [ ] Task G3 - Render tong hop low quality
- Lenh tham chieu: manim -pql manim_scene.py
- DoD: video tong khong dut mach.

## [ ] Pha H - Nghiem thu va render final
### [ ] Task H1 - Render final
- Lenh bat buoc: manim -pqm manim_scene.py
- DoD: xuat MP4 720p.

### [ ] Task H2 - Kiem tra metadata va thoi luong
- DoD: thoi luong >= 2 phut va <= 30 phut.

### [ ] Task H3 - Chot checklist cuoi
- DoD: dat tat ca tieu chi rubric.

## Song song va phu thuoc
- Co the song song: B, C, E (sau A).
- Co the song song: D va F (sau A).
- G phu thuoc: B + D + F.
- H phu thuoc: G.

## Checklist nghiem thu (rubric gate)
- [x] Co du 3 scene dung noi dung bat buoc.
- [x] Co hien thi ly thuyet va cong thuc chinh xac.
- [x] Co su dung numpy.linalg.cholesky trong source de verification.
- [x] Co su dung numpy.linalg.eig trong source de verification/tinh toan.
- [x] Co trinh bay SPD proof (symmetric + positive eigenvalues).
- [x] Co thay so Cholesky tung buoc va dien ma tran L.
- [ ] Co trinh bay eigenvalues, eigenvectors, D, P va P^{-1}.
- [ ] Co lap rap va verify A = P D P^{-1}.
- [ ] Xuat dung MP4 720p bang co -pqm.
- [ ] Thoi luong video nam trong [2, 30] phut.
