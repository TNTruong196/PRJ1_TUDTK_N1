# """Manim visualization for Cholesky decomposition and diagonalization.

# This file follows the project constraints:
# - Core matrix computations are implemented with pure Python list-of-lists.
# - No use of numpy.array for algorithm implementation.
# - Uses Manim Matrix and MathTex for visual rendering.
# """

# from __future__ import annotations

# import argparse
# import math
# import os
# from pathlib import Path
# import shutil
# import subprocess
# import sys

# from manim import (
#     BLUE,
#     GREEN,
#     ORANGE,
#     PURPLE,
#     RED,
#     WHITE,
#     YELLOW,
#     DOWN,
#     LEFT,
#     RIGHT,
#     UP,
#     UL,
#     UR,
#     PI,
#     BarChart,
#     FadeIn,
#     FadeOut,
#     MathTex,
#     Matrix,
#     Scene,
#     SurroundingRectangle,
#     Text,
#     Transform,
#     VGroup,
#     Write,
# )


# class CholeskyDecomposition(Scene):
#     """Full storyboard scene with 5 parts from manim.md."""

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.A = [
#             [4.0, 12.0, -16.0],
#             [12.0, 37.0, -43.0],
#             [-16.0, -43.0, 98.0],
#         ]

#         # Precomputed results for stable animation rendering.
#         self.L = self.cholesky_decompose(self.A)
#         self.eigenvalues = [123.4772, 15.5040, 0.0188]
#         self.eigenvectors = [
#             [0.1630, 0.4573, -0.8742],
#             [-0.2127, -0.8489, -0.4838],
#             [0.9635, -0.2648, 0.0411],
#         ]

#     def construct(self):
#         self.part1_intro()
#         self.clear()
#         self.part2_spd()
#         self.clear()
#         self.part3_cholesky_steps()
#         self.clear()
#         self.part4_cost()
#         self.clear()
#         self.part5_diagonalization()

#     # ============================
#     # Pure list-based math helpers
#     # ============================
#     def transpose(self, matrix: list[list[float]]) -> list[list[float]]:
#         return [list(row) for row in zip(*matrix)]

#     def matmul(self, a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
#         rows = len(a)
#         cols = len(b[0])
#         shared = len(b)
#         result = [[0.0 for _ in range(cols)] for _ in range(rows)]
#         for i in range(rows):
#             for k in range(shared):
#                 av = a[i][k]
#                 if av == 0.0:
#                     continue
#                 for j in range(cols):
#                     result[i][j] += av * b[k][j]
#         return result

#     def det_2x2(self, matrix: list[list[float]]) -> float:
#         return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

#     def det_3x3(self, matrix: list[list[float]]) -> float:
#         a11, a12, a13 = matrix[0]
#         a21, a22, a23 = matrix[1]
#         a31, a32, a33 = matrix[2]
#         return (
#             a11 * (a22 * a33 - a23 * a32)
#             - a12 * (a21 * a33 - a23 * a31)
#             + a13 * (a21 * a32 - a22 * a31)
#         )

#     def cholesky_decompose(self, matrix: list[list[float]]) -> list[list[float]]:
#         n = len(matrix)
#         l = [[0.0 for _ in range(n)] for _ in range(n)]
#         for i in range(n):
#             for j in range(i + 1):
#                 if i == j:
#                     s = sum(l[i][k] * l[i][k] for k in range(j))
#                     l[i][j] = math.sqrt(matrix[i][i] - s)
#                 else:
#                     s = sum(l[i][k] * l[j][k] for k in range(j))
#                     l[i][j] = (matrix[i][j] - s) / l[j][j]
#         return l

#     def fmt(self, value: float) -> str:
#         if abs(value - round(value)) < 1e-9:
#             return str(int(round(value)))
#         return f"{value:.4f}"

#     def to_manim_str_matrix(self, matrix: list[list[float]]) -> list[list[str]]:
#         return [[self.fmt(x) for x in row] for row in matrix]

#     # ====================================================
#     # Required helper: highlight a specific matrix cell
#     # ====================================================
#     def highlight_cell(self, matrix: Matrix, row: int, col: int, color=YELLOW):
#         entries = matrix.get_entries()
#         n = int(round(math.sqrt(len(entries))))
#         idx = (row - 1) * n + (col - 1)
#         return SurroundingRectangle(entries[idx], color=color, buff=0.08)

#     # =============
#     # Part 1: Intro
#     # =============
#     def part1_intro(self):
#         title = Text("Phan ra Cholesky (Cholesky Decomposition)", color=YELLOW).scale(0.8)
#         title.to_edge(UP)

#         formula = MathTex(r"A = L L^T", color=GREEN).scale(1.1)
#         formula.next_to(title, DOWN, buff=0.6)

#         l_note = MathTex(
#             r"L\;\text{la ma tran tam giac duoi,}\;L_{ii}>0",
#             color=WHITE,
#         ).scale(0.75)
#         l_note.next_to(formula, DOWN, buff=0.4)

#         triangle_shape = Matrix(
#             [["*", "0", "0"], ["*", "*", "0"], ["*", "*", "*"]],
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.75)
#         triangle_shape.next_to(l_note, DOWN, buff=0.4)

#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.85)
#         matrix_a.to_edge(DOWN, buff=0.8)

#         a_label = MathTex(r"A=", color=ORANGE).scale(0.9)
#         a_label.next_to(matrix_a, LEFT, buff=0.2)

#         self.play(Write(title))
#         self.play(Write(formula))
#         self.play(FadeIn(l_note))
#         self.play(FadeIn(triangle_shape))
#         self.play(FadeIn(a_label), FadeIn(matrix_a))
#         self.wait(1)

#     # ==========================
#     # Part 2: Verify SPD of A
#     # ==========================
#     def part2_spd(self):
#         title = Text("Phan 2: Kiem tra A la ma tran SPD", color=YELLOW).scale(0.8)
#         title.to_edge(UP)

#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.85)
#         matrix_a.shift(LEFT * 3.3 + UP * 0.2)
#         label_a = MathTex("A", color=ORANGE).next_to(matrix_a, UP)

#         self.play(Write(title))
#         self.play(FadeIn(matrix_a), FadeIn(label_a))

#         # Symmetry demonstration with rotating copy.
#         transpose_text = MathTex(r"A^T", color=BLUE).next_to(matrix_a, DOWN, buff=0.25)
#         matrix_at = matrix_a.copy().set_color(BLUE)
#         matrix_at.move_to(matrix_a.get_center() + RIGHT * 3.0)
#         self.play(FadeIn(matrix_at), FadeIn(transpose_text))
#         self.play(matrix_at.animate.rotate(PI, axis=UR).move_to(matrix_a.get_center()), run_time=1.6)

#         sym_result = MathTex(r"A = A^T", color=GREEN).next_to(matrix_a, DOWN, buff=0.9)
#         self.play(Write(sym_result))

#         # Sylvester criterion blocks via get_entries + rectangles.
#         entries = matrix_a.get_entries()
#         minor1 = SurroundingRectangle(entries[0], color=RED, buff=0.09)
#         minor2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE, buff=0.12)
#         minor3 = SurroundingRectangle(VGroup(*entries), color=YELLOW, buff=0.15)

#         d1 = self.A[0][0]
#         d2 = self.det_2x2([[self.A[0][0], self.A[0][1]], [self.A[1][0], self.A[1][1]]])
#         d3 = self.det_3x3(self.A)

#         sylvester_title = Text("Tieu chuan Sylvester", color=WHITE).scale(0.55)
#         sylvester_title.to_edge(RIGHT).shift(UP * 2.2)
#         delta1 = MathTex(r"\Delta_1 = 4 > 0", color=RED).scale(0.75)
#         delta2 = MathTex(r"\Delta_2 = 4 > 0", color=PURPLE).scale(0.75)
#         delta3 = MathTex(r"\Delta_3 = 36 > 0", color=YELLOW).scale(0.75)
#         sylv_group = VGroup(sylvester_title, delta1, delta2, delta3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
#         sylv_group.to_edge(RIGHT, buff=0.6).shift(UP * 0.4)

#         self.play(FadeIn(minor1), Write(delta1))
#         self.wait(0.3)
#         self.play(Transform(minor1, minor2), Write(delta2))
#         self.wait(0.3)
#         self.play(Transform(minor1, minor3), Write(delta3))
#         self.play(Write(sylvester_title))

#         summary = MathTex(
#             rf"\Delta_1={self.fmt(d1)},\;\Delta_2={self.fmt(d2)},\;\Delta_3={self.fmt(d3)}\Rightarrow A\;\text{{la SPD}}",
#             color=GREEN,
#         ).scale(0.7)
#         summary.to_edge(DOWN, buff=0.5)
#         self.play(Write(summary))
#         self.wait(1)

#     # ==================================
#     # Part 3: Step-by-step build of L
#     # ==================================
#     def part3_cholesky_steps(self):
#         title = Text("Phan 3: Tinh tung phan tu cua L", color=YELLOW).scale(0.8)
#         title.to_edge(UP)

#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.65)
#         matrix_a.to_corner(UL).shift(DOWN * 0.4)
#         label_a = MathTex("A", color=ORANGE).scale(0.7).next_to(matrix_a, UP, buff=0.1)

#         recurrence = VGroup(
#             MathTex(r"L_{jj}=\sqrt{A_{jj}-\sum_{k=1}^{j-1}L_{jk}^2}", color=WHITE).scale(0.7),
#             MathTex(r"L_{ij}=\frac{A_{ij}-\sum_{k=1}^{j-1}L_{ik}L_{jk}}{L_{jj}},\;i>j", color=WHITE).scale(0.7),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
#         recurrence.to_corner(UR).shift(DOWN * 0.5)

#         l_template = [
#             ["?", "0", "0"],
#             ["?", "?", "0"],
#             ["?", "?", "?"],
#         ]
#         matrix_l = Matrix(l_template, element_to_mobject=lambda x: MathTex(x)).scale(0.95)
#         matrix_l.move_to(DOWN * 0.8)
#         label_l = MathTex("L", color=GREEN).next_to(matrix_l, UP)

#         self.play(Write(title))
#         self.play(FadeIn(matrix_a), FadeIn(label_a))
#         self.play(Write(recurrence))
#         self.play(FadeIn(matrix_l), FadeIn(label_l))

#         steps = [
#             {
#                 "formula": r"L_{11}=\sqrt{A_{11}}=\sqrt{4}=2",
#                 "value": "2",
#                 "target": (1, 1),
#                 "highlights": [(1, 1)],
#             },
#             {
#                 "formula": r"L_{21}=\frac{A_{21}}{L_{11}}=\frac{12}{2}=6",
#                 "value": "6",
#                 "target": (2, 1),
#                 "highlights": [(2, 1), (1, 1)],
#             },
#             {
#                 "formula": r"L_{31}=\frac{A_{31}}{L_{11}}=\frac{-16}{2}=-8",
#                 "value": "-8",
#                 "target": (3, 1),
#                 "highlights": [(3, 1), (1, 1)],
#             },
#             {
#                 "formula": r"L_{22}=\sqrt{A_{22}-L_{21}^2}=\sqrt{37-6^2}=1",
#                 "value": "1",
#                 "target": (2, 2),
#                 "highlights": [(2, 2), (2, 1)],
#             },
#             {
#                 "formula": r"L_{32}=\frac{A_{32}-L_{31}L_{21}}{L_{22}}=\frac{-43-(-8)(6)}{1}=5",
#                 "value": "5",
#                 "target": (3, 2),
#                 "highlights": [(3, 2), (3, 1), (2, 1), (2, 2)],
#             },
#             {
#                 "formula": r"L_{33}=\sqrt{A_{33}-(L_{31}^2+L_{32}^2)}=\sqrt{98-(64+25)}=3",
#                 "value": "3",
#                 "target": (3, 3),
#                 "highlights": [(3, 3), (3, 1), (3, 2)],
#             },
#         ]

#         formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.76)
#         formula_box.to_edge(DOWN, buff=0.3)
#         self.play(Write(formula_box))

