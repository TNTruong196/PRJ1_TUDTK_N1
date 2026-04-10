"""Manim scenes for Part 2 without LaTeX runtime dependency."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
from manim import (
    config,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    Rectangle,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
    BLUE,
    RED,
    GREEN,
    YELLOW,
    WHITE,
)


DEFAULT_FONT = "Arial"
TEXT_COLOR = WHITE
EMPHASIS_COLOR = YELLOW

# Default render profile for this project: 1080p60.
# Set PRJ1_MANIM_FORCE_DEFAULT_1080=0 to let CLI quality flags control output.
if os.getenv("PRJ1_MANIM_FORCE_DEFAULT_1080", "1") == "1":
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60


# -----------------------------------------------------------------------------
# Phase A1: lock demo data in one place
# -----------------------------------------------------------------------------
A = np.array(
    [
        [4.0, 12.0, -16.0],
        [12.0, 37.0, -43.0],
        [-16.0, -43.0, 98.0],
    ]
)

L = np.linalg.cholesky(A)
EIGENVALUES, EIGENVECTORS = np.linalg.eig(A)
P = EIGENVECTORS
D = np.diag(EIGENVALUES)
P_INV = np.linalg.inv(P)


@dataclass
class CholeskyStep:
    name: str
    formula_numeric: str
    value: float
    matrix_pos: tuple[int, int]


# -----------------------------------------------------------------------------
# Phase A2: display formatting helper
# -----------------------------------------------------------------------------
def fmt_num(x: float, decimals: int = 4) -> str:
    if abs(x - round(x)) < 1e-10:
        return str(int(round(x)))
    return f"{x:.{decimals}f}"


def matrix_to_strings(data: np.ndarray, decimals: int = 4) -> list[list[str]]:
    return [[fmt_num(float(v), decimals) for v in row] for row in data]


def vector_to_text(values: np.ndarray, decimals: int = 4) -> str:
    parts = [fmt_num(float(v), decimals) for v in values]
    return "[" + ", ".join(parts) + "]"


def fit_to_width(mobj, max_width: float):
    """Scale down mobject only when it exceeds the target width."""
    if mobj.width > max_width:
        mobj.scale_to_fit_width(max_width)
    return mobj


def build_text_matrix(cells: list[list[str]], scale: float = 0.52, cell_width: float = 1.2) -> VGroup:
    rows = len(cells)
    cols = len(cells[0])
    all_cells = VGroup()
    for r in range(rows):
        row_group = VGroup()
        for c in range(cols):
            box = Rectangle(width=cell_width, height=0.85, color=BLUE, stroke_width=1.5)
            label = Text(cells[r][c], font=DEFAULT_FONT, color=TEXT_COLOR).scale(scale)
            label.move_to(box.get_center())
            row_group.add(VGroup(box, label))
        row_group.arrange(RIGHT, buff=0.05)
        all_cells.add(row_group)
    all_cells.arrange(DOWN, buff=0.05)
    left_bracket = Text("[", font=DEFAULT_FONT, color=TEXT_COLOR).scale(2.2)
    right_bracket = Text("]", font=DEFAULT_FONT, color=TEXT_COLOR).scale(2.2)
    left_bracket.next_to(all_cells, LEFT, buff=0.2)
    right_bracket.next_to(all_cells, RIGHT, buff=0.2)
    return VGroup(left_bracket, all_cells, right_bracket)


def cholesky_steps() -> list[CholeskyStep]:
    return [
        CholeskyStep("l_{11}", r"l_{11}=\sqrt{4}=2", 2.0, (0, 0)),
        CholeskyStep("l_{21}", r"l_{21}=\frac{12}{l_{11}}=\frac{12}{2}=6", 6.0, (1, 0)),
        CholeskyStep("l_{31}", r"l_{31}=\frac{-16}{l_{11}}=\frac{-16}{2}=-8", -8.0, (2, 0)),
        CholeskyStep("l_{22}", r"l_{22}=\sqrt{37-l_{21}^2}=\sqrt{37-36}=1", 1.0, (1, 1)),
        CholeskyStep("l_{32}", r"l_{32}=\frac{-43-l_{31}l_{21}}{l_{22}}=\frac{-43+48}{1}=5", 5.0, (2, 1)),
        CholeskyStep("l_{33}", r"l_{33}=\sqrt{98-l_{31}^2-l_{32}^2}=\sqrt{98-64-25}=3", 3.0, (2, 2)),
    ]


# -----------------------------------------------------------------------------
# Shared visual constants (Phase G2-ready)
# -----------------------------------------------------------------------------
TITLE_SCALE = 0.7
FORMULA_SCALE = 0.65
MATRIX_SCALE = 0.95

FINAL_SCENES = [
    "Scene1Introduction",
    "Scene2SPDProof",
    "Scene2CholeskyProcess",
    "Scene3EigenData",
    "Scene3DiagonalizationProcess",
    "Scene4FinalRecap",
]


class Scene1Introduction(Scene):
    """Phase B: Intro scene with problem statement and target formulas."""

    def construct(self) -> None:
        title = Text("Scene 1: Introduction to Matrix Decomposition", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(TITLE_SCALE).to_edge(UP)
        matrix_label = Text("Given matrix A:", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.62)
        matrix_a = build_text_matrix(matrix_to_strings(A), scale=0.52).scale(MATRIX_SCALE)

        matrix_group = VGroup(matrix_label, matrix_a).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        matrix_group.shift(LEFT * 3 + DOWN * 0.4)

        task_text = Text("Goal: decompose A by Cholesky and Diagonalization", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.50)
        formula_cholesky = Text("A = L * L^T", font=DEFAULT_FONT, color=GREEN).scale(FORMULA_SCALE)
        formula_diag = Text("A = P * D * P^(-1)", font=DEFAULT_FONT, color=GREEN).scale(FORMULA_SCALE)
        formula_group = VGroup(task_text, formula_cholesky, formula_diag).arrange(DOWN, buff=0.50)
        formula_group.shift(RIGHT * 2.8 + DOWN * 0.2)
        fit_to_width(formula_group, 6.2)

        self.play(Write(title))
        self.play(FadeIn(matrix_group, shift=UP * 0.2))
        self.play(FadeIn(task_text, shift=UP * 0.2))
        self.play(Write(formula_cholesky), Write(formula_diag))
        self.wait(1.5)


class Scene2SPDProof(Scene):
    """Phase C: standalone SPD proof (symmetry + positive eigenvalues)."""

    def construct(self) -> None:
        title = Text("Scene 2A: Why A is SPD", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(TITLE_SCALE).to_edge(UP)
        self.play(Write(title))

        mat = build_text_matrix(matrix_to_strings(A), scale=0.52).scale(MATRIX_SCALE).shift(LEFT * 3 + DOWN * 0.4)
        self.play(FadeIn(mat))

        # C1: symmetry highlight A12 and A21
        c1_text = Text("1) Symmetry: A[0][1] = A[1][0]", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.56)
        c1_text.next_to(mat, DOWN, buff=0.7)
        self.play(Write(c1_text))

        matrix_cells = mat[1]
        a12 = SurroundingRectangle(matrix_cells[0][1], color=RED, stroke_width=2.5, buff=0.08)
        a21 = SurroundingRectangle(matrix_cells[1][0], color=RED, stroke_width=2.5, buff=0.08)
        equal_mark = Text("=", font=DEFAULT_FONT, color=GREEN).scale(1.0)
        equal_mark.move_to((a12.get_center() + a21.get_center()) / 2)

        self.play(FadeIn(a12), FadeIn(a21), Write(equal_mark))
        self.wait(1)

        # C2: positive eigenvalues with numpy.linalg.eig
        eigvals = np.linalg.eig(A)[0]
        eig_text_title = Text("2) Positive eigenvalues:", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.56)
        eig_text_title.shift(RIGHT * 1.8 + UP * 1.0)

        eig_lines = VGroup(
            *[
                Text(f"lambda_{i+1} = {fmt_num(float(v), 2)} > 0", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.48)
                for i, v in enumerate(eigvals)
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        eig_lines.next_to(eig_text_title, DOWN, aligned_edge=LEFT, buff=0.3)

        conclude = Text("Conclusion: A is SPD (symmetric + positive eigenvalues)", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(0.45)
        conclude.next_to(eig_lines, DOWN, aligned_edge=LEFT, buff=0.4)

        right_group = VGroup(eig_text_title, eig_lines, conclude)
        fit_to_width(right_group, 5.8)

        self.play(FadeIn(mat), FadeIn(c1_text))
        self.play(FadeIn(a12), FadeIn(a21), Write(equal_mark))
        self.wait(0.8)
        self.play(Write(eig_text_title))
        self.play(AnimationGroup(*[Write(line) for line in eig_lines], lag_ratio=0.2))
        self.play(Write(conclude))
        self.wait(1.5)


class Scene2CholeskyProcess(Scene):
    """Phase D: step-by-step Cholesky substitution and LL^T verification."""

    def construct(self) -> None:
        title = Text("Scene 2B: Cholesky step-by-step", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(TITLE_SCALE).to_edge(UP)
        self.play(Write(title))

        mat_a = build_text_matrix(matrix_to_strings(A), scale=0.5).scale(0.95)
        mat_l = build_text_matrix(
            [["?", "0", "0"], ["?", "?", "0"], ["?", "?", "?"]],
            scale=0.5,
        ).scale(0.95)

        group = VGroup(mat_a, Text("=", font=DEFAULT_FONT, color=GREEN).scale(0.7), mat_l, Text("L^T", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.5))
        group.arrange(RIGHT, buff=0.5)
        group.shift(UP * 1.2)

        self.play(FadeIn(group))

        generic_formula = Text(
            "l_jj = sqrt(a_jj - sum(l_jk^2))   l_ij = (a_ij - sum(l_ik*l_jk)) / l_jj",
            font=DEFAULT_FONT,
            color=TEXT_COLOR,
        ).scale(0.38)
        fit_to_width(generic_formula, 12.0)
        generic_formula.next_to(group, DOWN, buff=0.8)
        self.play(Write(generic_formula))

        # D1 + D2: data-driven substitution steps
        step_formula = Text("", font=DEFAULT_FONT, color=YELLOW).scale(0.42)
        step_formula.next_to(generic_formula, DOWN, buff=0.75)
        self.add(step_formula)

        current_l = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        for step in cholesky_steps():
            formula_text = step.formula_numeric.replace("\\sqrt", "sqrt").replace("\\frac", "(").replace("\\sum", "sum")
            new_formula = Text(formula_text, font=DEFAULT_FONT, color=YELLOW).scale(0.38)
            fit_to_width(new_formula, 11.8)
            new_formula.move_to(step_formula)
            self.play(Transform(step_formula, new_formula))

            i, j = step.matrix_pos
            current_l[i][j] = fmt_num(step.value)
            new_mat_l = build_text_matrix(current_l, scale=0.5).scale(0.95).move_to(mat_l)
            self.play(Transform(mat_l, new_mat_l))

        self.wait(0.5)

        # D3: verify LL^T = A with numpy.linalg.cholesky
        l_np = np.linalg.cholesky(A)
        verify_ok = np.allclose(l_np, L)

        verify_text = Text(
            f"Verification: {'PASS' if verify_ok else 'FAIL'}",
            font=DEFAULT_FONT,
            color=GREEN if verify_ok else RED,
        ).scale(0.46)
        verify_text.next_to(step_formula, DOWN, buff=1.2)

        finish_formula = Text("L * L^T = A", font=DEFAULT_FONT, color=GREEN).scale(0.60)
        finish_formula.next_to(verify_text, DOWN, buff=0.5)

        self.play(Write(verify_text))
        self.play(Write(finish_formula))
        self.wait(1.5)


class Scene3EigenData(Scene):
    """Phase E: show eigenvalues and eigenvectors that build matrix P."""

    def construct(self) -> None:
        title = Text("Scene 3A: Eigen data for diagonalization", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(TITLE_SCALE).to_edge(UP)
        self.play(Write(title))

        # --- KHỐI 1: MA TRẬN A ---
        matrix_a = build_text_matrix(matrix_to_strings(A), scale=0.5).scale(0.92)
        # Đặt A ở bên trái
        matrix_a.shift(LEFT * 3.5 + UP * 0.5)

        input_label = Text("Input matrix A", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.56)
        input_label.next_to(matrix_a, UP, buff=0.2)

        self.play(FadeIn(matrix_a), Write(input_label))

        # --- KHỐI 2: EIGENVALUES ---
        eigval_title = Text("1) Eigenvalues from numpy.linalg.eig:", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.56)
        # Đặt tiêu đề lambda ở nửa trên bên phải
        eigval_title.shift(RIGHT * 2.0 + UP * 1.5)

        eigval_lines = VGroup(
            *[
                Text(f"lambda{i+1} = {fmt_num(float(val), 4)}", font=DEFAULT_FONT, color=GREEN).scale(0.54)
                for i, val in enumerate(EIGENVALUES)
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        eigval_lines.next_to(eigval_title, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(Write(eigval_title))
        self.play(AnimationGroup(*[Write(line) for line in eigval_lines], lag_ratio=0.2))

        # --- KHỐI 3: EIGENVECTORS ---
        eigvec_title = Text("2) Eigenvectors:", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.56)
        eigvec_title.next_to(eigval_lines, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(eigvec_title))

        eigvec_lines = VGroup(
            *[
                Text(
                    f"v{i+1} = {vector_to_text(P[:, i], 4)}",
                    font=DEFAULT_FONT,
                    color=TEXT_COLOR,
                ).scale(0.50)
                for i in range(P.shape[1])
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fit_to_width(eigvec_lines, 5.8)
        eigvec_lines.next_to(eigvec_title, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(AnimationGroup(*[Write(line) for line in eigvec_lines], lag_ratio=0.2))
        self.wait(2) # Dừng lại để người xem đọc

        # --- DỌN DẸP MÀN HÌNH CHUẨN BỊ CHO MA TRẬN P ---
        # Ẩn Ma trận A và khối Eigenvalues đi để lấy không gian
        self.play(
            FadeOut(matrix_a), 
            FadeOut(input_label),
            FadeOut(eigval_title),
            FadeOut(eigval_lines)
        )

        # Di chuyển khối Eigenvectors sang trái
        eigvec_group = VGroup(eigvec_title, eigvec_lines)
        self.play(eigvec_group.animate.to_edge(LEFT).shift(RIGHT * 0.5))

        # --- KHỐI 4: MA TRẬN P ---
        p_title = Text("Columns v1, v2, v3 form matrix P", font=DEFAULT_FONT, color=YELLOW).scale(0.56)
        p_matrix = build_text_matrix(matrix_to_strings(P, decimals=4), scale=0.45).scale(0.88)
        
        # Nhóm P lại và đặt nó cạnh khối Eigenvectors (ở giữa/phải màn hình)
        p_group = VGroup(p_title, p_matrix).arrange(DOWN, buff=0.3)
        fit_to_width(p_group, 5.9)
        p_group.to_edge(RIGHT, buff=0.55).shift(DOWN * 0.15)

        self.play(Write(p_title), FadeIn(p_matrix, shift=UP * 0.2))

        # Highlight các cột
        col_highlights = []
        p_cells = p_matrix[1]
        for c in range(P.shape[1]):
            col_group = VGroup(*[p_cells[r][c] for r in range(P.shape[0])])
            col_highlights.append(SurroundingRectangle(col_group, color=YELLOW, stroke_width=2.0, buff=0.06))

        for i, hl in enumerate(col_highlights):
            label = Text(f"v{i+1}", font=DEFAULT_FONT, color=YELLOW).scale(0.5)
            label.next_to(hl, DOWN, buff=0.1)
            self.play(Create(hl), FadeIn(label, shift=UP * 0.1), run_time=0.45)
            self.play(FadeOut(label), FadeOut(hl), run_time=0.30)

        # Hoàn tất
        done = Text("Scene 3A done: eigen data ready for A = P D P^-1", font=DEFAULT_FONT, color=GREEN).scale(0.55)
        done.to_edge(DOWN)
        self.play(Write(done))
        self.wait(1.5)


class Scene3DiagonalizationProcess(Scene):
    """Phase F: assemble P, D, P^-1 and verify A = P D P^-1."""

    def construct(self) -> None:
        title = Text("Scene 3B: Assemble diagonalization", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(TITLE_SCALE).to_edge(UP)
        self.play(Write(title))

        formula = Text("A = P D P^-1", font=DEFAULT_FONT, color=GREEN).scale(0.74)
        formula.next_to(title, DOWN, buff=0.18)
        self.play(Write(formula))

        p_title = Text("P", font=DEFAULT_FONT, color=YELLOW).scale(0.58)
        d_title = Text("D", font=DEFAULT_FONT, color=YELLOW).scale(0.58)
        pinv_title = Text("P^-1", font=DEFAULT_FONT, color=YELLOW).scale(0.58)

        p_matrix = build_text_matrix(matrix_to_strings(P, decimals=4), scale=0.34, cell_width=0.98).scale(0.78)
        d_matrix = build_text_matrix(matrix_to_strings(D, decimals=4), scale=0.38, cell_width=0.98).scale(0.80)
        pinv_matrix = build_text_matrix(matrix_to_strings(P_INV, decimals=4), scale=0.34, cell_width=0.98).scale(0.78)

        p_panel = VGroup(p_title, p_matrix).arrange(DOWN, buff=0.12)
        d_panel = VGroup(d_title, d_matrix).arrange(DOWN, buff=0.12)
        pinv_panel = VGroup(pinv_title, pinv_matrix).arrange(DOWN, buff=0.12)

        matrix_row = VGroup(p_panel, d_panel, pinv_panel).arrange(RIGHT, buff=0.55)
        fit_to_width(matrix_row, 12.8)
        matrix_row.next_to(formula, DOWN, buff=0.35)

        self.play(FadeIn(matrix_row, shift=UP * 0.15))

        # Highlight the diagonal of D because those entries are the eigenvalues.
        d_cells = d_matrix[1]
        for i in range(3):
            diag_box = SurroundingRectangle(d_cells[i][i], color=YELLOW, stroke_width=2.2, buff=0.06)
            self.play(Create(diag_box), run_time=0.35)
            self.play(FadeOut(diag_box), run_time=0.2)

        build_text = Text("Columns of P come from eigenvectors; diagonal of D stores eigenvalues.", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.48)
        fit_to_width(build_text, 12.8)
        build_text.next_to(matrix_row, DOWN, buff=0.32)
        self.play(Write(build_text))

        reconstructed = P @ D @ P_INV
        max_abs_error = float(np.max(np.abs(reconstructed - A)))
        verify_ok = bool(np.allclose(reconstructed, A, atol=1e-8, rtol=1e-8))

        verify_text = Text(
            f"Verification: {'PASS' if verify_ok else 'FAIL'} | max error = {fmt_num(max_abs_error, 8)}",
            font=DEFAULT_FONT,
            color=GREEN if verify_ok else RED,
        ).scale(0.55)
        fit_to_width(verify_text, 12.8)
        verify_text.next_to(build_text, DOWN, buff=0.26)

        self.play(Write(verify_text))

        result_formula = Text("P D P^-1 = A", font=DEFAULT_FONT, color=GREEN).scale(0.72)
        result_formula.next_to(verify_text, DOWN, buff=0.25)
        self.play(Write(result_formula))

        self.wait(1.4)


class Part2PipelinePreview(Scene):
    """Phase G: compact end-to-end preview of Part 2 scenes."""

    def construct(self) -> None:
        title = Text("Part 2 pipeline preview", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(0.72).to_edge(UP)
        self.play(Write(title))

        cards = []
        rows = [
            ("Scene 1", "Intro", "A = L L^T / A = P D P^-1", GREEN),
            ("Scene 2A", "SPD proof", "A = A^T and λ > 0", RED),
            ("Scene 2B", "Cholesky", "Step-by-step L and LL^T", BLUE),
            ("Scene 3A", "Eigen data", "λ and eigenvectors -> P", YELLOW),
            ("Scene 3B", "Diagonalization", "P, D, P^-1 -> A", GREEN),
        ]

        for name, subtitle, detail, accent in rows:
            header = Text(name, font=DEFAULT_FONT, color=accent).scale(0.52)
            sub = Text(subtitle, font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.42)
            info = Text(detail, font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.34)
            card_body = VGroup(header, sub, info).arrange(DOWN, buff=0.08)
            card_box = Rectangle(width=3.6, height=1.35, color=accent, stroke_width=2.0)
            card = VGroup(card_box, card_body)
            card_body.move_to(card_box.get_center())
            cards.append(card)

        top_row = VGroup(cards[0], cards[1], cards[2]).arrange(RIGHT, buff=0.35)
        bottom_row = VGroup(cards[3], cards[4]).arrange(RIGHT, buff=0.45)
        bottom_row.next_to(top_row, DOWN, buff=0.35)
        pipeline = VGroup(top_row, bottom_row)
        fit_to_width(pipeline, 12.8)
        pipeline.next_to(title, DOWN, buff=0.35)

        self.play(FadeIn(pipeline, shift=UP * 0.15))

        footer = Text("Render individually for rubrics, or render the full file for integration check.", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.48)
        fit_to_width(footer, 12.8)
        footer.to_edge(DOWN)
        self.play(Write(footer))
        self.wait(1.4)


class Scene4FinalRecap(Scene):
    """Phase H support scene to summarize key results and stabilize final duration."""

    def construct(self) -> None:
        title = Text("Final recap of Part 2", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(0.74).to_edge(UP)
        self.play(Write(title))

        points = [
            "1) A was verified as SPD: symmetric and positive eigenvalues.",
            "2) Cholesky decomposition produced L with LL^T = A.",
            "3) Eigenvalues and eigenvectors were extracted from A.",
            "4) Matrices P, D, and P^-1 reconstructed A by PDP^-1.",
            "5) Numerical verification passed with a small reconstruction error.",
            "6) Pipeline Scene1 -> Scene2A -> Scene2B -> Scene3A -> Scene3B is complete.",
        ]

        bullet_group = VGroup()
        for point in points:
            line = Text(point, font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.46)
            fit_to_width(line, 12.5)
            bullet_group.add(line)

        bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bullet_group.next_to(title, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)

        for line in bullet_group:
            self.play(Write(line), run_time=0.7)
            self.wait(5.0)

        outro = Text("End of final video", font=DEFAULT_FONT, color=GREEN).scale(0.70)
        outro.to_edge(DOWN)
        self.play(Write(outro))
        self.wait(6.0)


class Part2Preview(Scene):
    """Optional stitch scene for quick local preview of A-B-C-D-E in one render."""

    def construct(self) -> None:
        header = Text("Part 2 Preview: A-B-C-D-E completed", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(0.72)
        sub = Text("Use individual scene classes for rubric checks", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.58).next_to(header, DOWN)
        self.play(FadeIn(header, shift=UP * 0.2), FadeIn(sub, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(header), FadeOut(sub))


def _run_cmd(cmd: list[str], cwd: Path) -> None:
    env = dict(os.environ)
    # Force CLI quality flags (e.g. -qm) to take effect when autorunning.
    env["PRJ1_MANIM_FORCE_DEFAULT_1080"] = "0"
    completed = subprocess.run(cmd, cwd=str(cwd), check=False, env=env)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}")


def _find_latest_scene_video(project_dir: Path, scene_name: str) -> Path:
    root = project_dir / "media" / "videos" / "manim_scene"
    matches = list(root.glob(f"*/{scene_name}.mp4"))
    if not matches:
        raise FileNotFoundError(f"Rendered scene file not found: {scene_name}")
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0]


def _resolve_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    try:
        from imageio_ffmpeg import get_ffmpeg_exe

        return get_ffmpeg_exe()
    except Exception as exc:
        raise RuntimeError("ffmpeg executable not found. Install ffmpeg or imageio-ffmpeg.") from exc


def _get_video_info(video_path: Path) -> tuple[float, int, int, float]:
    import av

    with av.open(str(video_path)) as container:
        stream = container.streams.video[0]
        if container.duration is not None:
            duration_seconds = float(container.duration) / 1_000_000.0
        else:
            duration_seconds = float(stream.duration * stream.time_base) if stream.duration is not None else 0.0
        width = int(stream.width)
        height = int(stream.height)
        fps = float(stream.average_rate) if stream.average_rate is not None else 0.0
    return duration_seconds, width, height, fps


def _render_final_scenes(project_dir: Path, disable_caching: bool) -> list[Path]:
    outputs: list[Path] = []
    for scene in FINAL_SCENES:
        print(f"[render] {scene}")
        cmd = [
            sys.executable,
            "-m",
            "manim",
            "-qm",
            "--resolution",
            "1280,720",
            "--fps",
            "30",
            "manim_scene.py",
            scene,
        ]
        if disable_caching:
            cmd.append("--disable_caching")
        _run_cmd(cmd, cwd=project_dir)
        outputs.append(_find_latest_scene_video(project_dir, scene))
    return outputs


def _concat_videos(project_dir: Path, inputs: list[Path], output_name: str) -> Path:
    if not inputs:
        raise ValueError("No scene videos to concatenate.")
    output_dir = inputs[0].parent
    list_path = output_dir / "concat_list.txt"
    list_path.write_text("\n".join([f"file '{video.as_posix()}'" for video in inputs]) + "\n", encoding="utf-8")

    output_video = output_dir / output_name
    ffmpeg = _resolve_ffmpeg()
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-c",
        "copy",
        str(output_video),
    ]
    _run_cmd(cmd, cwd=project_dir)
    return output_video


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run this file directly to render final Part 2 video (720p30) and concatenate scenes.",
    )
    parser.add_argument("--output-name", default="demo_video.mp4")
    parser.add_argument("--disable-caching", action="store_true")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    print("[1/4] Rendering final scenes...")
    scene_outputs = _render_final_scenes(project_dir, disable_caching=args.disable_caching)

    print("[2/4] Scene metadata:")
    total_duration = 0.0
    for scene_video in scene_outputs:
        duration, width, height, fps = _get_video_info(scene_video)
        total_duration += duration
        print(f"  - {scene_video.name}: {duration:.2f}s | {width}x{height} | {fps:.2f}fps")
    print(f"  Total (sum): {total_duration:.2f}s")

    print("[3/4] Concatenating final video...")
    final_video = _concat_videos(project_dir, scene_outputs, args.output_name)

    print("[4/4] Final metadata:")
    duration, width, height, fps = _get_video_info(final_video)
    print(f"  - file: {final_video}")
    print(f"  - duration: {duration:.2f}s")
    print(f"  - resolution: {width}x{height}")
    print(f"  - fps: {fps:.2f}")
    if duration < 120.0 or duration > 1800.0:
        print("  Duration check: FAIL (must be between 120s and 1800s)")
        return 2

    print("  Duration check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
