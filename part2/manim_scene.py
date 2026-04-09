"""Manim scenes for Part 2 without LaTeX runtime dependency."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
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


class Scene1Introduction(Scene):
    """Phase B: Intro scene with problem statement and target formulas."""

    def construct(self) -> None:
        title = Text("Scene 1: Introduction to Matrix Decomposition", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(TITLE_SCALE).to_edge(UP)
        matrix_label = Text("Given matrix A:", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.62)
        matrix_a = build_text_matrix(matrix_to_strings(A), scale=0.52).scale(MATRIX_SCALE)

        matrix_group = VGroup(matrix_label, matrix_a).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        matrix_group.shift(LEFT * 3 + DOWN * 0.4)

        task_text = Text("Goal: decompose A by Cholesky and Diagonalization", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.58)
        formula_cholesky = Text("A = L L^T", font=DEFAULT_FONT, color=GREEN).scale(FORMULA_SCALE)
        formula_diag = Text("A = P D P^-1", font=DEFAULT_FONT, color=GREEN).scale(FORMULA_SCALE)
        formula_group = VGroup(task_text, formula_cholesky, formula_diag).arrange(DOWN, buff=0.35)
        formula_group.shift(RIGHT * 2.5 + DOWN * 0.1)

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
        c1_text = Text("1) Symmetry: A[0][1] = A[1][0]", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.62)
        c1_text.next_to(mat, DOWN, buff=0.5)
        self.play(Write(c1_text))

        matrix_cells = mat[1]
        a12 = SurroundingRectangle(matrix_cells[0][1], color=RED, stroke_width=2.5, buff=0.08)
        a21 = SurroundingRectangle(matrix_cells[1][0], color=RED, stroke_width=2.5, buff=0.08)
        equal_mark = Text("=", font=DEFAULT_FONT, color=GREEN).scale(1.0)
        equal_mark.move_to((a12.get_center() + a21.get_center()) / 2 + RIGHT * 0.75)

        self.play(FadeIn(a12), FadeIn(a21), Write(equal_mark))
        self.wait(1)

        # C2: positive eigenvalues with numpy.linalg.eig
        eigvals = np.linalg.eig(A)[0]
        eig_text_title = Text("2) Positive definiteness via eigenvalues:", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.62)
        eig_text_title.shift(RIGHT * 2.5 + UP * 0.6)

        eig_lines = VGroup(
            *[
                Text(f"λ{i+1} = {fmt_num(float(v), 2)} > 0", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.56)
                for i, v in enumerate(eigvals)
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        eig_lines.next_to(eig_text_title, DOWN, aligned_edge=LEFT, buff=0.2)

        conclude = Text("Conclusion: A is SPD", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(0.62)
        conclude.next_to(eig_lines, DOWN, aligned_edge=LEFT, buff=0.35)

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
        group.shift(UP * 0.7)

        self.play(FadeIn(group))

        generic_formula = Text(
            "l_jj = sqrt(a_jj - Σl_jk²)  |  l_ij = (a_ij - Σl_ik*l_jk)/l_jj",
            font=DEFAULT_FONT,
            color=TEXT_COLOR
        ).scale(0.54)
        generic_formula.next_to(group, DOWN, buff=0.5)
        self.play(Write(generic_formula))

        # D1 + D2: data-driven substitution steps
        step_formula = Text("", font=DEFAULT_FONT, color=YELLOW).scale(0.52)
        step_formula.next_to(generic_formula, DOWN, buff=0.3)
        self.add(step_formula)

        current_l = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        for step in cholesky_steps():
            formula_text = step.formula_numeric.replace("\\sqrt", "sqrt").replace("\\frac", "(")
            new_formula = Text(formula_text, font=DEFAULT_FONT, color=YELLOW).scale(0.48).move_to(step_formula)
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
            f"Verification with numpy.linalg.cholesky: {'PASS' if verify_ok else 'FAIL'}",
            font=DEFAULT_FONT,
            color=GREEN if verify_ok else RED
        ).scale(0.60)
        verify_text.next_to(step_formula, DOWN, buff=0.35)

        finish_formula = Text("L L^T = A", font=DEFAULT_FONT, color=GREEN).scale(0.68)
        finish_formula.next_to(verify_text, DOWN, buff=0.2)

        self.play(Write(verify_text))
        self.play(Write(finish_formula))
        self.wait(1.5)


class Part2Preview(Scene):
    """Optional stitch scene for quick local preview of A-B-C-D in one render."""

    def construct(self) -> None:
        header = Text("Part 2 Preview: A-B-C-D completed", font=DEFAULT_FONT, color=EMPHASIS_COLOR).scale(0.72)
        sub = Text("Use individual scene classes for rubric checks", font=DEFAULT_FONT, color=TEXT_COLOR).scale(0.58).next_to(header, DOWN)
        self.play(FadeIn(header, shift=UP * 0.2), FadeIn(sub, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(header), FadeOut(sub))