#         for step in steps:
#             new_formula = MathTex(step["formula"], color=YELLOW).scale(0.76)
#             new_formula.move_to(formula_box)
#             self.play(Transform(formula_box, new_formula))

#             highlight_boxes = []
#             for row, col in step["highlights"]:
#                 box = self.highlight_cell(matrix_a, row, col, color=ORANGE)
#                 highlight_boxes.append(box)
#                 self.play(FadeIn(box), run_time=0.18)

#             row, col = step["target"]
#             n = 3
#             target_idx = (row - 1) * n + (col - 1)
#             l_entries = matrix_l.get_entries()
#             target_entry = l_entries[target_idx]

#             flying = MathTex(step["value"], color=GREEN).scale(0.9)
#             flying.next_to(formula_box, UP, buff=0.2)

#             self.play(FadeIn(flying, shift=UP * 0.1))
#             self.play(flying.animate.move_to(target_entry.get_center()), run_time=0.7)

#             filled = MathTex(step["value"], color=WHITE).move_to(target_entry.get_center())
#             self.play(Transform(target_entry, filled), FadeOut(flying), run_time=0.3)

#             for box in highlight_boxes:
#                 self.play(FadeOut(box), run_time=0.15)

#         # Final acceptance: show L, L^T and product statement.
#         matrix_lt = Matrix(
#             self.to_manim_str_matrix(self.transpose(self.L)),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.7)
#         matrix_lt.next_to(matrix_l, RIGHT, buff=1.2)
#         label_lt = MathTex("L^T", color=GREEN).scale(0.75).next_to(matrix_lt, UP, buff=0.15)

#         product_text = MathTex(r"L\times L^T = A", color=GREEN).scale(0.9)
#         product_text.next_to(matrix_l, DOWN, buff=0.7)

#         computed = self.matmul(self.L, self.transpose(self.L))
#         status = "PASS" if all(
#             abs(computed[i][j] - self.A[i][j]) < 1e-8
#             for i in range(3)
#             for j in range(3)
#         ) else "FAIL"
#         verify_text = Text(f"Kiem tra nhan ma tran: {status}", color=GREEN if status == "PASS" else RED).scale(0.52)
#         verify_text.next_to(product_text, DOWN, buff=0.2)

#         self.play(FadeIn(matrix_lt), FadeIn(label_lt))
#         self.play(Write(product_text))
#         self.play(Write(verify_text))
#         self.wait(1.2)

#     # ===========================
#     # Part 4: Cost comparison
#     # ===========================
#     def part4_cost(self):
#         title = Text("Phan 4: Chi phi tinh toan", color=YELLOW).scale(0.8)
#         title.to_edge(UP)

#         lu_bar = BarChart(
#             values=[1.0],
#             bar_names=["LU"],
#             y_range=[0, 1.2, 0.2],
#             y_length=4,
#             x_length=3,
#             bar_colors=[RED],
#         ).scale(0.7)
#         lu_bar.shift(LEFT * 2.8 + DOWN * 0.4)

#         chol_bar = BarChart(
#             values=[1.0],
#             bar_names=["Cholesky"],
#             y_range=[0, 1.2, 0.2],
#             y_length=4,
#             x_length=3,
#             bar_colors=[GREEN],
#         ).scale(0.7)
#         chol_bar.shift(RIGHT * 2.8 + DOWN * 0.4)

#         note_before = MathTex(
#             r"\text{So sanh ban dau: LU}\approx\frac{2}{3}n^3,\;\text{Cholesky}\approx\frac{1}{3}n^3",
#             color=WHITE,
#         ).scale(0.67)
#         note_before.to_edge(DOWN, buff=0.8)

#         self.play(Write(title))
#         self.play(FadeIn(lu_bar), FadeIn(chol_bar))
#         self.play(Write(note_before))

#         chol_rect = chol_bar.bars[0]
#         self.play(chol_rect.animate.scale([1, 0.5, 1], about_edge=DOWN), run_time=1.4)

#         note_after = MathTex(
#             r"\text{Cholesky chi phi}\approx\frac{1}{2}\text{ so voi LU tren ma tran SPD}",
#             color=GREEN,
#         ).scale(0.75)
#         note_after.next_to(note_before, UP, buff=0.35)
#         self.play(Write(note_after))
#         self.wait(1)

#     # ============================================
#     # Part 5: Diagonalization A = P D P^{-1}
#     # ============================================
#     def part5_diagonalization(self):
#         title = Text("Phan 5: Cheo hoa ma tran", color=YELLOW).scale(0.8)
#         title.to_edge(UP)

#         char_eq = MathTex(r"\det(A-\lambda I)=0", color=WHITE).scale(0.95)
#         char_eq.next_to(title, DOWN, buff=0.45)

#         lambdas = VGroup(
#             MathTex(r"\lambda_1\approx 123.4772 > 0", color=GREEN).scale(0.75),
#             MathTex(r"\lambda_2\approx 15.5040 > 0", color=GREEN).scale(0.75),
#             MathTex(r"\lambda_3\approx 0.0188 > 0", color=GREEN).scale(0.75),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
#         lambdas.to_edge(LEFT, buff=0.6).shift(UP * 0.6)

#         self.play(Write(title))
#         self.play(Write(char_eq))
#         self.play(FadeIn(lambdas))

#         # Show eigenvectors and group them into matrix P.
#         v1 = MathTex(r"v_1=\begin{bmatrix}0.1630\\-0.2127\\0.9635\end{bmatrix}", color=BLUE).scale(0.72)
#         v2 = MathTex(r"v_2=\begin{bmatrix}0.4573\\-0.8489\\-0.2648\end{bmatrix}", color=BLUE).scale(0.72)
#         v3 = MathTex(r"v_3=\begin{bmatrix}-0.8742\\-0.4838\\0.0411\end{bmatrix}", color=BLUE).scale(0.72)
#         vec_group = VGroup(v1, v2, v3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
#         vec_group.to_edge(LEFT, buff=0.6).shift(DOWN * 1.6)

#         self.play(FadeIn(vec_group))

#         p_matrix = Matrix(
#             [
#                 ["0.1630", "0.4573", "-0.8742"],
#                 ["-0.2127", "-0.8489", "-0.4838"],
#                 ["0.9635", "-0.2648", "0.0411"],
#             ],
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.72)
#         p_matrix.to_edge(RIGHT, buff=1.0).shift(UP * 0.9)
#         p_label = MathTex("P", color=ORANGE).next_to(p_matrix, UP, buff=0.12)

#         self.play(vec_group.animate.to_edge(LEFT, buff=0.2).shift(RIGHT * 1.0))
#         self.play(FadeIn(p_matrix), FadeIn(p_label))

#         d_matrix = Matrix(
#             [
#                 ["123.4772", "0", "0"],
#                 ["0", "15.5040", "0"],
#                 ["0", "0", "0.0188"],
#             ],
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.72)
#         d_matrix.next_to(p_matrix, DOWN, buff=0.8)
#         d_label = MathTex("D", color=ORANGE).next_to(d_matrix, UP, buff=0.12)

#         pinv_tex = MathTex(r"P^{-1}\;\text{(hien thi ket qua truc tiep)}", color=WHITE).scale(0.7)
#         pinv_tex.next_to(d_matrix, DOWN, buff=0.35)

#         final_formula = MathTex(r"A = P D P^{-1}", color=GREEN).scale(1.0)
#         final_formula.to_edge(DOWN, buff=0.6)

#         self.play(FadeIn(d_matrix), FadeIn(d_label))
#         self.play(Write(pinv_tex))
#         self.play(Write(final_formula))
#         self.wait(1.5)


# DEFAULT_SCENE = "CholeskyDecomposition"


# def _run_cmd(cmd: list[str], cwd: Path) -> None:
#     completed = subprocess.run(cmd, cwd=str(cwd), check=False)
#     if completed.returncode != 0:
#         raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}")


# def _check_runtime_dependencies() -> None:
#     required = {
#         "latex": "MiKTeX/TexLive latex compiler",
#         "dvisvgm": "dvisvgm (usually bundled with MiKTeX)",
#         "ffmpeg": "FFmpeg video backend",
#     }

#     missing = []
#     for exe, description in required.items():
#         if shutil.which(exe) is None:
#             missing.append((exe, description))

#     if not missing:
#         return

#     lines = ["Missing runtime dependencies required by MathTex/Manim:"]
#     for exe, description in missing:
#         lines.append(f"- {exe}: {description}")
#     lines.extend(
#         [
#             "",
#             "Suggested fixes on Windows:",
#             "1) Install MiKTeX: winget install --id MiKTeX.MiKTeX --source winget --accept-package-agreements --accept-source-agreements --silent",
#             "2) Install FFmpeg: winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent",
#             "3) Close and reopen terminal/VS Code so PATH is refreshed.",
#             "4) Verify with: where latex, where dvisvgm, where ffmpeg",
#         ]
#     )
#     raise RuntimeError("\n".join(lines))


# def _find_latest_scene_video(project_dir: Path, scene_name: str) -> Path:
#     root = project_dir / "media" / "videos" / "manim_scene1"
#     matches = list(root.glob(f"*/{scene_name}.mp4"))
#     if not matches:
#         raise FileNotFoundError(f"Rendered scene file not found: {scene_name}")
#     matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
#     return matches[0]


# def main() -> int:
#     parser = argparse.ArgumentParser(
#         description="Run this file directly to render CholeskyDecomposition scene.",
#     )
#     parser.add_argument("--scene", default=DEFAULT_SCENE)
#     parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="m")
#     parser.add_argument("--disable-caching", action="store_true")
#     args = parser.parse_args()

#     project_dir = Path(__file__).resolve().parent
#     file_name = Path(__file__).name

#     _check_runtime_dependencies()

#     quality_flag = f"-q{args.quality}"
#     cmd = [
#         sys.executable,
#         "-m",
#         "manim",
#         quality_flag,
#         file_name,
#         args.scene,
#     ]
#     if args.disable_caching:
#         cmd.append("--disable_caching")

#     print(f"[render] scene={args.scene}, quality={args.quality}")
#     _run_cmd(cmd, cwd=project_dir)

#     video_path = _find_latest_scene_video(project_dir, args.scene)
#     print(f"[done] video: {video_path}")

#     # Auto-open video only when running in interactive terminal.
#     if os.name == "nt":
#         try:
#             os.startfile(video_path)  # type: ignore[attr-defined]
#         except OSError:
#             pass
#     return 0


# if __name__ == "__main__":
#     raise SystemExit(main())




























# """Manim visualization for Cholesky decomposition and diagonalization.

# This file follows the project constraints:
# - Core matrix computations are implemented with pure Python list-of-lists.
# - No use of numpy.array for algorithm implementation.
# - Uses Manim Matrix and MathTex for visual rendering.
# """

# from __future__ import annotations

# import argparse
# import math
# import os
# from pathlib import Path
# import shutil
# import subprocess
# import sys

# from manim import (
#     BLUE,
#     GREEN,
#     ORANGE,
#     PURPLE,
#     RED,
#     WHITE,
#     YELLOW,
#     DOWN,
#     LEFT,
#     RIGHT,
#     UP,
#     UL,
#     UR,
#     PI,
#     BarChart,
#     FadeIn,
#     FadeOut,
#     MathTex,
#     Matrix,
#     Scene,
#     SurroundingRectangle,
#     Text,
#     Transform,
#     VGroup,
#     Write,
# )


