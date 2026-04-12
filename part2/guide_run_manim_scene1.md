# Huong dan chay manim_scene1.py chi tiet (Windows)

Tai lieu nay huong dan day du de render video tu file `part2/manim_scene1.py`.

## 1) Chuan bi moi truong

1. Mo terminal tai thu muc goc project:
```powershell
cd "c:\TranNhatTruong_2026\Toan Ung Dung\PRJ1\main"
```

2. Kich hoat virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

3. Neu chua co Manim trong venv, cai dat:
```powershell
python -m pip install --upgrade pip
python -m pip install manim
```

## 2) Cai dependency he thong cho MathTex va video

`MathTex` can bo cong cu LaTeX he thong, va Manim can `ffmpeg` de xuat mp4.

1. Cai MiKTeX:
```powershell
winget install --id MiKTeX.MiKTeX --source winget --accept-package-agreements --accept-source-agreements --silent
```

2. Cai FFmpeg:
```powershell
winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent
```

3. Dong terminal/VS Code va mo lai de cap nhat PATH.

## 3) Kiem tra nhanh dependency

Chay cac lenh sau:
```powershell
where latex
where dvisvgm
where ffmpeg
```

Neu ca 3 lenh tra ve duong dan thi da san sang render.

## 4) Chay render video (cach de xuat)

# Huong dan chay `manim_scene.py` (Windows)

Tai lieu nay huong dan render tung scene rieng va render video tong hop tu file `part2/manim_scene.py`.

## 1) Chuan bi moi truong

Mo terminal tai thu muc goc project:

```powershell
cd "c:\TranNhatTruong_2026\Toan Ung Dung\PRJ1\main"
```

Kich hoat virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Neu chua co dependency:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2) Kiem tra cong cu he thong

Manim can LaTeX va FFmpeg de xuat video MP4.

```powershell
where latex
where dvisvgm
where ffmpeg
```

Neu chua co, cai dat nhanh bang winget:

```powershell
winget install --id MiKTeX.MiKTeX --source winget --accept-package-agreements --accept-source-agreements --silent
winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent
```

Dong va mo lai terminal/VS Code sau khi cai de cap nhat PATH.

## 3) Chay tung scene

File hien tai co 4 scene chinh:

```powershell
python part2/manim_scene.py --scene Scene0_Overview --quality m
python part2/manim_scene.py --scene Scene1_Cholesky_IntroAndSPD --quality m
python part2/manim_scene.py --scene Scene2_Cholesky_Calculation --quality m
python part2/manim_scene.py --scene Scene3_Diagonalization --quality m
```

Co the doi chat luong:

```powershell
python part2/manim_scene.py --scene Scene1_Cholesky_IntroAndSPD --quality l
python part2/manim_scene.py --scene Scene1_Cholesky_IntroAndSPD --quality h
```

## 4) Chay video hoan chinh

Lenh sau se render tat ca scene va tu dong ghep thanh `Full_Presentation.mp4`:

```powershell
python part2/manim_scene.py --quality m
```

Neu muon test nhanh truoc khi xuat chat luong cao, dung `--quality l`.

## 5) Vi tri video dau ra

Video rieng cua tung scene nam trong thu muc Manim mac dinh:

```text
part2\media\videos\manim_scene\<profile>\<SceneName>.mp4
```

Video ghep hoan chinh nam tai:

```text
part2\media\videos\manim_scene\<profile>\Full_Presentation.mp4
```

Voi `--quality m`, profile thuong la `720p30`.

## 6) Lenh chay nhanh

```powershell
cd "c:\TranNhatTruong_2026\Toan Ung Dung\PRJ1\main"
.\.venv\Scripts\Activate.ps1
python part2/manim_scene.py --quality m
```