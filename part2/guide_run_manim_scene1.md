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

File da co runner, ban chay truc tiep:
```powershell
python part2/manim_scene1.py --quality m
```

Cac muc chat luong:
- `--quality l`: nhanh, 480p15
- `--quality m`: can bang toc do/chat luong, 720p30
- `--quality h`: chat luong cao, 1080p60
- `--quality k`: 4K

Co the bo cache khi can:
```powershell
python part2/manim_scene1.py --quality m --disable-caching
```

## 5) Duong dan video dau ra

Video duoc tao tai:
- `part2/media/videos/manim_scene1/<profile>/CholeskyDecomposition.mp4`

Vi du profile `m`:
- `part2/media/videos/manim_scene1/720p30/CholeskyDecomposition.mp4`

## 6) Truong hop PATH chua cap nhat (fix nhanh trong 1 terminal)

Neu vua cai xong ma `where latex`/`where ffmpeg` van khong thay, co the tam them PATH:

```powershell
$env:Path = "C:\Users\ADMIN\AppData\Local\Programs\MiKTeX\miktex\bin\x64;C:\Users\ADMIN\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin;" + $env:Path
python part2/manim_scene1.py --quality l
```

## 7) Loi thuong gap va cach xu ly

1. Loi `FileNotFoundError [WinError 2]` tai `MathTex`:
- Nguyen nhan: thieu `latex`/`dvisvgm` trong PATH.
- Cach sua: cai MiKTeX, mo lai terminal, kiem tra `where latex` va `where dvisvgm`.

2. Loi khong tao duoc mp4:
- Nguyen nhan: thieu `ffmpeg`.
- Cach sua: cai FFmpeg, mo lai terminal, kiem tra `where ffmpeg`.

3. Render cham:
- Giam chat luong xuong `--quality l` de test logic, sau do render lai `m` hoac `h`.

## 8) Lenh full nhanh de chay lai tu dau

```powershell
cd "c:\TranNhatTruong_2026\Toan Ung Dung\PRJ1\main"
.\.venv\Scripts\Activate.ps1
python part2/manim_scene1.py --quality m
```


# Run with Phuc
## Run each scene
* python manim_scene.py --scene Scene1Introduction
* python manim_scene.py --scene Scene2CholeskyProcess
* python manim_scene.py --scene Scene3DiagonalizationProcess
## Run scence with high quality
* python manim_scene.py --scene Scene2CholeskyProcess --quality m
# Run all scence
* python manim_scene.py --quality m