# class CholeskyDecomposition(Scene):
#     """Full storyboard scene with 5 parts from manim.md."""

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.A = [
#             [4.0, 12.0, -16.0],
#             [12.0, 37.0, -43.0],
#             [-16.0, -43.0, 98.0],
#         ]

#         # Precomputed results for stable animation rendering.
#         self.L = self.cholesky_decompose(self.A)
#         self.eigenvalues = [123.4772, 15.5040, 0.0188]
#         self.eigenvectors = [
#             [0.1630, 0.4573, -0.8742],
#             [-0.2127, -0.8489, -0.4838],
#             [0.9635, -0.2648, 0.0411],
#         ]

#     def construct(self):
#         self.part1_intro()
#         self.clear()
#         self.part2_spd()
#         self.clear()
#         self.part3_cholesky_steps()
#         self.clear()
#         self.part4_cost()
#         self.clear()
#         self.part5_diagonalization()

#     # ============================
#     # Pure list-based math helpers
#     # ============================
#     def transpose(self, matrix: list[list[float]]) -> list[list[float]]:
#         return [list(row) for row in zip(*matrix)]

#     def matmul(self, a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
#         rows = len(a)
#         cols = len(b[0])
#         shared = len(b)
#         result = [[0.0 for _ in range(cols)] for _ in range(rows)]
#         for i in range(rows):
#             for k in range(shared):
#                 av = a[i][k]
#                 if av == 0.0:
#                     continue
#                 for j in range(cols):
#                     result[i][j] += av * b[k][j]
#         return result

#     def det_2x2(self, matrix: list[list[float]]) -> float:
#         return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

#     def det_3x3(self, matrix: list[list[float]]) -> float:
#         a11, a12, a13 = matrix[0]
#         a21, a22, a23 = matrix[1]
#         a31, a32, a33 = matrix[2]
#         return (
#             a11 * (a22 * a33 - a23 * a32)
#             - a12 * (a21 * a33 - a23 * a31)
#             + a13 * (a21 * a32 - a22 * a31)
#         )

#     def cholesky_decompose(self, matrix: list[list[float]]) -> list[list[float]]:
#         n = len(matrix)
#         l = [[0.0 for _ in range(n)] for _ in range(n)]
#         for i in range(n):
#             for j in range(i + 1):
#                 if i == j:
#                     s = sum(l[i][k] * l[i][k] for k in range(j))
#                     l[i][j] = math.sqrt(matrix[i][i] - s)
#                 else:
#                     s = sum(l[i][k] * l[j][k] for k in range(j))
#                     l[i][j] = (matrix[i][j] - s) / l[j][j]
#         return l

#     def fmt(self, value: float) -> str:
#         if abs(value - round(value)) < 1e-9:
#             return str(int(round(value)))
#         return f"{value:.4f}"

#     def to_manim_str_matrix(self, matrix: list[list[float]]) -> list[list[str]]:
#         return [[self.fmt(x) for x in row] for row in matrix]

#     # ====================================================
#     # Required helper: highlight a specific matrix cell
#     # ====================================================
#     def highlight_cell(self, matrix: Matrix, row: int, col: int, color=YELLOW):
#         entries = matrix.get_entries()
#         n = int(round(math.sqrt(len(entries))))
#         idx = (row - 1) * n + (col - 1)
#         return SurroundingRectangle(entries[idx], color=color, buff=0.08)

#     # =============
#     # Part 1: Intro
#     # =============
#     def part1_intro(self):
#         title = Text("Phân rã Cholesky (Cholesky Decomposition)", color=YELLOW, font_size=36)
#         title.to_edge(UP)

#         formula = MathTex(r"A = L L^T", color=GREEN).scale(1.2)
#         formula.next_to(title, DOWN, buff=0.6)

#         # Sử dụng VGroup để kết hợp Text (Tiếng Việt) và MathTex tránh lỗi LaTeX
#         l_note = VGroup(
#             Text("L là ma trận tam giác dưới, ", font_size=28, color=WHITE),
#             MathTex(r"L_{ii}>0", color=WHITE)
#         ).arrange(RIGHT, buff=0.1)
#         l_note.next_to(formula, DOWN, buff=0.4)

#         triangle_shape = Matrix(
#             [["*", "0", "0"], ["*", "*", "0"], ["*", "*", "*"]],
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.75)
#         triangle_shape.next_to(l_note, DOWN, buff=0.4)

#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.85)
#         matrix_a.to_edge(DOWN, buff=0.6)

#         a_label = MathTex(r"A=", color=ORANGE).scale(0.9)
#         a_label.next_to(matrix_a, LEFT, buff=0.2)

#         self.play(Write(title))
#         self.play(Write(formula))
#         self.play(FadeIn(l_note))
#         self.play(FadeIn(triangle_shape))
#         self.play(FadeIn(a_label), FadeIn(matrix_a))
#         self.wait(1)

#     # ==========================
#     # Part 2: Verify SPD of A
#     # ==========================
#     def part2_spd(self):
#         title = Text("Phần 2: Kiểm tra A là ma trận SPD", color=YELLOW, font_size=36)
#         title.to_edge(UP)

#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.85)
#         matrix_a.move_to(LEFT * 3 + UP * 0.2)
#         label_a = MathTex("A", color=ORANGE).next_to(matrix_a, UP)

#         self.play(Write(title))
#         self.play(FadeIn(matrix_a), FadeIn(label_a))

#         # Symmetry demonstration with rotating copy.
#         transpose_text = MathTex(r"A^T", color=BLUE).next_to(matrix_a, DOWN, buff=0.25)
#         matrix_at = matrix_a.copy().set_color(BLUE)
#         matrix_at.move_to(RIGHT * 3 + UP * 0.2)
        
#         self.play(FadeIn(matrix_at), FadeIn(transpose_text))
#         # Rotate into A's position
#         self.play(matrix_at.animate.rotate(PI, axis=UR).move_to(matrix_a.get_center()), run_time=1.6)

#         sym_result = MathTex(r"A = A^T", color=GREEN).next_to(matrix_a, DOWN, buff=0.8)
#         self.play(Write(sym_result))

#         # Sylvester criterion blocks via get_entries + rectangles.
#         entries = matrix_a.get_entries()
#         minor1 = SurroundingRectangle(entries[0], color=RED, buff=0.09)
#         minor2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE, buff=0.12)
#         minor3 = SurroundingRectangle(VGroup(*entries), color=YELLOW, buff=0.15)

#         d1 = self.A[0][0]
#         d2 = self.det_2x2([[self.A[0][0], self.A[0][1]], [self.A[1][0], self.A[1][1]]])
#         d3 = self.det_3x3(self.A)

#         sylvester_title = Text("Tiêu chuẩn Sylvester", color=WHITE, font_size=28)
#         delta1 = MathTex(r"\Delta_1 = 4 > 0", color=RED).scale(0.8)
#         delta2 = MathTex(r"\Delta_2 = 4 > 0", color=PURPLE).scale(0.8)
#         delta3 = MathTex(r"\Delta_3 = 36 > 0", color=YELLOW).scale(0.8)
        
#         sylv_group = VGroup(sylvester_title, delta1, delta2, delta3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
#         sylv_group.move_to(RIGHT * 3 + UP * 0.5)

#         self.play(FadeIn(minor1), Write(delta1))
#         self.wait(0.3)
#         self.play(Transform(minor1, minor2), Write(delta2))
#         self.wait(0.3)
#         self.play(Transform(minor1, minor3), Write(delta3))
#         self.play(Write(sylvester_title))

#         # Khắc phục lỗi tiếng Việt cho phần summary
#         summary = VGroup(
#             MathTex(rf"\Delta_1={self.fmt(d1)},\;\Delta_2={self.fmt(d2)},\;\Delta_3={self.fmt(d3)}\Rightarrow A", color=GREEN).scale(0.8),
#             Text(" là ma trận SPD", color=GREEN, font_size=28)
#         ).arrange(RIGHT, buff=0.15)
#         summary.to_edge(DOWN, buff=0.5)
        
#         self.play(Write(summary))
#         self.wait(1)

#     # ==================================
#     # Part 3: Step-by-step build of L
#     # ==================================
#     def part3_cholesky_steps(self):
#         title = Text("Phần 3: Tính từng phần tử của L", color=YELLOW, font_size=36)
#         title.to_edge(UP)

#         # Scale nhỏ lại để lấy không gian
#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.6)
#         matrix_a.to_corner(UL).shift(DOWN * 0.4 + RIGHT * 0.5)
#         label_a = MathTex("A", color=ORANGE).scale(0.7).next_to(matrix_a, UP, buff=0.1)

#         recurrence = VGroup(
#             MathTex(r"L_{jj}=\sqrt{A_{jj}-\sum_{k=1}^{j-1}L_{jk}^2}", color=WHITE).scale(0.7),
#             MathTex(r"L_{ij}=\frac{A_{ij}-\sum_{k=1}^{j-1}L_{ik}L_{jk}}{L_{jj}},\;i>j", color=WHITE).scale(0.7),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
#         recurrence.to_corner(UR).shift(DOWN * 0.5 + LEFT * 0.5)

#         l_template = [
#             ["?", "0", "0"],
#             ["?", "?", "0"],
#             ["?", "?", "?"],
#         ]
#         matrix_l = Matrix(l_template, element_to_mobject=lambda x: MathTex(x)).scale(0.85)
#         # Dời ma trận L sang trái một chút để chừa chỗ cho công thức
#         matrix_l.move_to(LEFT * 2.5 + DOWN * 0.8)
#         label_l = MathTex("L", color=GREEN).next_to(matrix_l, UP)

#         self.play(Write(title))
#         self.play(FadeIn(matrix_a), FadeIn(label_a))
#         self.play(Write(recurrence))
#         self.play(FadeIn(matrix_l), FadeIn(label_l))

#         steps = [
#             {
#                 "formula": r"L_{11}=\sqrt{A_{11}}=\sqrt{4}=2",
#                 "value": "2",
#                 "target": (1, 1),
#                 "highlights": [(1, 1)],
#             },
#             {
#                 "formula": r"L_{21}=\frac{A_{21}}{L_{11}}=\frac{12}{2}=6",
#                 "value": "6",
#                 "target": (2, 1),
#                 "highlights": [(2, 1), (1, 1)],
#             },
#             {
#                 "formula": r"L_{31}=\frac{A_{31}}{L_{11}}=\frac{-16}{2}=-8",
#                 "value": "-8",
#                 "target": (3, 1),
#                 "highlights": [(3, 1), (1, 1)],
#             },
#             {
#                 "formula": r"L_{22}=\sqrt{A_{22}-L_{21}^2}=\sqrt{37-6^2}=1",
#                 "value": "1",
#                 "target": (2, 2),
#                 "highlights": [(2, 2), (2, 1)],
#             },
#             {
#                 "formula": r"L_{32}=\frac{A_{32}-L_{31}L_{21}}{L_{22}}=\frac{-43-(-8)(6)}{1}=5",
#                 "value": "5",
#                 "target": (3, 2),
#                 "highlights": [(3, 2), (3, 1), (2, 1), (2, 2)],
#             },
#             {
#                 "formula": r"L_{33}=\sqrt{A_{33}-(L_{31}^2+L_{32}^2)}=\sqrt{98-(64+25)}=3",
#                 "value": "3",
#                 "target": (3, 3),
#                 "highlights": [(3, 3), (3, 1), (3, 2)],
#             },
#         ]

#         # Đặt hộp công thức sang góc phải bên dưới
#         formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.8)
#         formula_box.move_to(RIGHT * 2.5 + DOWN * 1.5)
#         self.play(Write(formula_box))

#         for step in steps:
#             new_formula = MathTex(step["formula"], color=YELLOW).scale(0.8)
#             new_formula.move_to(formula_box)
#             self.play(Transform(formula_box, new_formula))

#             highlight_boxes = []
#             for row, col in step["highlights"]:
#                 box = self.highlight_cell(matrix_a, row, col, color=ORANGE)
#                 highlight_boxes.append(box)
#                 self.play(FadeIn(box), run_time=0.18)

#             row, col = step["target"]
#             n = 3
#             target_idx = (row - 1) * n + (col - 1)
#             l_entries = matrix_l.get_entries()
#             target_entry = l_entries[target_idx]

#             flying = MathTex(step["value"], color=GREEN).scale(0.9)
#             flying.next_to(formula_box, UP, buff=0.3)

#             self.play(FadeIn(flying, shift=UP * 0.1))
#             self.play(flying.animate.move_to(target_entry.get_center()), run_time=0.7)

#             filled = MathTex(step["value"], color=WHITE).move_to(target_entry.get_center())
#             self.play(Transform(target_entry, filled), FadeOut(flying), run_time=0.3)

#             for box in highlight_boxes:
#                 self.play(FadeOut(box), run_time=0.15)

#         # Xóa bớt công thức để lấy không gian hiển thị L^T
#         self.play(FadeOut(formula_box))

#         matrix_lt = Matrix(
#             self.to_manim_str_matrix(self.transpose(self.L)),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.85)
#         matrix_lt.move_to(RIGHT * 2.5 + DOWN * 0.8)
#         label_lt = MathTex("L^T", color=GREEN).scale(0.9).next_to(matrix_lt, UP, buff=0.15)

#         product_text = MathTex(r"L \times L^T = A", color=GREEN).scale(0.9)
#         product_text.next_to(matrix_l, DOWN, buff=0.8).shift(RIGHT * 2.5) # Căn giữa hai ma trận

#         computed = self.matmul(self.L, self.transpose(self.L))
#         status = "ĐẠT" if all(
#             abs(computed[i][j] - self.A[i][j]) < 1e-8
#             for i in range(3)
#             for j in range(3)
#         ) else "THẤT BẠI"
#         verify_text = Text(f"Kiểm tra nhân ma trận: {status}", color=GREEN if status == "ĐẠT" else RED, font_size=24)
#         verify_text.next_to(product_text, DOWN, buff=0.2)

#         self.play(FadeIn(matrix_lt), FadeIn(label_lt))
#         self.play(Write(product_text))
#         self.play(Write(verify_text))
#         self.wait(1.2)

#     # ===========================
#     # Part 4: Cost comparison
#     # ===========================
#     def part4_cost(self):
#         title = Text("Phần 4: Chi phí tính toán", color=YELLOW, font_size=36)
#         title.to_edge(UP)

#         lu_bar = BarChart(
#             values=[1.0],
#             bar_names=["LU"],
#             y_range=[0, 1.2, 0.2],
#             y_length=4,
#             x_length=3,
#             bar_colors=[RED],
#         ).scale(0.7)
#         lu_bar.shift(LEFT * 2.8 + DOWN * 0.4)

#         chol_bar = BarChart(
#             values=[1.0],
#             bar_names=["Cholesky"],
#             y_range=[0, 1.2, 0.2],
#             y_length=4,
#             x_length=3,
#             bar_colors=[GREEN],
#         ).scale(0.7)
#         chol_bar.shift(RIGHT * 2.8 + DOWN * 0.4)

#         note_before = VGroup(
#             Text("So sánh: LU", font_size=28, color=WHITE),
#             MathTex(r"\approx \frac{2}{3}n^3,", color=WHITE),
#             Text("Cholesky", font_size=28, color=WHITE),
#             MathTex(r"\approx \frac{1}{3}n^3", color=WHITE)
#         ).arrange(RIGHT, buff=0.15)
#         note_before.to_edge(DOWN, buff=0.8)

#         self.play(Write(title))
#         self.play(FadeIn(lu_bar), FadeIn(chol_bar))
#         self.play(Write(note_before))

#         chol_rect = chol_bar.bars[0]
#         self.play(chol_rect.animate.scale([1, 0.5, 1], about_edge=DOWN), run_time=1.4)

#         note_after = VGroup(
#             Text("Chi phí Cholesky ", font_size=28, color=GREEN),
#             MathTex(r"\approx \frac{1}{2}", color=GREEN),
#             Text(" so với LU (trên ma trận SPD)", font_size=28, color=GREEN)
#         ).arrange(RIGHT, buff=0.1)
#         note_after.next_to(note_before, UP, buff=0.4)
        
#         self.play(Write(note_after))
#         self.wait(1)

#     # ============================================
#     # Part 5: Diagonalization A = P D P^{-1}
#     # ============================================
#     def part5_diagonalization(self):
#         title = Text("Phần 5: Chéo hóa ma trận", color=YELLOW, font_size=36)
#         title.to_edge(UP)

#         char_eq = MathTex(r"\det(A-\lambda I)=0", color=WHITE).scale(0.95)
#         char_eq.next_to(title, DOWN, buff=0.4)

#         lambdas = VGroup(
#             MathTex(r"\lambda_1\approx 123.4772 > 0", color=GREEN).scale(0.75),
#             MathTex(r"\lambda_2\approx 15.5040 > 0", color=GREEN).scale(0.75),
#             MathTex(r"\lambda_3\approx 0.0188 > 0", color=GREEN).scale(0.75),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
#         lambdas.to_edge(LEFT, buff=0.8).shift(UP * 0.7)

#         self.play(Write(title))
#         self.play(Write(char_eq))
#         self.play(FadeIn(lambdas))

#         # Show eigenvectors and group them into matrix P. Scale nhỏ xuống tránh đụng đáy.
#         v1 = MathTex(r"v_1=\begin{bmatrix}0.1630\\-0.2127\\0.9635\end{bmatrix}", color=BLUE).scale(0.65)
#         v2 = MathTex(r"v_2=\begin{bmatrix}0.4573\\-0.8489\\-0.2648\end{bmatrix}", color=BLUE).scale(0.65)
#         v3 = MathTex(r"v_3=\begin{bmatrix}-0.8742\\-0.4838\\0.0411\end{bmatrix}", color=BLUE).scale(0.65)
#         vec_group = VGroup(v1, v2, v3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
#         vec_group.to_edge(LEFT, buff=0.8).shift(DOWN * 1.5)

#         self.play(FadeIn(vec_group))

#         p_matrix = Matrix(
#             [
#                 ["0.1630", "0.4573", "-0.8742"],
#                 ["-0.2127", "-0.8489", "-0.4838"],
#                 ["0.9635", "-0.2648", "0.0411"],
#             ],
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.65)
#         p_matrix.to_edge(RIGHT, buff=1.2).shift(UP * 1.2)
#         p_label = MathTex("P", color=ORANGE).next_to(p_matrix, UP, buff=0.1)

#         # Di chuyển nhẹ vectors để focus vào P
#         self.play(vec_group.animate.to_edge(LEFT, buff=0.4).shift(RIGHT * 0.5))
#         self.play(FadeIn(p_matrix), FadeIn(p_label))

#         d_matrix = Matrix(
#             [
#                 ["123.4772", "0", "0"],
#                 ["0", "15.5040", "0"],
#                 ["0", "0", "0.0188"],
#             ],
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.65)
#         d_matrix.next_to(p_matrix, DOWN, buff=0.6)
#         d_label = MathTex("D", color=ORANGE).next_to(d_matrix, UP, buff=0.1)

#         pinv_tex = VGroup(
#             MathTex("P^{-1}", color=WHITE),
#             Text("(nghịch đảo của P)", font_size=24, color=WHITE)
#         ).arrange(RIGHT, buff=0.15)
#         pinv_tex.next_to(d_matrix, DOWN, buff=0.35)

#         final_formula = MathTex(r"A = P D P^{-1}", color=GREEN).scale(1.1)
#         final_formula.to_edge(DOWN, buff=0.4)

#         self.play(FadeIn(d_matrix), FadeIn(d_label))
#         self.play(Write(pinv_tex))
#         self.play(Write(final_formula))
#         self.wait(1.5)


# DEFAULT_SCENE = "CholeskyDecomposition"


# def _run_cmd(cmd: list[str], cwd: Path) -> None:
#     completed = subprocess.run(cmd, cwd=str(cwd), check=False)
#     if completed.returncode != 0:
#         raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}")


# def _check_runtime_dependencies() -> None:
#     required = {
#         "latex": "MiKTeX/TexLive latex compiler",
#         "dvisvgm": "dvisvgm (usually bundled with MiKTeX)",
#         "ffmpeg": "FFmpeg video backend",
#     }

#     missing = []
#     for exe, description in required.items():
#         if shutil.which(exe) is None:
#             missing.append((exe, description))

#     if not missing:
#         return

#     lines = ["Missing runtime dependencies required by MathTex/Manim:"]
#     for exe, description in missing:
#         lines.append(f"- {exe}: {description}")
#     lines.extend(
#         [
#             "",
#             "Suggested fixes on Windows:",
#             "1) Install MiKTeX: winget install --id MiKTeX.MiKTeX --source winget --accept-package-agreements --accept-source-agreements --silent",
#             "2) Install FFmpeg: winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent",
#             "3) Close and reopen terminal/VS Code so PATH is refreshed.",
#             "4) Verify with: where latex, where dvisvgm, where ffmpeg",
#         ]
#     )
#     raise RuntimeError("\n".join(lines))


# def _find_latest_scene_video(project_dir: Path, scene_name: str) -> Path:
#     root = project_dir / "media" / "videos" / "manim_scene1"
#     matches = list(root.glob(f"*/{scene_name}.mp4"))
#     if not matches:
#         raise FileNotFoundError(f"Rendered scene file not found: {scene_name}")
#     matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
#     return matches[0]


# def main() -> int:
#     parser = argparse.ArgumentParser(
#         description="Run this file directly to render CholeskyDecomposition scene.",
#     )
#     parser.add_argument("--scene", default=DEFAULT_SCENE)
#     parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="m")
#     parser.add_argument("--disable-caching", action="store_true")
#     args = parser.parse_args()

#     project_dir = Path(__file__).resolve().parent
#     file_name = Path(__file__).name

#     _check_runtime_dependencies()

#     quality_flag = f"-q{args.quality}"
#     cmd = [
#         sys.executable,
#         "-m",
#         "manim",
#         quality_flag,
#         file_name,
#         args.scene,
#     ]
#     if args.disable_caching:
#         cmd.append("--disable_caching")

#     print(f"[render] scene={args.scene}, quality={args.quality}")
#     _run_cmd(cmd, cwd=project_dir)

#     video_path = _find_latest_scene_video(project_dir, args.scene)
#     print(f"[done] video: {video_path}")

#     # Auto-open video only when running in interactive terminal.
#     if os.name == "nt":
#         try:
#             os.startfile(video_path)  # type: ignore[attr-defined]
#         except OSError:
#             pass
#     return 0


# if __name__ == "__main__":
#     raise SystemExit(main())















# """Manim visualization for Cholesky decomposition and diagonalization.

# This file follows the project constraints:
# - Core matrix computations are implemented with pure Python list-of-lists.
# - No use of numpy.array for algorithm implementation.
# - Uses Manim Matrix and MathTex for visual rendering.
# """

# from __future__ import annotations

# import argparse
# import math
# import os
# from pathlib import Path
# import shutil
# import subprocess
# import sys

# from manim import (
#     BLUE, GREEN, ORANGE, PURPLE, RED, WHITE, YELLOW,
#     DOWN, LEFT, RIGHT, UP, UL, UR, DL, PI, # Thêm DL vào đây
#     BarChart,
#     FadeIn,
#     FadeOut,
#     MathTex,
#     Matrix,
#     Scene,
#     SurroundingRectangle,
#     Text,
#     Transform,
#     VGroup,
#     Write,
#     AnimationGroup,
#     Indicate,
#     Create
# )


# class CholeskyAndDiagonalization(Scene):
#     """Full storyboard scene with 6 parts avoiding visual overlap."""

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.A = [
#             [4.0, 12.0, -16.0],
#             [12.0, 37.0, -43.0],
#             [-16.0, -43.0, 98.0],
#         ]

#         # Precomputed results for stable animation rendering.
#         self.L = self.cholesky_decompose(self.A)
        
#         # Hardcoded for Part 6 visualization
#         self.lambdas = [123.4772, 15.5040, 0.0188]
#         self.eigenvectors = [
#             [0.1630, 0.4573, -0.8742],
#             [-0.2127, -0.8489, -0.4838],
#             [0.9635, -0.2648, 0.0411],
#         ]

#     def construct(self):
#         self.part1_roadmap()
#         self.part2_intro()
#         self.part3_spd_check()
#         self.part4_l_calculation()
#         self.part5_cost()
#         self.part6_diagonalization()

#     # ============================
#     # Pure list-based math helpers
#     # ============================
#     def transpose(self, matrix: list[list[float]]) -> list[list[float]]:
#         return [list(row) for row in zip(*matrix)]

#     def matmul(self, a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
#         rows = len(a)
#         cols = len(b[0])
#         shared = len(b)
#         result = [[0.0 for _ in range(cols)] for _ in range(rows)]
#         for i in range(rows):
#             for k in range(shared):
#                 av = a[i][k]
#                 if av == 0.0:
#                     continue
#                 for j in range(cols):
#                     result[i][j] += av * b[k][j]
#         return result

#     def cholesky_decompose(self, matrix: list[list[float]]) -> list[list[float]]:
#         n = len(matrix)
#         l = [[0.0 for _ in range(n)] for _ in range(n)]
#         for i in range(n):
#             for j in range(i + 1):
#                 if i == j:
#                     s = sum(l[i][k] * l[i][k] for k in range(j))
#                     l[i][j] = math.sqrt(matrix[i][i] - s)
#                 else:
#                     s = sum(l[i][k] * l[j][k] for k in range(j))
#                     l[i][j] = (matrix[i][j] - s) / l[j][j]
#         return l

#     def fmt(self, value: float) -> str:
#         if abs(value - round(value)) < 1e-9:
#             return str(int(round(value)))
#         return f"{value:.4f}"

#     def to_manim_str_matrix(self, matrix: list[list[float]]) -> list[list[str]]:
#         return [[self.fmt(x) for x in row] for row in matrix]

#     def highlight_cell(self, matrix: Matrix, row: int, col: int, color=YELLOW):
#         entries = matrix.get_entries()
#         n = int(round(math.sqrt(len(entries))))
#         idx = (row - 1) * n + (col - 1)
#         return SurroundingRectangle(entries[idx], color=color, buff=0.08)

#     # ==========================================
#     # Part 1: Giới thiệu tổng quan lộ trình
#     # ==========================================
#     def part1_roadmap(self):
#         title = Text("Phân rã Cholesky và Chéo hóa Ma trận", color=YELLOW, font_size=40, weight="BOLD")
#         title.to_edge(UP, buff=1.0)

#         steps = [
#             "1. Giới thiệu bài toán & Khởi tạo ma trận.",
#             "2. Kiểm tra điều kiện ma trận SPD.",
#             "3. Thuật toán tính toán L (Step-by-step).",
#             "4. Ưu điểm về chi phí tính toán.",
#             "5. Thuật toán Chéo hóa ma trận."
#         ]
        
#         step_texts = VGroup(*[Text(step, font_size=28, color=WHITE) for step in steps])
#         step_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
#         step_texts.next_to(title, DOWN, buff=0.8)

#         self.play(Write(title))
        
#         # Mờ dần xuất hiện từ trên xuống
#         self.play(AnimationGroup(*[FadeIn(t, shift=DOWN*0.3) for t in step_texts], lag_ratio=0.3))
#         self.wait(1)

#         # Highlight mục 1
#         box = SurroundingRectangle(step_texts[0], color=GREEN, buff=0.2)
#         self.play(Create(box))
#         self.wait(1.5)

#         # Dọn dẹp toàn màn hình
#         self.clear()

#     # ==========================================
#     # Part 2: Đặt vấn đề và Định nghĩa
#     # ==========================================
#     def part2_intro(self):
#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda x: MathTex(x),
#         ).scale(0.9)
#         matrix_a.move_to(UP * 0.5)
#         label_a = MathTex("A =", color=ORANGE).next_to(matrix_a, LEFT)
#         group_a = VGroup(label_a, matrix_a)

#         self.play(FadeIn(group_a))

#         question = Text("Làm thế nào để phân rã ma trận A này thành các ma trận tam giác?", font_size=28, color=YELLOW)
#         question.next_to(group_a, DOWN, buff=0.8)
#         self.play(Write(question))
#         self.wait(1.5)

#         # Transform câu hỏi thành công thức A = LL^T
#         formula = MathTex(r"A = L L^T", color=GREEN).scale(1.5)
#         formula.move_to(question.get_center())
#         self.play(Transform(question, formula))
#         self.wait(1)

#         # Dịch chuyển A=LL^T sang trái để nhường chỗ vẽ L
#         self.play(
#             group_a.animate.scale(0.7).to_corner(UL).shift(DOWN*0.5),
#             question.animate.scale(0.8).next_to(group_a, DOWN, buff=0.5, aligned_edge=LEFT)
#         )

#         # Vẽ ma trận L mô phỏng
#         l_template = [
#             ["L_{11}", "0", "0"],
#             ["L_{21}", "L_{22}", "0"],
#             ["L_{31}", "L_{32}", "L_{33}"]
#         ]
#         matrix_l = Matrix(l_template).scale(0.9)
#         matrix_l.move_to(RIGHT * 2)
        
#         # Tô màu đỏ các số 0
#         entries = matrix_l.get_entries()
#         entries[1].set_color(RED)  # row 1 col 2
#         entries[2].set_color(RED)  # row 1 col 3
#         entries[5].set_color(RED)  # row 2 col 3

#         desc = Text("L là ma trận tam giác dưới (nửa trên bằng 0)", font_size=24, color=WHITE)
#         desc.next_to(matrix_l, DOWN, buff=0.5)

#         self.play(FadeIn(matrix_l), Write(desc))
#         self.wait(2)
#         self.clear()

#     # ==========================================
#     # Part 3: Kiểm tra SPD tỉ mỉ
#     # ==========================================
#     def part3_spd_check(self):
#         title = Text("Điều kiện: A phải là ma trận SPD", color=YELLOW, font_size=32)
#         title.to_edge(UP)
#         self.play(Write(title))

#         matrix_a = Matrix(self.to_manim_str_matrix(self.A)).scale(0.75)
#         matrix_a.move_to(UP * 0.5)
        
#         # 3.1 Tính đối xứng
#         sym_text = Text("1. Tính đối xứng (Symmetric):", font_size=24, color=WHITE).to_corner(UL).shift(DOWN)
#         self.play(Write(sym_text), FadeIn(matrix_a))

#         matrix_at = matrix_a.copy().set_color(BLUE).move_to(RIGHT * 3 + UP * 0.5)
#         label_at = MathTex("A^T", color=BLUE).next_to(matrix_at, UP)
#         self.play(FadeIn(matrix_at), FadeIn(label_at))
        
#         # Xoay quanh đường chéo chính (axis=[1, -1, 0])
#         self.play(matrix_at.animate.rotate(PI, axis=[1, -1, 0]).move_to(matrix_a.get_center()), run_time=1.5)
#         sym_result = MathTex(r"A = A^T", color=GREEN).next_to(matrix_a, DOWN)
#         self.play(Write(sym_result))
#         self.wait(1)
        
#         # Dọn dẹp để qua 3.2
#         self.play(FadeOut(sym_text), FadeOut(matrix_at), FadeOut(label_at), FadeOut(sym_result))

#         # 3.2 Sylvester
#         sylv_text = Text("2. Tiêu chuẩn Sylvester (Leading principal minors > 0)", font_size=24, color=WHITE).to_corner(UL).shift(DOWN)
#         self.play(Write(sylv_text))

#         # Dịch ma trận A sang trái một chút
#         self.play(matrix_a.animate.move_to(LEFT * 3 + UP * 0.5))

#         entries = matrix_a.get_entries()
        
#         # Delta 1
#         box1 = SurroundingRectangle(entries[0], color=RED)
#         calc1 = MathTex(r"\Delta_1 = \det([4]) = 4 > 0", color=RED).scale(0.8)
#         calc1.move_to(RIGHT * 2 + UP * 1)
#         self.play(Create(box1), Write(calc1))
#         self.wait(1)

#         # Delta 2
#         box2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE)
#         calc2 = MathTex(r"\Delta_2 = (4 \times 37) - (12 \times 12) = 4 > 0", color=PURPLE).scale(0.8)
#         calc2.next_to(calc1, DOWN, buff=0.4, aligned_edge=LEFT)
#         self.play(Transform(box1, box2), Write(calc2))
#         self.wait(1)

#         # Delta 3 (Chi tiết)
#         self.play(FadeOut(calc1), FadeOut(calc2)) # Dọn chỗ
#         box3 = SurroundingRectangle(VGroup(*entries), color=YELLOW)
        
#         calc3_1 = MathTex(r"\Delta_3 = 4(37 \cdot 98 - (-43)^2) - 12(12 \cdot 98 - (-16)(-43)) - 16(12 \cdot (-43) - 37(-16))", color=YELLOW).scale(0.65)
#         calc3_2 = MathTex(r"\Delta_3 = 4(1777) - 12(488) - 16(76)", color=YELLOW).scale(0.7)
#         calc3_3 = MathTex(r"\Delta_3 = 7108 - 5856 - 1216 = 36 > 0", color=YELLOW).scale(0.8)

#         calc_group = VGroup(calc3_1, calc3_2, calc3_3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
#         calc_group.move_to(DOWN * 2)

#         self.play(Transform(box1, box3))
#         self.play(Write(calc3_1))
#         self.wait(1)
#         self.play(Write(calc3_2))
#         self.wait(1)
#         self.play(Write(calc3_3))
#         self.wait(1)

#         # Đóng mộc PASSED
#         stamp = Text("PASSED", color=GREEN, font_size=50, weight="BOLD")
#         stamp.rotate(15 * PI / 180).move_to(matrix_a.get_center())
#         self.play(FadeIn(stamp, scale=2.0))
#         self.wait(2)
        
#         self.clear()

#     # ==========================================
#     # Part 4: Tính toán L (Trực quan trái-phải)
#     # ==========================================
#     def part4_l_calculation(self):
#         title = Text("Bước 3: Thuật toán tính toán L", color=YELLOW, font_size=32).to_edge(UP)
        
#         # A bên trái, L rỗng bên phải
#         matrix_a = Matrix(self.to_manim_str_matrix(self.A)).scale(0.7)
#         matrix_a.move_to(LEFT * 3.5 + UP * 1)
#         label_a = MathTex("A", color=ORANGE).scale(0.8).next_to(matrix_a, UP)

#         l_template = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
#         matrix_l = Matrix(l_template).scale(0.7)
#         matrix_l.move_to(RIGHT * 3.5 + UP * 1)
#         label_l = MathTex("L", color=GREEN).scale(0.8).next_to(matrix_l, UP)
        
#         # Làm mờ tam giác trên của L
#         for i, entry in enumerate(matrix_l.get_entries()):
#             if i in [1, 2, 5]: # Các vị trí 0
#                 entry.set_opacity(0.3)
#             else:
#                 entry.set_opacity(0.0) # Ẩn các ô chờ bay vào

#         # Công thức lặp góc dưới trái
#         recurrence = VGroup(
#             MathTex(r"L_{jj}=\sqrt{A_{jj}-\sum L_{jk}^2}", color=WHITE),
#             MathTex(r"L_{ij}=\frac{1}{L_{jj}}(A_{ij}-\sum L_{ik}L_{jk})", color=WHITE)
#         ).arrange(DOWN, aligned_edge=LEFT).scale(0.55).to_corner(DL).shift(UP*0.5)

#         self.play(Write(title), FadeIn(matrix_a), FadeIn(label_a), FadeIn(matrix_l), FadeIn(label_l), Write(recurrence))

#         # Hộp công thức ở giữa bên dưới
#         steps = [
#             {"formula": r"L_{11}=\sqrt{4}=2", "val": "2", "pos": (1,1), "hl": [(1,1)]},
#             {"formula": r"L_{21}=12/2=6", "val": "6", "pos": (2,1), "hl": [(2,1), (1,1)]},
#             {"formula": r"L_{31}=-16/2=-8", "val": "-8", "pos": (3,1), "hl": [(3,1), (1,1)]},
#             {"formula": r"L_{22}=\sqrt{37-6^2}=1", "val": "1", "pos": (2,2), "hl": [(2,2), (2,1)]},
#             {"formula": r"L_{32}=\frac{1}{1}(-43-(-8 \times 6))=5", "val": "5", "pos": (3,2), "hl": [(3,2), (3,1), (2,1)]},
#             {"formula": r"L_{33}=\sqrt{98-((-8)^2+5^2)}=3", "val": "3", "pos": (3,3), "hl": [(3,3), (3,1), (3,2)]},
#         ]

#         formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.8).move_to(DOWN * 1.5)
#         self.play(Write(formula_box))

#         for step in steps:
#             # Update công thức
#             new_formula = MathTex(step["formula"], color=YELLOW).scale(0.8).move_to(formula_box)
#             self.play(Transform(formula_box, new_formula))

#             # Highlight A
#             hl_boxes = [self.highlight_cell(matrix_a, r, c, ORANGE) for r, c in step["hl"]]
#             self.play(*[FadeIn(box) for box in hl_boxes], run_time=0.5)

#             # Bay số vào L
#             target_entry = matrix_l.get_entries()[(step["pos"][0]-1)*3 + (step["pos"][1]-1)]
#             flying_num = MathTex(step["val"], color=GREEN).scale(0.8).move_to(formula_box).shift(UP*0.5)
            
#             self.play(FadeIn(flying_num, shift=UP*0.2))
#             self.play(flying_num.animate.move_to(target_entry.get_center()), run_time=0.8)
            
#             target_entry.become(MathTex(step["val"], color=WHITE).scale(0.7).move_to(target_entry.get_center()))
#             target_entry.set_opacity(1.0)
            
#             self.play(FadeOut(flying_num), *[FadeOut(box) for box in hl_boxes], run_time=0.3)

#         self.wait(2)
#         self.clear()

#     # ==========================================
#     # Part 5: Chi phí tính toán
#     # ==========================================
#     def part5_cost(self):
#         title = Text("Bước 4: Ưu điểm Chi phí tính toán", color=YELLOW, font_size=32).to_edge(UP)
        
#         chart = BarChart(
#             values=[2.0, 1.0], 
#             bar_names=["LU", "Cholesky"],
#             y_range=[0, 2.5, 0.5],
#             bar_colors=[RED, GREEN],
#             y_length=4, x_length=4
#         ).move_to(UP * 0.5)

#         stats = VGroup(
#             MathTex(r"\text{LU} \approx \frac{2}{3}n^3", color=RED),
#             MathTex(r"\text{Cholesky} \approx \frac{1}{3}n^3", color=GREEN)
#         ).arrange(RIGHT, buff=1.0).next_to(chart, DOWN, buff=0.5)

#         conclusion = Text("Tối ưu 50% khối lượng tính toán cho ma trận SPD", font_size=28, color=YELLOW)
#         conclusion.next_to(stats, DOWN, buff=0.5)

#         self.play(Write(title), FadeIn(chart))
#         self.play(Write(stats))
#         self.play(Write(conclusion))
#         self.wait(2)
#         self.clear()

#     # ==========================================
#     # Part 6: Chéo hóa ma trận tỉ mỉ
#     # ==========================================
#     def part6_diagonalization(self):
#         # 6.1 Giải thích lý thuyết
#         title = Text("Bước 5: Chéo hóa Ma trận", color=YELLOW, font_size=32).to_edge(UP)
#         formula = MathTex(r"A = P D P^{-1}", color=GREEN).scale(1.5).move_to(UP * 1.5)
        
#         desc = Text("Mục tiêu: Tìm ma trận đường chéo D (Trị riêng) và P (Vector riêng)", font_size=24, color=WHITE)
#         desc.next_to(formula, DOWN, buff=0.5)

#         self.play(Write(title), Write(formula), FadeIn(desc))
#         self.wait(2)
        
#         # Đẩy lên góc trái
#         theory_group = VGroup(formula, desc)
#         self.play(theory_group.animate.scale(0.5).to_corner(UL).shift(DOWN*0.5))

#         # 6.2 Tìm D
#         step_d = Text("1. Tìm ma trận D (Giải PT đặc trưng)", font_size=24, color=BLUE).move_to(LEFT*2.5 + UP*1.5)
#         char_eq = MathTex(r"\det(A - \lambda I) = 0", color=WHITE).next_to(step_d, DOWN, aligned_edge=LEFT)
        
#         mat_a_lam = Matrix([
#             ["4-\\lambda", "12", "-16"],
#             ["12", "37-\\lambda", "-43"],
#             ["-16", "-43", "98-\\lambda"]
#         ]).scale(0.6).next_to(char_eq, DOWN, aligned_edge=LEFT)

#         self.play(Write(step_d), Write(char_eq), FadeIn(mat_a_lam))
        
#         # Nhấp nháy lambda
#         self.play(Indicate(mat_a_lam.get_entries()[0], color=YELLOW), Indicate(mat_a_lam.get_entries()[4], color=YELLOW), Indicate(mat_a_lam.get_entries()[8], color=YELLOW))
        
#         lambdas_text = VGroup(
#             MathTex(r"\lambda_1 \approx 123.48", color=GREEN),
#             MathTex(r"\lambda_2 \approx 15.50", color=GREEN),
#             MathTex(r"\lambda_3 \approx 0.02", color=GREEN)
#         ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).next_to(mat_a_lam, RIGHT, buff=0.5)
#         self.play(FadeIn(lambdas_text))

#         # Tạo D bên phải
#         mat_d = Matrix([
#             ["\\lambda_1", "0", "0"],
#             ["0", "\\lambda_2", "0"],
#             ["0", "0", "\\lambda_3"]
#         ]).scale(0.7).to_edge(RIGHT, buff=1.0).shift(UP*0.5)
#         label_d = MathTex("D = ", color=GREEN).scale(0.8).next_to(mat_d, LEFT)
        
#         self.play(FadeIn(mat_d), FadeIn(label_d))
#         self.wait(1)

#         # Dọn phần trái để làm 6.3
#         self.play(FadeOut(step_d), FadeOut(char_eq), FadeOut(mat_a_lam), FadeOut(lambdas_text))

#         # 6.3 Tìm P (Khử Gauss)
#         step_p = Text("2. Tìm ma trận P (Giải hệ phương trình)", font_size=24, color=BLUE).move_to(LEFT*3 + UP*1.5)
#         sys_eq = MathTex(r"(A - \lambda_1 I)v_1 = 0", color=WHITE).next_to(step_p, DOWN, aligned_edge=LEFT)
        
#         # Hiển thị số cụ thể (hardcode cho đẹp minh họa)
#         mat_gauss = Matrix([
#             ["-119.48", "12", "-16"],
#             ["12", "-86.48", "-43"],
#             ["-16", "-43", "-25.48"]
#         ]).scale(0.6).next_to(sys_eq, DOWN, aligned_edge=LEFT)
        
#         # arrow = MathTex(r"\xrightarrow{\text{Khử Gauss}}").next_to(mat_gauss, RIGHT)
#         # Tạo mũi tên trơn
#         arrow_symbol = MathTex(r"\longrightarrow").next_to(mat_gauss, RIGHT)
#         # Dùng Text để hiển thị tiếng Việt và đặt lên trên mũi tên
#         arrow_text = Text("Khử Gauss", font_size=20, color=WHITE).next_to(arrow_symbol, UP, buff=0.1)
#         # Gom chúng lại thành 1 nhóm tên là 'arrow' để các lệnh phía sau hoạt động bình thường
#         arrow = VGroup(arrow_symbol, arrow_text)
#         v1 = Matrix([["0.16"], ["-0.21"], ["0.96"]]).scale(0.6).next_to(arrow, RIGHT)
#         label_v1 = MathTex("v_1=").scale(0.7).next_to(v1, LEFT)

#         self.play(Write(step_p), Write(sys_eq))
#         self.play(FadeIn(mat_gauss))
#         self.play(Write(arrow), FadeIn(v1), FadeIn(label_v1))
#         self.wait(1)

#         v2 = MathTex(r"v_2 = \begin{bmatrix}0.45\\-0.84\\-0.26\end{bmatrix}").scale(0.6).next_to(v1, DOWN, buff=0.2).align_to(label_v1, LEFT)
#         v3 = MathTex(r"v_3 = \begin{bmatrix}-0.87\\-0.48\\0.04\end{bmatrix}").scale(0.6).next_to(v2, DOWN, buff=0.2).align_to(label_v1, LEFT)
#         self.play(FadeIn(v2), FadeIn(v3))
#         self.wait(1)

#         # Dọn dẹp để qua 6.4
#         self.play(FadeOut(step_p), FadeOut(sys_eq), FadeOut(mat_gauss), FadeOut(arrow))

#         # 6.4 Tổng hợp
#         # Gom các vector lại thành P
#         p_matrix = Matrix([
#             ["0.16", "0.45", "-0.87"],
#             ["-0.21", "-0.84", "-0.48"],
#             ["0.96", "-0.26", "0.04"]
#         ]).scale(0.7).move_to(LEFT * 2 + DOWN * 2)
#         label_p = MathTex("P =", color=ORANGE).scale(0.8).next_to(p_matrix, LEFT)

#         # Transform các vi rải rác thành P
#         self.play(Transform(VGroup(label_v1, v1, v2, v3), VGroup(label_p, p_matrix)))
        
#         # Chuyển D xuống ngang hàng
#         self.play(VGroup(label_d, mat_d).animate.next_to(p_matrix, RIGHT, buff=0.8))

#         # Hiển thị P^-1
#         pinv_matrix = MathTex(r"P^{-1}").scale(1.2).next_to(mat_d, RIGHT, buff=0.8)
#         self.play(FadeIn(pinv_matrix))

#         final = MathTex(r"A = P \times D \times P^{-1}", color=YELLOW).scale(1.2).move_to(DOWN * 3)
#         self.play(Write(final))
#         self.wait(3)


# DEFAULT_SCENE = "CholeskyAndDiagonalization"


# def _run_cmd(cmd: list[str], cwd: Path) -> None:
#     completed = subprocess.run(cmd, cwd=str(cwd), check=False)
#     if completed.returncode != 0:
#         raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}")


# def _check_runtime_dependencies() -> None:
#     required = {
#         "latex": "MiKTeX/TexLive latex compiler",
#         "dvisvgm": "dvisvgm (usually bundled with MiKTeX)",
#         "ffmpeg": "FFmpeg video backend",
#     }

#     missing = []
#     for exe, description in required.items():
#         if shutil.which(exe) is None:
#             missing.append((exe, description))

#     if not missing:
#         return

#     lines = ["Missing runtime dependencies required by MathTex/Manim:"]
#     for exe, description in missing:
#         lines.append(f"- {exe}: {description}")
#     lines.extend(
#         [
#             "",
#             "Suggested fixes on Windows:",
#             "1) Install MiKTeX: winget install --id MiKTeX.MiKTeX --source winget --accept-package-agreements --accept-source-agreements --silent",
#             "2) Install FFmpeg: winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent",
#             "3) Close and reopen terminal/VS Code so PATH is refreshed.",
#             "4) Verify with: where latex, where dvisvgm, where ffmpeg",
#         ]
#     )
#     raise RuntimeError("\n".join(lines))


# def _find_latest_scene_video(project_dir: Path, scene_name: str) -> Path:
#     root = project_dir / "media" / "videos" / "manim_scene1"
#     matches = list(root.glob(f"*/{scene_name}.mp4"))
#     if not matches:
#         raise FileNotFoundError(f"Rendered scene file not found: {scene_name}")
#     matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
#     return matches[0]


# def main() -> int:
#     parser = argparse.ArgumentParser(
#         description="Run this file directly to render CholeskyDecomposition scene.",
#     )
#     parser.add_argument("--scene", default=DEFAULT_SCENE)
#     parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="m")
#     parser.add_argument("--disable-caching", action="store_true")
#     args = parser.parse_args()

#     project_dir = Path(__file__).resolve().parent
#     file_name = Path(__file__).name

#     _check_runtime_dependencies()

#     quality_flag = f"-q{args.quality}"
#     cmd = [
#         sys.executable,
#         "-m",
#         "manim",
#         quality_flag,
#         file_name,
#         args.scene,
#     ]
#     if args.disable_caching:
#         cmd.append("--disable_caching")

#     print(f"[render] scene={args.scene}, quality={args.quality}")
#     _run_cmd(cmd, cwd=project_dir)

#     video_path = _find_latest_scene_video(project_dir, args.scene)
#     print(f"[done] video: {video_path}")

#     # Auto-open video only when running in interactive terminal.
#     if os.name == "nt":
#         try:
#             os.startfile(video_path)  # type: ignore[attr-defined]
#         except OSError:
#             pass
#     return 0

# if __name__ == "__main__":
#     raise SystemExit(main())











"""Manim visualization for Cholesky decomposition and diagonalization.

This file follows the project constraints:
- Core matrix computations are implemented with pure Python list-of-lists.
- No use of numpy.array for algorithm implementation.
- Uses Manim Matrix and MathTex for visual rendering.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

from manim import (
    BLUE,
    GREEN,
    ORANGE,
    PURPLE,
    RED,
    WHITE,
    YELLOW,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UL,
    UR,
    DL,  # Đã fix lỗi thiếu DL
    PI,
    BarChart,
    FadeIn,
    FadeOut,
    MathTex,
    Matrix,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
    AnimationGroup,
    Indicate,
    Create
)


class CholeskyAndDiagonalization(Scene):
    """Full storyboard scene with 6 parts avoiding visual overlap."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.A = [
            [4.0, 12.0, -16.0],
            [12.0, 37.0, -43.0],
            [-16.0, -43.0, 98.0],
        ]

        # Precomputed results for stable animation rendering.
        self.L = self.cholesky_decompose(self.A)
        
        # Hardcoded for Part 6 visualization
        self.lambdas = [123.4772, 15.5040, 0.0188]
        self.eigenvectors = [
            [0.1630, 0.4573, -0.8742],
            [-0.2127, -0.8489, -0.4838],
            [0.9635, -0.2648, 0.0411],
        ]

    def construct(self):
        self.part1_roadmap()
        self.part2_intro()
        self.part3_spd_check()
        self.part4_l_calculation()
        self.part5_cost()
        self.part6_diagonalization()

    # ============================
    # Pure list-based math helpers
    # ============================
    def transpose(self, matrix: list[list[float]]) -> list[list[float]]:
        return [list(row) for row in zip(*matrix)]

    def matmul(self, a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
        rows = len(a)
        cols = len(b[0])
        shared = len(b)
        result = [[0.0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for k in range(shared):
                av = a[i][k]
                if av == 0.0:
                    continue
                for j in range(cols):
                    result[i][j] += av * b[k][j]
        return result

    def cholesky_decompose(self, matrix: list[list[float]]) -> list[list[float]]:
        n = len(matrix)
        l = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                if i == j:
                    s = sum(l[i][k] * l[i][k] for k in range(j))
                    l[i][j] = math.sqrt(matrix[i][i] - s)
                else:
                    s = sum(l[i][k] * l[j][k] for k in range(j))
                    l[i][j] = (matrix[i][j] - s) / l[j][j]
        return l

    def fmt(self, value: float) -> str:
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        return f"{value:.4f}"

    def to_manim_str_matrix(self, matrix: list[list[float]]) -> list[list[str]]:
        return [[self.fmt(x) for x in row] for row in matrix]

    def highlight_cell(self, matrix: Matrix, row: int, col: int, color=YELLOW):
        entries = matrix.get_entries()
        n = int(round(math.sqrt(len(entries))))
        idx = (row - 1) * n + (col - 1)
        return SurroundingRectangle(entries[idx], color=color, buff=0.08)

    # ==========================================
    # Part 1: Giới thiệu tổng quan lộ trình
    # ==========================================
    def part1_roadmap(self):
        title = Text("Phân rã Cholesky và Chéo hóa Ma trận", color=YELLOW, font_size=40, weight="BOLD")
        title.to_edge(UP, buff=1.0)

        steps = [
            "1. Giới thiệu bài toán & Khởi tạo ma trận.",
            "2. Kiểm tra điều kiện ma trận SPD.",
            "3. Thuật toán tính toán L (Step-by-step).",
            "4. Ưu điểm về chi phí tính toán.",
            "5. Thuật toán Chéo hóa ma trận."
        ]
        
        step_texts = VGroup(*[Text(step, font_size=28, color=WHITE) for step in steps])
        step_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        step_texts.next_to(title, DOWN, buff=0.8)

        self.play(Write(title))
        
        # Mờ dần xuất hiện từ trên xuống
        self.play(AnimationGroup(*[FadeIn(t, shift=DOWN*0.3) for t in step_texts], lag_ratio=0.3))
        self.wait(1)

        # Highlight mục 1
        box = SurroundingRectangle(step_texts[0], color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(1.5)

        # Dọn dẹp toàn màn hình
        self.clear()

    # ==========================================
    # Part 2: Đặt vấn đề và Định nghĩa
    # ==========================================
    def part2_intro(self):
        matrix_a = Matrix(
            self.to_manim_str_matrix(self.A),
            element_to_mobject=lambda x: MathTex(x),
        ).scale(0.9)
        matrix_a.move_to(UP * 0.5)
        label_a = MathTex("A =", color=ORANGE).next_to(matrix_a, LEFT)
        group_a = VGroup(label_a, matrix_a)

        self.play(FadeIn(group_a))

        question = Text("Làm thế nào để phân rã ma trận A này thành các ma trận tam giác?", font_size=28, color=YELLOW)
        question.next_to(group_a, DOWN, buff=0.8)
        self.play(Write(question))
        self.wait(1.5)

        # Transform câu hỏi thành công thức A = LL^T
        formula = MathTex(r"A = L L^T", color=GREEN).scale(1.5)
        formula.move_to(question.get_center())
        self.play(Transform(question, formula))
        self.wait(1)

        # Dịch chuyển A=LL^T sang trái để nhường chỗ vẽ L
        self.play(
            group_a.animate.scale(0.7).to_corner(UL).shift(DOWN*0.5),
            question.animate.scale(0.8).next_to(group_a, DOWN, buff=0.5, aligned_edge=LEFT)
        )

        # Vẽ ma trận L mô phỏng
        l_template = [
            ["L_{11}", "0", "0"],
            ["L_{21}", "L_{22}", "0"],
            ["L_{31}", "L_{32}", "L_{33}"]
        ]
        matrix_l = Matrix(l_template).scale(0.9)
        matrix_l.move_to(RIGHT * 2)
        
        # Tô màu đỏ các số 0
        entries = matrix_l.get_entries()
        entries[1].set_color(RED)  # row 1 col 2
        entries[2].set_color(RED)  # row 1 col 3
        entries[5].set_color(RED)  # row 2 col 3

        desc = Text("L là ma trận tam giác dưới (nửa trên bằng 0)", font_size=24, color=WHITE)
        desc.next_to(matrix_l, DOWN, buff=0.5)

        self.play(FadeIn(matrix_l), Write(desc))
        self.wait(2)
        self.clear()

    # ==========================================
    # Part 3: Kiểm tra SPD tỉ mỉ
    # ==========================================
    def part3_spd_check(self):
        title = Text("Điều kiện: A phải là ma trận SPD", color=YELLOW, font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        matrix_a = Matrix(self.to_manim_str_matrix(self.A)).scale(0.75)
        matrix_a.move_to(UP * 0.5)
        
        # 3.1 Tính đối xứng
        sym_text = Text("1. Tính đối xứng (Symmetric):", font_size=24, color=WHITE).to_corner(UL).shift(DOWN)
        self.play(Write(sym_text), FadeIn(matrix_a))

        matrix_at = matrix_a.copy().set_color(BLUE).move_to(RIGHT * 3 + UP * 0.5)
        label_at = MathTex("A^T", color=BLUE).next_to(matrix_at, UP)
        self.play(FadeIn(matrix_at), FadeIn(label_at))
        
        # Xoay quanh đường chéo chính (axis=[1, -1, 0])
        self.play(matrix_at.animate.rotate(PI, axis=[1, -1, 0]).move_to(matrix_a.get_center()), run_time=1.5)
        sym_result = MathTex(r"A = A^T", color=GREEN).next_to(matrix_a, DOWN)
        self.play(Write(sym_result))
        self.wait(1)
        
        # Dọn dẹp để qua 3.2
        self.play(FadeOut(sym_text), FadeOut(matrix_at), FadeOut(label_at), FadeOut(sym_result))

        # 3.2 Sylvester
        sylv_text = Text("2. Tiêu chuẩn Sylvester (Leading principal minors > 0)", font_size=24, color=WHITE).to_corner(UL).shift(DOWN)
        self.play(Write(sylv_text))

        # Dịch ma trận A sang trái một chút
        self.play(matrix_a.animate.move_to(LEFT * 3 + UP * 0.5))

        entries = matrix_a.get_entries()
        
        # Delta 1
        box1 = SurroundingRectangle(entries[0], color=RED)
        calc1 = MathTex(r"\Delta_1 = \det([4]) = 4 > 0", color=RED).scale(0.8)
        calc1.move_to(RIGHT * 2 + UP * 1)
        self.play(Create(box1), Write(calc1))
        self.wait(1)

        # Delta 2
        box2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE)
        calc2 = MathTex(r"\Delta_2 = (4 \times 37) - (12 \times 12) = 4 > 0", color=PURPLE).scale(0.8)
        calc2.next_to(calc1, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Transform(box1, box2), Write(calc2))
        self.wait(1)

        # Delta 3 (Chi tiết)
        self.play(FadeOut(calc1), FadeOut(calc2)) # Dọn chỗ
        box3 = SurroundingRectangle(VGroup(*entries), color=YELLOW)
        
        calc3_1 = MathTex(r"\Delta_3 = 4(37 \cdot 98 - (-43)^2) - 12(12 \cdot 98 - (-16)(-43)) - 16(12 \cdot (-43) - 37(-16))", color=YELLOW).scale(0.65)
        calc3_2 = MathTex(r"\Delta_3 = 4(1777) - 12(488) - 16(76)", color=YELLOW).scale(0.7)
        calc3_3 = MathTex(r"\Delta_3 = 7108 - 5856 - 1216 = 36 > 0", color=YELLOW).scale(0.8)

        calc_group = VGroup(calc3_1, calc3_2, calc3_3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        calc_group.move_to(DOWN * 2)

        self.play(Transform(box1, box3))
        self.play(Write(calc3_1))
        self.wait(1)
        self.play(Write(calc3_2))
        self.wait(1)
        self.play(Write(calc3_3))
        self.wait(1)

        # Đóng mộc PASSED
        stamp = Text("PASSED", color=GREEN, font_size=50, weight="BOLD")
        stamp.rotate(15 * PI / 180).move_to(matrix_a.get_center())
        self.play(FadeIn(stamp, scale=2.0))
        self.wait(2)
        
        self.clear()

    # ==========================================
    # Part 4: Tính toán L (Trực quan trái-phải)
    # ==========================================
    def part4_l_calculation(self):
        title = Text("Bước 3: Thuật toán tính toán L", color=YELLOW, font_size=32).to_edge(UP)
        
        # A bên trái, L rỗng bên phải
        matrix_a = Matrix(self.to_manim_str_matrix(self.A)).scale(0.7)
        matrix_a.move_to(LEFT * 3.5 + UP * 1)
        label_a = MathTex("A", color=ORANGE).scale(0.8).next_to(matrix_a, UP)

        l_template = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        matrix_l = Matrix(l_template).scale(0.7)
        matrix_l.move_to(RIGHT * 3.5 + UP * 1)
        label_l = MathTex("L", color=GREEN).scale(0.8).next_to(matrix_l, UP)
        
        # Làm mờ tam giác trên của L
        for i, entry in enumerate(matrix_l.get_entries()):
            if i in [1, 2, 5]: # Các vị trí 0
                entry.set_opacity(0.3)
            else:
                entry.set_opacity(0.0) # Ẩn các ô chờ bay vào

        # Công thức lặp góc dưới trái
        recurrence = VGroup(
            MathTex(r"L_{jj}=\sqrt{A_{jj}-\sum L_{jk}^2}", color=WHITE),
            MathTex(r"L_{ij}=\frac{1}{L_{jj}}(A_{ij}-\sum L_{ik}L_{jk})", color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.55).to_corner(DL).shift(UP*0.5)

        self.play(Write(title), FadeIn(matrix_a), FadeIn(label_a), FadeIn(matrix_l), FadeIn(label_l), Write(recurrence))

        # Hộp công thức ở giữa bên dưới
        steps = [
            {"formula": r"L_{11}=\sqrt{4}=2", "val": "2", "pos": (1,1), "hl": [(1,1)]},
            {"formula": r"L_{21}=12/2=6", "val": "6", "pos": (2,1), "hl": [(2,1), (1,1)]},
            {"formula": r"L_{31}=-16/2=-8", "val": "-8", "pos": (3,1), "hl": [(3,1), (1,1)]},
            {"formula": r"L_{22}=\sqrt{37-6^2}=1", "val": "1", "pos": (2,2), "hl": [(2,2), (2,1)]},
            {"formula": r"L_{32}=\frac{1}{1}(-43-(-8 \times 6))=5", "val": "5", "pos": (3,2), "hl": [(3,2), (3,1), (2,1)]},
            {"formula": r"L_{33}=\sqrt{98-((-8)^2+5^2)}=3", "val": "3", "pos": (3,3), "hl": [(3,3), (3,1), (3,2)]},
        ]

        formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.8).move_to(DOWN * 1.5)
        self.play(Write(formula_box))

        for step in steps:
            # Update công thức
            new_formula = MathTex(step["formula"], color=YELLOW).scale(0.8).move_to(formula_box)
            self.play(Transform(formula_box, new_formula))

            # Highlight A
            hl_boxes = [self.highlight_cell(matrix_a, r, c, ORANGE) for r, c in step["hl"]]
            self.play(*[FadeIn(box) for box in hl_boxes], run_time=0.5)

            # Bay số vào L
            target_entry = matrix_l.get_entries()[(step["pos"][0]-1)*3 + (step["pos"][1]-1)]
            flying_num = MathTex(step["val"], color=GREEN).scale(0.8).move_to(formula_box).shift(UP*0.5)
            
            self.play(FadeIn(flying_num, shift=UP*0.2))
            self.play(flying_num.animate.move_to(target_entry.get_center()), run_time=0.8)
            
            target_entry.become(MathTex(step["val"], color=WHITE).scale(0.7).move_to(target_entry.get_center()))
            target_entry.set_opacity(1.0)
            
            self.play(FadeOut(flying_num), *[FadeOut(box) for box in hl_boxes], run_time=0.3)

        self.wait(2)
        self.clear()

    # ==========================================
    # Part 5: Chi phí tính toán
    # ==========================================
    def part5_cost(self):
        title = Text("Bước 4: Ưu điểm Chi phí tính toán", color=YELLOW, font_size=32).to_edge(UP)
        
        chart = BarChart(
            values=[2.0, 1.0], 
            bar_names=["LU", "Cholesky"],
            y_range=[0, 2.5, 0.5],
            bar_colors=[RED, GREEN],
            y_length=4, x_length=4
        ).move_to(UP * 0.5)

        stats = VGroup(
            MathTex(r"\text{LU} \approx \frac{2}{3}n^3", color=RED),
            MathTex(r"\text{Cholesky} \approx \frac{1}{3}n^3", color=GREEN)
        ).arrange(RIGHT, buff=1.0).next_to(chart, DOWN, buff=0.5)

        conclusion = Text("Tối ưu 50% khối lượng tính toán cho ma trận SPD", font_size=28, color=YELLOW)
        conclusion.next_to(stats, DOWN, buff=0.5)

        self.play(Write(title), FadeIn(chart))
        self.play(Write(stats))
        self.play(Write(conclusion))
        self.wait(2)
        self.clear()

    # ==========================================
    # Part 6: Chéo hóa ma trận tỉ mỉ
    # ==========================================
    def part6_diagonalization(self):
        # 6.1 Giải thích lý thuyết
        title = Text("Bước 5: Chéo hóa Ma trận", color=YELLOW, font_size=32).to_edge(UP)
        formula = MathTex(r"A = P D P^{-1}", color=GREEN).scale(1.5).move_to(UP * 1.5)
        
        desc = Text("Mục tiêu: Tìm ma trận đường chéo D (Trị riêng) và P (Vector riêng)", font_size=24, color=WHITE)
        desc.next_to(formula, DOWN, buff=0.5)

        self.play(Write(title), Write(formula), FadeIn(desc))
        self.wait(2)
        
        # Đẩy lên góc trái
        theory_group = VGroup(formula, desc)
        self.play(theory_group.animate.scale(0.5).to_corner(UL).shift(DOWN*0.5))

        # 6.2 Tìm D
        step_d = Text("1. Tìm ma trận D (Giải PT đặc trưng)", font_size=24, color=BLUE).move_to(LEFT*2.5 + UP*1.5)
        char_eq = MathTex(r"\det(A - \lambda I) = 0", color=WHITE).next_to(step_d, DOWN, aligned_edge=LEFT)
        
        mat_a_lam = Matrix([
            ["4-\\lambda", "12", "-16"],
            ["12", "37-\\lambda", "-43"],
            ["-16", "-43", "98-\\lambda"]
        ]).scale(0.6).next_to(char_eq, DOWN, aligned_edge=LEFT)

        self.play(Write(step_d), Write(char_eq), FadeIn(mat_a_lam))
        
        # Nhấp nháy lambda
        self.play(Indicate(mat_a_lam.get_entries()[0], color=YELLOW), Indicate(mat_a_lam.get_entries()[4], color=YELLOW), Indicate(mat_a_lam.get_entries()[8], color=YELLOW))
        
        lambdas_text = VGroup(
            MathTex(r"\lambda_1 \approx 123.48", color=GREEN),
            MathTex(r"\lambda_2 \approx 15.50", color=GREEN),
            MathTex(r"\lambda_3 \approx 0.02", color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).next_to(mat_a_lam, RIGHT, buff=0.5)
        self.play(FadeIn(lambdas_text))

        # Tạo D bên phải
        mat_d = Matrix([
            ["\\lambda_1", "0", "0"],
            ["0", "\\lambda_2", "0"],
            ["0", "0", "\\lambda_3"]
        ]).scale(0.7).to_edge(RIGHT, buff=1.0).shift(UP*0.5)
        label_d = MathTex("D = ", color=GREEN).scale(0.8).next_to(mat_d, LEFT)
        
        self.play(FadeIn(mat_d), FadeIn(label_d))
        self.wait(1)

        # Dọn phần trái để làm 6.3
        self.play(FadeOut(step_d), FadeOut(char_eq), FadeOut(mat_a_lam), FadeOut(lambdas_text))

        # 6.3 Tìm P (Khử Gauss)
        step_p = Text("2. Tìm ma trận P (Giải hệ phương trình)", font_size=24, color=BLUE).move_to(LEFT*3 + UP*1.5)
        sys_eq = MathTex(r"(A - \lambda_1 I)v_1 = 0", color=WHITE).next_to(step_p, DOWN, aligned_edge=LEFT)
        
        # Hiển thị số cụ thể (hardcode cho đẹp minh họa)
        mat_gauss = Matrix([
            ["-119.48", "12", "-16"],
            ["12", "-86.48", "-43"],
            ["-16", "-43", "-25.48"]
        ]).scale(0.6).next_to(sys_eq, DOWN, aligned_edge=LEFT)
        
        # Đã fix lỗi Unicode LaTeX Khử Gauss
        arrow_symbol = MathTex(r"\longrightarrow").next_to(mat_gauss, RIGHT)
        arrow_text = Text("Khử Gauss", font_size=20, color=WHITE).next_to(arrow_symbol, UP, buff=0.1)
        arrow = VGroup(arrow_symbol, arrow_text)

        v1 = Matrix([["0.16"], ["-0.21"], ["0.96"]]).scale(0.6).next_to(arrow, RIGHT)
        label_v1 = MathTex("v_1=").scale(0.7).next_to(v1, LEFT)

        self.play(Write(step_p), Write(sys_eq))
        self.play(FadeIn(mat_gauss))
        self.play(Write(arrow), FadeIn(v1), FadeIn(label_v1))
        self.wait(1)

        v2 = MathTex(r"v_2 = \begin{bmatrix}0.45\\-0.84\\-0.26\end{bmatrix}").scale(0.6).next_to(v1, DOWN, buff=0.2).align_to(label_v1, LEFT)
        v3 = MathTex(r"v_3 = \begin{bmatrix}-0.87\\-0.48\\0.04\end{bmatrix}").scale(0.6).next_to(v2, DOWN, buff=0.2).align_to(label_v1, LEFT)
        self.play(FadeIn(v2), FadeIn(v3))
        self.wait(1)

        # Dọn dẹp để qua 6.4
        self.play(FadeOut(step_p), FadeOut(sys_eq), FadeOut(mat_gauss), FadeOut(arrow))

        # 6.4 Tổng hợp
        # Gom các vector lại thành P
        p_matrix = Matrix([
            ["0.16", "0.45", "-0.87"],
            ["-0.21", "-0.84", "-0.48"],
            ["0.96", "-0.26", "0.04"]
        ]).scale(0.7).move_to(LEFT * 2 + DOWN * 2)
        label_p = MathTex("P =", color=ORANGE).scale(0.8).next_to(p_matrix, LEFT)

        # Transform các vi rải rác thành P
        self.play(Transform(VGroup(label_v1, v1, v2, v3), VGroup(label_p, p_matrix)))
        
        # Chuyển D xuống ngang hàng
        self.play(VGroup(label_d, mat_d).animate.next_to(p_matrix, RIGHT, buff=0.8))

        # Hiển thị P^-1
        pinv_matrix = MathTex(r"P^{-1}").scale(1.2).next_to(mat_d, RIGHT, buff=0.8)
        self.play(FadeIn(pinv_matrix))

        final = MathTex(r"A = P \times D \times P^{-1}", color=YELLOW).scale(1.2).move_to(DOWN * 3)
        self.play(Write(final))
        self.wait(3)

# ==========================================
# Trình khởi chạy (Launcher)
# ==========================================
DEFAULT_SCENE = "CholeskyAndDiagonalization"

def _run_cmd(cmd: list[str], cwd: Path) -> None:
    completed = subprocess.run(cmd, cwd=str(cwd), check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}")

def _check_runtime_dependencies() -> None:
    required = {
        "latex": "MiKTeX/TexLive latex compiler",
        "dvisvgm": "dvisvgm (usually bundled with MiKTeX)",
        "ffmpeg": "FFmpeg video backend",
    }

    missing = []
    for exe, description in required.items():
        if shutil.which(exe) is None:
            missing.append((exe, description))

    if not missing:
        return

    lines = ["Missing runtime dependencies required by MathTex/Manim:"]
    for exe, description in missing:
        lines.append(f"- {exe}: {description}")
    lines.extend(
        [
            "",
            "Suggested fixes on Windows:",
            "1) Install MiKTeX: winget install --id MiKTeX.MiKTeX --source winget --accept-package-agreements --accept-source-agreements --silent",
            "2) Install FFmpeg: winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent",
            "3) Close and reopen terminal/VS Code so PATH is refreshed.",
            "4) Verify with: where latex, where dvisvgm, where ffmpeg",
        ]
    )
    raise RuntimeError("\n".join(lines))

def _find_latest_scene_video(project_dir: Path, scene_name: str) -> Path:
    root = project_dir / "media" / "videos" / "manim_scene1"
    matches = list(root.glob(f"*/{scene_name}.mp4"))
    if not matches:
        raise FileNotFoundError(f"Rendered scene file not found: {scene_name}")
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0]

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run this file directly to render CholeskyAndDiagonalization scene.",
    )
    parser.add_argument("--scene", default=DEFAULT_SCENE)
    parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="m")
    parser.add_argument("--disable-caching", action="store_true")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    file_name = Path(__file__).name

    _check_runtime_dependencies()

    quality_flag = f"-q{args.quality}"
    cmd = [
        sys.executable,
        "-m",
        "manim",
        quality_flag,
        file_name,
        args.scene,
    ]
    if args.disable_caching:
        cmd.append("--disable_caching")

    print(f"[render] scene={args.scene}, quality={args.quality}")
    _run_cmd(cmd, cwd=project_dir)

    video_path = _find_latest_scene_video(project_dir, args.scene)
    print(f"[done] video: {video_path}")

    # Auto-open video only when running in interactive terminal.
    if os.name == "nt":
        try:
            os.startfile(video_path)  # type: ignore[attr-defined]
        except OSError:
            pass
    return 0

if __name__ == "__main__":
    raise SystemExit(main())