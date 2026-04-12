"""Manim visualization for Cholesky decomposition and diagonalization.

This file follows the project constraints:
- Core matrix computations are implemented with pure Python list-of-lists.
- numpy is used only for verification at the end of scenes.
- The presentation is split into independent scenes for modular rendering.
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup,
    Arrow,
    BLUE,
    BarChart,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    Indicate,
    LEFT,
    MathTex,
    Matrix,
    ORANGE,
    PI,
    PURPLE,
    RED,
    RIGHT,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    TransformFromCopy,
    UP,
    UL,
    VGroup,
    WHITE,
    YELLOW,
    Write,
)


class BaseMathScene(Scene):
    TIME_FAST = 1.0
    TIME_NORMAL = 1.5
    TIME_SLOW = 2.5
    WAIT_SHORT = 2.0
    WAIT_LONG = 4.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.A = [
            [4.0, 12.0, -16.0],
            [12.0, 37.0, -43.0],
            [-16.0, -43.0, 98.0],
        ]
        self.L = self.cholesky_decompose(self.A)
        self.lambdas = [123.4772, 15.5040, 0.0188]
        self.eigenvectors = [
            [0.1630, 0.4573, -0.8742],
            [-0.2127, -0.8489, -0.4838],
            [0.9635, -0.2648, 0.0411],
        ]
        self.P = self.eigenvectors
        self.P_inv = self.transpose(self.P)
        self.D = [
            [self.lambdas[0], 0.0, 0.0],
            [0.0, self.lambdas[1], 0.0],
            [0.0, 0.0, self.lambdas[2]],
        ]

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
        return [[self.fmt(value) for value in row] for row in matrix]

    def highlight_cell(self, matrix: Matrix, row: int, col: int, color=YELLOW):
        entries = matrix.get_entries()
        n = int(round(math.sqrt(len(entries))))
        index = (row - 1) * n + (col - 1)
        return SurroundingRectangle(entries[index], color=color, buff=0.08)

    def make_labeled_matrix(
        self,
        values: list[list[str]],
        label: str,
        label_color,
        scale: float = 0.8,
        h_buff: float | None = None,
    ) -> VGroup:
        kwargs = {}
        if h_buff is not None:
            kwargs["h_buff"] = h_buff
        matrix = Matrix(values, **kwargs).scale(scale)
        label_mob = MathTex(label, color=label_color).scale(scale).next_to(matrix, LEFT)
        return VGroup(label_mob, matrix)

    def make_section_title(self, text: str, color=YELLOW, font_size: int = 32):
        return Text(text, color=color, font_size=font_size, weight="BOLD")

    def _make_roadmap_card(
        self,
        header_text: str,
        steps: list[str],
        accent_color,
        width: float = 6.2,
    ) -> tuple[VGroup, dict[str, Text]]:
        header = Text(header_text, color=accent_color, font_size=24, weight="BOLD")
        step_mobjects = [Text(step, color=WHITE, font_size=22) for step in steps]
        content = VGroup(header, *step_mobjects).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        frame = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=content.height + 0.7,
            stroke_color=accent_color,
            stroke_width=2.5,
            fill_color="#0b0f17",
            fill_opacity=0.75,
        ).move_to(content)
        card = VGroup(frame, content)
        step_map = {step: mob for step, mob in zip(steps, step_mobjects)}
        return card, step_map

    def show_transition_roadmap(self, part_index: int, step_name: str):
        self.clear()

        title = Text(
            "Phân rã Cholesky và Chéo hóa ma trận",
            color=YELLOW,
            font_size=40,
            weight="BOLD",
        ).to_edge(UP, buff=0.35)

        part1_card, part1_steps = self._make_roadmap_card(
            "PHẦN I: PHÂN RÃ CHOLESKY",
            [
                "1.1. Bài toán & Điều kiện",
                "1.2. Kiểm tra tính chất SPD",
                "1.3. Tính toán ma trận L",
                "1.4. Đánh giá chi phí",
            ],
            GREEN,
        )
        part2_card, part2_steps = self._make_roadmap_card(
            "PHẦN II: CHÉO HÓA MA TRẬN",
            [
                "2.1. Giới thiệu Bài toán",
                "2.2. Thuật toán Chéo hóa (Tìm D, P)",
            ],
            BLUE,
        )

        cards = VGroup(part1_card, part2_card).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.05)

        self.play(Write(title), run_time=self.TIME_NORMAL)
        self.play(FadeIn(cards, shift=UP * 0.15), run_time=self.TIME_NORMAL)

        active_card = part1_card if part_index == 1 else part2_card
        active_color = GREEN if part_index == 1 else BLUE
        step_lookup = part1_steps if part_index == 1 else part2_steps
        active_step = step_lookup.get(step_name)
        if active_step is None:
            active_step = next(iter(step_lookup.values()))

        card_box = SurroundingRectangle(active_card, color=active_color, buff=0.12)
        step_box = SurroundingRectangle(active_step, color=YELLOW, buff=0.1)

        self.play(Create(card_box), Create(step_box), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        self.play(FadeOut(title), FadeOut(cards), FadeOut(card_box), FadeOut(step_box), run_time=self.TIME_FAST)


# class Scene0_Overview(BaseMathScene):
#     def construct(self):
#         title = Text("Bài toán Phân tích Ma trận", color=YELLOW, font_size=40, weight="BOLD")
#         title.to_edge(UP, buff=0.6)

#         matrix_a = Matrix(
#             self.to_manim_str_matrix(self.A),
#             element_to_mobject=lambda value: MathTex(value),
#         ).scale(0.95)
#         label_a = MathTex("A =", color=ORANGE).next_to(matrix_a, LEFT)
#         center_group = VGroup(label_a, matrix_a).move_to(UP * 0.2)

#         left_panel = self._overview_branch_panel("Phần 1: A = LL^T", "Xanh lá", GREEN)
#         right_panel = self._overview_branch_panel("Phần 2: A = PDP^{-1}", "Xanh dương", BLUE)
#         left_panel.move_to(LEFT * 3.2 + DOWN * 1.9)
#         right_panel.move_to(RIGHT * 3.2 + DOWN * 1.9)

#         left_arrow = Arrow(center_group.get_bottom(), left_panel.get_top(), buff=0.15, color=GREEN)
#         right_arrow = Arrow(center_group.get_bottom(), right_panel.get_top(), buff=0.15, color=BLUE)

#         self.play(Write(title), FadeIn(center_group), run_time=self.TIME_NORMAL)
#         self.play(
#             AnimationGroup(
#                 Create(left_arrow),
#                 Create(right_arrow),
#                 FadeIn(left_panel, shift=UP * 0.15),
#                 FadeIn(right_panel, shift=UP * 0.15),
#                 lag_ratio=0.15,
#             ),
#             run_time=self.TIME_NORMAL,
#         )
#         self.wait(self.WAIT_SHORT)

#         self.play(
#             center_group.animate.scale(0.72).to_corner(UL, buff=0.7),
#             FadeOut(left_panel),
#             FadeOut(right_panel),
#             FadeOut(left_arrow),
#             FadeOut(right_arrow),
#             FadeOut(title),
#             run_time=self.TIME_NORMAL,
#         )
#         self.wait(self.TIME_FAST)
#         self.clear()

#     def _overview_branch_panel(self, headline: str, body: str, accent_color) -> VGroup:
#         headline_text = Text(headline, color=accent_color, font_size=24, weight="BOLD")
#         body_text = Text(body, color=WHITE, font_size=22)
#         content = VGroup(headline_text, body_text).arrange(DOWN, buff=0.2)
#         frame = RoundedRectangle(
#             corner_radius=0.2,
#             width=4.2,
#             height=content.height + 0.5,
#             stroke_color=accent_color,
#             fill_color="#0b0f17",
#             fill_opacity=0.7,
#         ).move_to(content)
#         return VGroup(frame, content)
class Scene0_Overview(BaseMathScene):
    def construct(self):
        title = Text("Bài toán Phân tích Ma trận", color=YELLOW, font_size=40, weight="BOLD")
        title.to_edge(UP, buff=0.6)

        matrix_a = Matrix(
            self.to_manim_str_matrix(self.A),
            element_to_mobject=lambda value: MathTex(value),
        ).scale(0.95)
        label_a = MathTex("A =", color=ORANGE).next_to(matrix_a, LEFT)
        center_group = VGroup(label_a, matrix_a).move_to(UP * 0.4) # Đẩy nhẹ lên trên để cân đối hơn

        # Truyền riêng phần Text (Tiếng Việt) và MathTex (Công thức)
        left_panel = self._overview_branch_panel(
            prefix="Phần 1: ", 
            math_formula="A = LL^T", 
            body="Phân rã ma trận SPD", 
            accent_color=GREEN
        )
        right_panel = self._overview_branch_panel(
            prefix="Phần 2: ", 
            math_formula="A = PDP^{-1}", 
            body="Chéo hóa ma trận", 
            accent_color=BLUE
        )
        
        # Mở rộng khoảng cách 2 panel ra một chút cho thoáng
        left_panel.move_to(LEFT * 3.5 + DOWN * 1.8)
        right_panel.move_to(RIGHT * 3.5 + DOWN * 1.8)

        left_arrow = Arrow(center_group.get_bottom(), left_panel.get_top(), buff=0.2, color=GREEN)
        right_arrow = Arrow(center_group.get_bottom(), right_panel.get_top(), buff=0.2, color=BLUE)

        self.play(Write(title), FadeIn(center_group), run_time=self.TIME_NORMAL)
        self.play(
            AnimationGroup(
                Create(left_arrow),
                Create(right_arrow),
                FadeIn(left_panel, shift=UP * 0.15),
                FadeIn(right_panel, shift=UP * 0.15),
                lag_ratio=0.15,
            ),
            run_time=self.TIME_NORMAL,
        )
        self.wait(self.WAIT_LONG) # Dừng lâu hơn một chút (4s) để khán giả kịp đọc

        self.play(
            center_group.animate.scale(0.72).to_corner(UL, buff=0.7),
            FadeOut(left_panel),
            FadeOut(right_panel),
            FadeOut(left_arrow),
            FadeOut(right_arrow),
            FadeOut(title),
            run_time=self.TIME_NORMAL,
        )
        self.wait(self.TIME_FAST)
        self.clear()

    def _overview_branch_panel(self, prefix: str, math_formula: str, body: str, accent_color) -> VGroup:
        # Tách riêng chữ tiếng Việt và công thức Toán để render chuẩn chỉnh
        prefix_text = Text(prefix, color=accent_color, font_size=24, weight="BOLD")
        formula_text = MathTex(math_formula, color=accent_color).scale(0.85)
        
        # Xếp chữ và công thức nằm ngang cạnh nhau
        headline_group = VGroup(prefix_text, formula_text).arrange(RIGHT, buff=0.15)
        
        body_text = Text(body, color=WHITE, font_size=20)
        content = VGroup(headline_group, body_text).arrange(DOWN, buff=0.25)
        
        frame = RoundedRectangle(
            corner_radius=0.2,
            width=max(content.width + 0.8, 4.2), # Khung tự co giãn nếu nội dung dài hơn
            height=content.height + 0.6,
            stroke_color=accent_color,
            fill_color="#0b0f17",
            fill_opacity=0.7,
        ).move_to(content)
        
        return VGroup(frame, content)


# class Scene1_Cholesky_IntroAndSPD(BaseMathScene):
#     def construct(self):
#         self.show_transition_roadmap(1, "1.1. Bài toán & Điều kiện")
#         self.show_goal_and_warning()

#         self.show_transition_roadmap(1, "1.2. Kiểm tra tính chất SPD")
#         self.show_spd_proof()

#     def show_goal_and_warning(self):
#         title = self.make_section_title("Mục tiêu: A = L L^T", GREEN, 34).to_edge(UP, buff=0.6)
#         formula = MathTex(r"A = L L^T", color=GREEN).scale(1.6).move_to(UP * 1.0)
#         warning_text = Text(
#             "ĐIỀU KIỆN ÁP DỤNG: Ma trận A phải là SPD",
#             color=RED,
#             font_size=26,
#             weight="BOLD",
#         )
#         warning_box = SurroundingRectangle(warning_text, color=RED, buff=0.25)
#         warning_group = VGroup(warning_box, warning_text).move_to(DOWN * 1.3)

#         self.play(Write(title), Write(formula), run_time=self.TIME_NORMAL)
#         self.play(FadeIn(warning_group, scale=1.1), run_time=self.TIME_FAST)
#         for _ in range(2):
#             self.play(FadeOut(warning_group), run_time=0.35)
#             self.play(FadeIn(warning_group), run_time=0.35)
#         self.wait(self.WAIT_SHORT)
#         self.play(FadeOut(title), FadeOut(formula), FadeOut(warning_group), run_time=self.TIME_FAST)

#     def show_spd_proof(self):
#         title = self.make_section_title("Kiểm tra tính chất SPD", YELLOW, 34).to_edge(UP, buff=0.6)
#         self.play(Write(title), run_time=self.TIME_NORMAL)

#         matrix_a = Matrix(self.to_manim_str_matrix(self.A), element_to_mobject=lambda value: MathTex(value)).scale(0.78)
#         label_a = MathTex("A", color=ORANGE).next_to(matrix_a, UP)
#         matrix_group = VGroup(label_a, matrix_a).move_to(LEFT * 3.1 + UP * 0.1)
#         self.play(FadeIn(matrix_group), run_time=self.TIME_NORMAL)

#         matrix_at = Matrix(self.to_manim_str_matrix(self.A), element_to_mobject=lambda value: MathTex(value)).scale(0.78).move_to(RIGHT * 3.1 + UP * 0.1)
#         label_at = MathTex("A^T", color=BLUE).next_to(matrix_at, UP)
#         self.play(AnimationGroup(TransformFromCopy(matrix_a, matrix_at), FadeIn(label_at), lag_ratio=0.1), run_time=self.TIME_NORMAL)

#         sym_result = MathTex(r"A = A^T", color=GREEN).scale(1.3).move_to(DOWN * 2.5)
#         self.play(Write(sym_result), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)
#         self.play(FadeOut(matrix_at), FadeOut(label_at), FadeOut(sym_result), run_time=self.TIME_FAST)

#         sylvester_title = Text(
#             "Tiêu chuẩn Sylvester: các định thức con đầu dương",
#             color=WHITE,
#             font_size=24,
#             weight="BOLD",
#         ).to_edge(UP, buff=0.95)
#         self.play(Write(sylvester_title), run_time=self.TIME_NORMAL)
#         self.play(matrix_group.animate.scale(0.92).move_to(LEFT * 3.0 + UP * 0.95), run_time=self.TIME_NORMAL)

#         entries = matrix_a.get_entries()
#         box1 = SurroundingRectangle(entries[0], color=RED, buff=0.08)
#         delta1 = MathTex(r"\Delta_1 = \det([4]) = 4 > 0", color=RED).scale(0.82).move_to(RIGHT * 2.7 + UP * 1.25)
#         self.play(Create(box1), Write(delta1), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)

#         box2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE, buff=0.08)
#         delta2 = MathTex(r"\Delta_2 = 4\cdot 37 - 12\cdot 12 = 4 > 0", color=PURPLE).scale(0.76).next_to(delta1, DOWN, buff=0.45).align_to(delta1, LEFT)
#         self.play(Transform(box1, box2), Write(delta2), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)

#         self.play(FadeOut(delta1), FadeOut(delta2), run_time=self.TIME_FAST)
#         box3 = SurroundingRectangle(VGroup(*entries), color=YELLOW, buff=0.08)
#         delta3_1 = MathTex(
#             r"\Delta_3 = 4(37\cdot 98 - (-43)^2)",
#             r" - 12(12\cdot 98 - (-16)(-43))",
#             r" - 16(12\cdot(-43) - 37(-16))",
#             color=YELLOW,
#         ).scale(0.5).move_to(RIGHT * 2.55 + UP * 0.1)
#         delta3_2 = MathTex(r"\Delta_3 = 7108 - 5856 - 1216 = 36 > 0", color=YELLOW).scale(0.76).next_to(delta3_1, DOWN, buff=0.35).align_to(delta3_1, LEFT)

#         self.play(Transform(box1, box3), run_time=self.TIME_NORMAL)
#         self.play(Write(delta3_1), run_time=self.TIME_SLOW)
#         self.play(Write(delta3_2), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)

#         stamp = Text("PASSED", color=GREEN, font_size=54, weight="BOLD").rotate(15 * PI / 180).move_to(matrix_group.get_center())
#         self.play(FadeIn(stamp, scale=1.6), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_LONG)
#         self.clear()
class Scene1_Cholesky_IntroAndSPD(BaseMathScene):
    def construct(self):
        # 1.1. Mục tiêu và Điều kiện
        self.show_transition_roadmap(1, "1.1. Bài toán & Điều kiện")
        self.show_goal_and_warning()

        # 1.2. Kiểm tra SPD
        self.show_transition_roadmap(1, "1.2. Kiểm tra tính chất SPD")
        self.show_spd_proof()

    def show_goal_and_warning(self):
        # SỬA LỖI 1: Tách riêng Text tiếng Việt và MathTex
        title = Text("Mục tiêu của bài toán", color=GREEN, font_size=36, weight="BOLD").to_edge(UP, buff=0.8)
        formula = MathTex(r"A = L \cdot L^T", color=GREEN).scale(1.8).next_to(title, DOWN, buff=0.8)
        
        warning_text = Text(
            "ĐIỀU KIỆN ÁP DỤNG: Ma trận A phải là SPD\n(Symmetric Positive Definite)",
            color=RED,
            font_size=26,
            weight="BOLD",
            t2c={"(Symmetric Positive Definite)": YELLOW} # Đổi màu dòng phụ chú
        )
        warning_box = SurroundingRectangle(warning_text, color=RED, buff=0.3, stroke_width=4)
        warning_group = VGroup(warning_box, warning_text).move_to(DOWN * 1.5)

        self.play(Write(title), FadeIn(formula, shift=UP*0.2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        
        # Hiệu ứng cảnh báo nhấp nháy mượt hơn
        self.play(FadeIn(warning_group, scale=1.1), run_time=self.TIME_FAST)
        self.play(Indicate(warning_box, color=YELLOW, scale_factor=1.05), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        
        self.play(FadeOut(title), FadeOut(formula), FadeOut(warning_group), run_time=self.TIME_FAST)

    def show_spd_proof(self):
        # --- BƯỚC 1: KIỂM TRA TÍNH ĐỐI XỨNG ---
        title1 = Text("1. Tính đối xứng (Symmetric)", color=YELLOW, font_size=32, weight="BOLD").to_edge(UP, buff=0.5)
        self.play(Write(title1), run_time=self.TIME_NORMAL)

        matrix_a = Matrix(self.to_manim_str_matrix(self.A), element_to_mobject=lambda value: MathTex(value)).scale(0.8)
        label_a = MathTex("A", color=ORANGE).next_to(matrix_a, UP)
        matrix_group = VGroup(label_a, matrix_a).move_to(LEFT * 3.0 + DOWN * 0.2) # Hạ thấp xuống để thoáng
        self.play(FadeIn(matrix_group), run_time=self.TIME_NORMAL)

        matrix_at = Matrix(self.to_manim_str_matrix(self.A), element_to_mobject=lambda value: MathTex(value)).scale(0.8).move_to(RIGHT * 3.0 + DOWN * 0.2)
        label_at = MathTex("A^T", color=BLUE).next_to(matrix_at, UP)
        
        self.play(
            AnimationGroup(TransformFromCopy(matrix_a, matrix_at), FadeIn(label_at), lag_ratio=0.2), 
            run_time=self.TIME_NORMAL
        )

        sym_result = MathTex(r"A = A^T", color=GREEN).scale(1.3).move_to(DOWN * 2.8)
        self.play(Write(sym_result), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        
        # Dọn dẹp màn hình bên phải
        self.play(FadeOut(matrix_at), FadeOut(label_at), FadeOut(sym_result), run_time=self.TIME_FAST)

        # --- BƯỚC 2: TIÊU CHUẨN SYLVESTER ---
        # SỬA LỖI 2: Dùng Transform để đổi tiêu đề, tránh đè chữ
        title2 = Text("2. Tiêu chuẩn Sylvester (Định thức con > 0)", color=YELLOW, font_size=32, weight="BOLD").to_edge(UP, buff=0.5)
        self.play(Transform(title1, title2), run_time=self.TIME_NORMAL)

        # SỬA LỖI 3: Dời ma trận A sang lề trái hoàn toàn, hạ thấp xuống để không đụng tiêu đề
        self.play(matrix_group.animate.scale(0.95).move_to(LEFT * 3.5 + DOWN * 0.5), run_time=self.TIME_NORMAL)

        entries = matrix_a.get_entries()
        
        # Tính Delta 1
        box1 = SurroundingRectangle(entries[0], color=RED, buff=0.1)
        delta1 = MathTex(r"\Delta_1 = \det([4]) = 4 > 0", color=RED).scale(0.85).move_to(RIGHT * 2.5 + UP * 1.5)
        self.play(Create(box1), Write(delta1), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)

        # Tính Delta 2
        box2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE, buff=0.1)
        delta2 = MathTex(r"\Delta_2 = 4(37) - 12(12) = 4 > 0", color=PURPLE).scale(0.85).next_to(delta1, DOWN, buff=0.8).align_to(delta1, LEFT)
        self.play(Transform(box1, box2), Write(delta2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)

        # Dọn dẹp Delta 1, 2 để nhường chỗ cho Delta 3 (vì công thức rất dài)
        self.play(FadeOut(delta1), FadeOut(delta2), run_time=self.TIME_FAST)
        
        # Tính Delta 3
        box3 = SurroundingRectangle(VGroup(*entries), color=YELLOW, buff=0.1)
        
        # SỬA LỖI 4: Bẻ công thức Delta 3 thành nhiều dòng bằng VGroup để không bị tràn lề phải
        d3_line1 = MathTex(r"\Delta_3 = 4(37 \cdot 98 - (-43)^2)", color=YELLOW)
        d3_line2 = MathTex(r"- 12(12 \cdot 98 - (-16)(-43))", color=YELLOW)
        d3_line3 = MathTex(r"- 16(12 \cdot (-43) - 37(-16))", color=YELLOW)
        d3_line4 = MathTex(r"= 7108 - 5856 - 1216", color=YELLOW)
        d3_line5 = MathTex(r"= 36 > 0", color=YELLOW)
        
        delta3_group = VGroup(d3_line1, d3_line2, d3_line3, d3_line4, d3_line5)
        delta3_group.arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.75)
        delta3_group.move_to(RIGHT * 2.5 + DOWN * 0.2) # Đặt ở nửa bên phải màn hình

        self.play(Transform(box1, box3), run_time=self.TIME_NORMAL)
        
        # Vẽ tuần tự từng dòng công thức
        self.play(Write(VGroup(d3_line1, d3_line2, d3_line3)), run_time=self.TIME_SLOW)
        self.wait(1.0)
        self.play(Write(VGroup(d3_line4, d3_line5)), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)

        # Đóng dấu PASSED lên thẳng vị trí của ma trận
        stamp = Text("PASSED", color=GREEN, font_size=60, weight="BOLD")
        stamp.rotate(20 * PI / 180).move_to(matrix_a.get_center())
        
        # Khung viền cho con dấu
        stamp_box = SurroundingRectangle(stamp, color=GREEN, buff=0.2, stroke_width=6)
        stamp_group = VGroup(stamp_box, stamp)
        
        self.play(FadeIn(stamp_group, scale=2.5), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_LONG) # Dừng lâu hơn để khán giả xem kết quả cuối cùng
        
        self.clear()

# class Scene2_Cholesky_Calculation(BaseMathScene):
#     def construct(self):
#         self.show_transition_roadmap(1, "1.3. Tính toán ma trận L")
#         self.calculate_l_step_by_step()
#         self.verify_cholesky_numpy()

#         self.show_transition_roadmap(1, "1.4. Đánh giá chi phí")
#         self.show_cost_bar_chart()

#     def calculate_l_step_by_step(self):
#         title = self.make_section_title("Tính toán từng phần tử của L", YELLOW, 34).to_edge(UP, buff=0.6)

#         matrix_a = Matrix(self.to_manim_str_matrix(self.A), element_to_mobject=lambda value: MathTex(value)).scale(0.72).move_to(LEFT * 3.6 + UP * 0.9)
#         label_a = MathTex("A", color=ORANGE).scale(0.9).next_to(matrix_a, UP)
#         matrix_l = Matrix([["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]], element_to_mobject=lambda value: MathTex(value)).scale(0.72).move_to(RIGHT * 3.6 + UP * 0.9)
#         label_l = MathTex("L", color=GREEN).scale(0.9).next_to(matrix_l, UP)

#         recurrence = VGroup(
#             MathTex(r"L_{jj}=\sqrt{A_{jj}-\sum_{k<j}L_{jk}^2}", color=WHITE),
#             MathTex(r"L_{ij}=\frac{A_{ij}-\sum_{k<j}L_{ik}L_{jk}}{L_{jj}}", color=WHITE),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(0.58).move_to(LEFT * 3.4 + DOWN * 2.15)

#         self.play(Write(title), FadeIn(matrix_a), FadeIn(label_a), FadeIn(matrix_l), FadeIn(label_l), Write(recurrence), run_time=self.TIME_NORMAL)

#         steps = [
#             {"formula": r"L_{11}=\sqrt{4}=2", "value": "2", "target": (1, 1), "highlight": [(1, 1)]},
#             {"formula": r"L_{21}=12/2=6", "value": "6", "target": (2, 1), "highlight": [(2, 1), (1, 1)]},
#             {"formula": r"L_{31}=-16/2=-8", "value": "-8", "target": (3, 1), "highlight": [(3, 1), (1, 1)]},
#             {"formula": r"L_{22}=\sqrt{37-6^2}=1", "value": "1", "target": (2, 2), "highlight": [(2, 2), (2, 1)]},
#             {"formula": r"L_{32}=\frac{-43-(-8\cdot 6)}{1}=5", "value": "5", "target": (3, 2), "highlight": [(3, 2), (3, 1), (2, 1)]},
#             {"formula": r"L_{33}=\sqrt{98-((-8)^2+5^2)}=3", "value": "3", "target": (3, 3), "highlight": [(3, 3), (3, 1), (3, 2)]},
#         ]

#         formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.84).move_to(RIGHT * 2.4 + DOWN * 2.1)
#         self.play(Write(formula_box), run_time=self.TIME_NORMAL)

#         for step in steps:
#             updated_formula = MathTex(step["formula"], color=YELLOW).scale(0.84).move_to(formula_box)
#             self.play(Transform(formula_box, updated_formula), run_time=self.TIME_NORMAL)

#             highlights = [self.highlight_cell(matrix_a, row, col, ORANGE) for row, col in step["highlight"]]
#             self.play(*[FadeIn(box) for box in highlights], run_time=self.TIME_FAST)

#             row, col = step["target"]
#             index = (row - 1) * 3 + (col - 1)
#             target_entry = matrix_l.get_entries()[index]
#             flying_value = MathTex(step["value"], color=GREEN).scale(0.8).move_to(formula_box).shift(UP * 0.5)
#             replacement = MathTex(step["value"], color=WHITE).scale(0.7).move_to(target_entry.get_center())

#             self.play(FadeIn(flying_value, shift=UP * 0.15), run_time=self.TIME_FAST)
#             self.play(Transform(flying_value, replacement), run_time=self.TIME_NORMAL)
#             self.play(Transform(target_entry, replacement.copy()), run_time=self.TIME_NORMAL)
#             self.play(FadeOut(flying_value), *[FadeOut(box) for box in highlights], run_time=self.TIME_FAST)

#         self.wait(self.WAIT_SHORT)
#         self.clear()

#     def verify_cholesky_numpy(self):
#         title = self.make_section_title("Đối chiếu kết quả phân rã Cholesky", BLUE, 32).to_edge(UP, buff=0.6)
#         np_A = np.array(self.A)
#         np_L = np.linalg.cholesky(np_A)

#         manual_group = self.make_labeled_matrix(self.to_manim_str_matrix(self.L), "L_{manual} =", ORANGE, scale=0.7)
#         numpy_group = self.make_labeled_matrix(self.to_manim_str_matrix(np_L.tolist()), "L_{numpy} =", BLUE, scale=0.7)

#         manual_row = VGroup(Text("Tính toán thủ công", color=WHITE, font_size=24), manual_group).arrange(RIGHT, buff=0.5)
#         numpy_row = VGroup(Text("Thư viện Numpy", color=WHITE, font_size=24), numpy_group).arrange(RIGHT, buff=0.5)
#         comparison = VGroup(manual_row, numpy_row).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to(UP * 0.25)

#         msg = Text("Ma trận L khớp với kết quả của numpy.linalg.cholesky", color=GREEN, font_size=28, weight="BOLD").next_to(comparison, DOWN, buff=0.9)

#         self.play(Write(title), run_time=self.TIME_NORMAL)
#         self.play(FadeIn(manual_row, shift=UP * 0.1), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)
#         self.play(FadeIn(numpy_row, shift=UP * 0.1), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)
#         self.play(Write(msg), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_LONG)
#         self.clear()

#     def show_cost_bar_chart(self):
#         title = self.make_section_title("Đánh giá chi phí tính toán", YELLOW, 34).to_edge(UP, buff=0.6)
#         chart = BarChart(
#             values=[2.0, 1.0],
#             bar_names=["LU", "Cholesky"],
#             y_range=[0, 2.5, 0.5],
#             bar_colors=[RED, GREEN],
#             y_length=3.2,
#             x_length=4.2,
#         ).move_to(UP * 0.5)
#         stats = VGroup(
#             MathTex(r"\text{LU} \approx \frac{2}{3}n^3", color=RED),
#             MathTex(r"\text{Cholesky} \approx \frac{1}{3}n^3", color=GREEN),
#         ).arrange(RIGHT, buff=1.1).next_to(chart, DOWN, buff=0.45)
#         conclusion = Text("Tiết kiệm xấp xỉ 50% khối lượng tính toán", color=YELLOW, font_size=28).next_to(stats, DOWN, buff=0.45)

#         self.play(Write(title), FadeIn(chart), run_time=self.TIME_NORMAL)
#         self.play(Write(stats), run_time=self.TIME_NORMAL)
#         self.play(Write(conclusion), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_LONG)
#         self.clear()

from manim import Line # Thêm import Line ở đầu file nếu chưa có

class Scene2_Cholesky_Calculation(BaseMathScene):
    def construct(self):
        # 1.3. Tính toán L
        self.show_transition_roadmap(1, "1.3. Tính toán ma trận L")
        self.calculate_l_step_by_step()
        self.verify_cholesky_numpy()

        # 1.4. Chi phí
        self.show_transition_roadmap(1, "1.4. Đánh giá chi phí")
        self.show_cost_bar_chart()

    def calculate_l_step_by_step(self):
        title = self.make_section_title("Tính toán từng phần tử của L", YELLOW, 34).to_edge(UP, buff=0.4)

        # Đẩy ma trận lên cao hơn (UP * 1.2) để tạo không gian
        matrix_a = Matrix(self.to_manim_str_matrix(self.A), element_to_mobject=lambda value: MathTex(value)).scale(0.75).move_to(LEFT * 3.5 + UP * 1.2)
        label_a = MathTex("A", color=ORANGE).scale(0.9).next_to(matrix_a, UP)
        
        # Làm mờ (opacity=0.3) các số 0 ở nửa trên của L để nhấn mạnh nó là tam giác dưới
        l_initial = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        matrix_l = Matrix(l_initial, element_to_mobject=lambda value: MathTex(value)).scale(0.75).move_to(RIGHT * 3.5 + UP * 1.2)
        label_l = MathTex("L", color=GREEN).scale(0.9).next_to(matrix_l, UP)
        
        for i, entry in enumerate(matrix_l.get_entries()):
            if i in [1, 2, 5]: # Vị trí nửa trên đường chéo
                entry.set_opacity(0.3)

        # Thêm một đường kẻ ngang phân cách khu vực ma trận và khu vực công thức
        divider = Line(LEFT * 6, RIGHT * 6, color=BLUE, stroke_opacity=0.5).move_to(DOWN * 0.4)

        # Căn lề trái cho công thức tổng quát và đặt ở nửa dưới bên trái
        recurrence = VGroup(
            MathTex(r"L_{jj} = \sqrt{A_{jj} - \sum_{k<j}L_{jk}^2}", color=WHITE),
            MathTex(r"L_{ij} = \frac{A_{ij} - \sum_{k<j}L_{ik}L_{jk}}{L_{jj}}", color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.65).move_to(LEFT * 3.5 + DOWN * 1.8)

        self.play(
            Write(title), 
            FadeIn(matrix_a), FadeIn(label_a), 
            FadeIn(matrix_l), FadeIn(label_l), 
            Create(divider),
            Write(recurrence), 
            run_time=self.TIME_NORMAL
        )

        steps = [
            {"formula": r"L_{11}=\sqrt{4}=2", "value": "2", "target": (1, 1), "highlight": [(1, 1)]},
            {"formula": r"L_{21}=\frac{12}{2}=6", "value": "6", "target": (2, 1), "highlight": [(2, 1), (1, 1)]},
            {"formula": r"L_{31}=\frac{-16}{2}=-8", "value": "-8", "target": (3, 1), "highlight": [(3, 1), (1, 1)]},
            {"formula": r"L_{22}=\sqrt{37-6^2}=1", "value": "1", "target": (2, 2), "highlight": [(2, 2), (2, 1)]},
            {"formula": r"L_{32}=\frac{-43-(-8\cdot 6)}{1}=5", "value": "5", "target": (3, 2), "highlight": [(3, 2), (3, 1), (2, 1)]},
            {"formula": r"L_{33}=\sqrt{98-((-8)^2+5^2)}=3", "value": "3", "target": (3, 3), "highlight": [(3, 3), (3, 1), (3, 2)]},
        ]

        # Đặt hộp công thức đang tính ở nửa dưới bên phải
        formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.9).move_to(RIGHT * 3.0 + DOWN * 1.8)
        self.play(Write(formula_box), run_time=self.TIME_NORMAL)

        for step in steps:
            updated_formula = MathTex(step["formula"], color=YELLOW).scale(0.9).move_to(formula_box)
            self.play(Transform(formula_box, updated_formula), run_time=self.TIME_NORMAL)

            highlights = [self.highlight_cell(matrix_a, row, col, ORANGE) for row, col in step["highlight"]]
            self.play(*[FadeIn(box) for box in highlights], run_time=self.TIME_FAST)

            # Xử lý hiệu ứng bay số mượt mà
            row, col = step["target"]
            index = (row - 1) * 3 + (col - 1)
            target_entry = matrix_l.get_entries()[index]
            
            flying_value = MathTex(step["value"], color=GREEN).scale(0.8).move_to(formula_box).shift(UP * 0.6)
            replacement = MathTex(step["value"], color=GREEN).scale(0.75).move_to(target_entry.get_center()) # Match kích thước

            self.play(FadeIn(flying_value, shift=UP * 0.2), run_time=self.TIME_FAST)
            
            # Số bay vào đúng vị trí
            self.play(flying_value.animate.move_to(target_entry.get_center()), run_time=self.TIME_NORMAL)
            
            # Ghi đè (become) để xóa sổ số 0 cũ mà không để lại bóng
            target_entry.become(replacement)
            
            self.play(FadeOut(flying_value), *[FadeOut(box) for box in highlights], run_time=self.TIME_FAST)

        self.wait(self.WAIT_LONG)
        self.clear()

    def verify_cholesky_numpy(self):
        title = self.make_section_title("Đối chiếu kết quả phân rã Cholesky", BLUE, 34).to_edge(UP, buff=0.6)
        np_A = np.array(self.A)
        np_L = np.linalg.cholesky(np_A)

        manual_group = self.make_labeled_matrix(self.to_manim_str_matrix(self.L), "L_{manual} =", ORANGE, scale=0.75)
        numpy_group = self.make_labeled_matrix(self.to_manim_str_matrix(np_L.tolist()), "L_{numpy} =", BLUE, scale=0.75)

        manual_row = VGroup(Text("Tính toán thủ công:", color=WHITE, font_size=26), manual_group).arrange(RIGHT, buff=0.8)
        numpy_row = VGroup(Text("Thư viện Numpy:", color=WHITE, font_size=26), numpy_group).arrange(RIGHT, buff=0.8)
        
        # Căn lề trái cho cả 2 hàng để trông như một cái bảng
        comparison = VGroup(manual_row, numpy_row).arrange(DOWN, aligned_edge=LEFT, buff=1.0).move_to(UP * 0.1)

        msg = Text("✓ Ma trận L khớp hoàn toàn với numpy.linalg.cholesky!", color=GREEN, font_size=28, weight="BOLD").next_to(comparison, DOWN, buff=1.2)

        self.play(Write(title), run_time=self.TIME_NORMAL)
        self.play(FadeIn(manual_row, shift=RIGHT * 0.2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        self.play(FadeIn(numpy_row, shift=RIGHT * 0.2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        self.play(Write(msg), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_LONG)
        self.clear()

    def show_cost_bar_chart(self):
        title = self.make_section_title("Đánh giá chi phí tính toán", YELLOW, 34).to_edge(UP, buff=0.6)
        
        # Phóng to biểu đồ để nhìn rõ nét hơn
        chart = BarChart(
            values=[2.0, 1.0],
            bar_names=["LU", "Cholesky"],
            y_range=[0, 2.5, 0.5],
            bar_colors=[RED, GREEN],
            y_length=4.5, 
            x_length=5.5,
        ).move_to(UP * 0.2)
        
        stats = VGroup(
            MathTex(r"\text{LU} \approx \frac{2}{3}n^3", color=RED),
            MathTex(r"\text{Cholesky} \approx \frac{1}{3}n^3", color=GREEN),
        ).arrange(RIGHT, buff=1.5).next_to(chart, DOWN, buff=0.5)
        
        conclusion = Text("Tiết kiệm xấp xỉ 50% khối lượng tính toán", color=YELLOW, font_size=30, weight="BOLD").next_to(stats, DOWN, buff=0.6)

        self.play(Write(title), FadeIn(chart), run_time=self.TIME_NORMAL)
        self.play(Write(stats), run_time=self.TIME_NORMAL)
        self.play(Write(conclusion), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_LONG)
        self.clear()


class Scene3_Diagonalization(BaseMathScene):
    def construct(self):
        # 2.1. Giới thiệu Bài toán
        self.show_transition_roadmap(2, "2.1. Giới thiệu Bài toán")
        self.show_introduction()

        # 2.2. Thuật toán Chéo hóa (Tìm D, P)
        self.show_transition_roadmap(2, "2.2. Thuật toán Chéo hóa (Tìm D, P)")
        self.find_matrix_D()
        self.find_matrix_P()
        self.show_final_assembly()

        # Đối chiếu kết quả
        self.show_final_verification()

    def show_introduction(self):
        title = self.make_section_title("Giới thiệu Bài toán Chéo hóa", BLUE, 34).to_edge(UP, buff=0.5)
        
        goal = MathTex(r"A = P \cdot D \cdot P^{-1}", color=GREEN).scale(1.8).move_to(UP * 0.5)
        
        desc_group = VGroup(
            Text("Mục tiêu của bài toán:", color=WHITE, font_size=26),
            Text("- Tìm ma trận đường chéo D (chứa các trị riêng)", color=YELLOW, font_size=24),
            Text("- Tìm ma trận khả nghịch P (chứa các vector riêng)", color=ORANGE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(goal, DOWN, buff=0.8)

        self.play(Write(title), run_time=self.TIME_NORMAL)
        self.play(FadeIn(goal, shift=UP*0.2), run_time=self.TIME_NORMAL)
        self.play(FadeIn(desc_group), run_time=self.TIME_NORMAL)
        
        self.wait(self.WAIT_LONG)
        
        # DỌN SẠCH MÀN HÌNH CHUẨN BỊ VÀO THUẬT TOÁN
        self.play(FadeOut(title), FadeOut(goal), FadeOut(desc_group), run_time=self.TIME_FAST)

    def find_matrix_D(self):
        title = self.make_section_title("Bước 1: Tìm ma trận D (Trị riêng)", YELLOW, 30).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=self.TIME_NORMAL)

        # Trái: Phương trình đặc trưng
        char_eq = MathTex(r"\det(A - \lambda I) = 0", color=WHITE).scale(1.2).move_to(LEFT * 3.0 + UP * 1.5)
        self.play(Write(char_eq), run_time=self.TIME_NORMAL)

        mat_a_lam = Matrix(
            [["4-\\lambda", "12", "-16"], ["12", "37-\\lambda", "-43"], ["-16", "-43", "98-\\lambda"]],
            h_buff=2.0,
            element_to_mobject=lambda value: MathTex(value),
        ).scale(0.65).move_to(LEFT * 3.0 + DOWN * 0.5)
        
        self.play(FadeIn(mat_a_lam), run_time=self.TIME_NORMAL)
        self.play(
            Indicate(mat_a_lam.get_entries()[0], color=YELLOW),
            Indicate(mat_a_lam.get_entries()[4], color=YELLOW),
            Indicate(mat_a_lam.get_entries()[8], color=YELLOW),
            run_time=self.TIME_SLOW,
        )

        # Phải: Kết quả Lambda và Ma trận D
        lambdas_text = VGroup(
            MathTex(r"\lambda_1 \approx 123.48", color=GREEN),
            MathTex(r"\lambda_2 \approx 15.50", color=GREEN),
            MathTex(r"\lambda_3 \approx 0.02", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8)
        
        d_matrix = Matrix(
            [[self.fmt(self.lambdas[0]), "0", "0"], ["0", self.fmt(self.lambdas[1]), "0"], ["0", "0", self.fmt(self.lambdas[2])]],
            element_to_mobject=lambda value: MathTex(value),
            h_buff=1.2,
        ).scale(0.7)
        d_label = MathTex("D =", color=GREEN).scale(0.8).next_to(d_matrix, LEFT)
        d_group = VGroup(d_label, d_matrix)
        
        right_panel = VGroup(lambdas_text, d_group).arrange(DOWN, buff=0.8).move_to(RIGHT * 3.0 + DOWN * 0.5)

        self.play(FadeIn(lambdas_text, shift=LEFT*0.2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        self.play(FadeIn(d_group, shift=UP*0.2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_LONG)

        # DỌN SẠCH MÀN HÌNH CHO BƯỚC 2
        self.play(FadeOut(title), FadeOut(char_eq), FadeOut(mat_a_lam), FadeOut(right_panel), run_time=self.TIME_FAST)

    def find_matrix_P(self):
        title = self.make_section_title("Bước 2: Tìm ma trận P (Vector riêng)", ORANGE, 30).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=self.TIME_NORMAL)

        # Trái: Khử Gauss
        step_p = Text("Hệ phương trình: (A - λ₁ I)v₁ = 0", color=WHITE, font_size=24, weight="BOLD").move_to(LEFT * 3.5 + UP * 1.8)
        self.play(Write(step_p), run_time=self.TIME_NORMAL)

        gauss_matrix = Matrix(
            [["-119.48", "12", "-16"], ["12", "-86.48", "-43"], ["-16", "-43", "-25.48"]],
            h_buff=2.0,
            element_to_mobject=lambda value: MathTex(value),
        ).scale(0.55).next_to(step_p, DOWN, buff=0.5).align_to(step_p, LEFT)
        self.play(FadeIn(gauss_matrix), run_time=self.TIME_NORMAL)

        # Mô phỏng phép biến đổi hàng (sau đó xóa đi để đỡ chật)
        row_ops = VGroup(
            MathTex(r"R_2 \leftarrow R_2 + 0.10R_1", color=YELLOW),
            MathTex(r"R_3 \leftarrow R_3 - 0.13R_1", color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.65).next_to(gauss_matrix, RIGHT, buff=0.5)
        
        self.play(Write(row_ops), run_time=self.TIME_SLOW)
        self.wait(1.0)
        self.play(FadeOut(row_ops), run_time=self.TIME_FAST)

        # Phải: Mũi tên và kết quả 3 vector
        arrow = MathTex(r"\Longrightarrow", color=GREEN).scale(1.2).move_to(DOWN * 0.5)
        
        # Nhóm 3 vector
        def make_vec(label_str, val_list):
            label = MathTex(label_str, color=ORANGE).scale(0.7)
            vec = Matrix([[v] for v in val_list], element_to_mobject=lambda value: MathTex(value)).scale(0.6)
            return VGroup(label, vec).arrange(RIGHT, buff=0.15)

        v1_group = make_vec("v_1 =", ["0.16", "-0.21", "0.96"])
        v2_group = make_vec("v_2 =", ["0.45", "-0.84", "-0.26"])
        v3_group = make_vec("v_3 =", ["-0.87", "-0.48", "0.04"])

        vectors_panel = VGroup(v1_group, v2_group, v3_group).arrange(RIGHT, buff=0.5).move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(Write(arrow), FadeIn(v1_group), run_time=self.TIME_NORMAL)
        self.wait(1.0)
        
        step_p2 = Text("Tương tự cho λ₂ và λ₃:", color=WHITE, font_size=24, weight="BOLD").move_to(LEFT * 3.5 + UP * 1.8)
        self.play(Transform(step_p, step_p2), FadeIn(v2_group), FadeIn(v3_group), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_LONG)

        # DỌN SẠCH ĐỂ TỔNG HỢP
        self.play(FadeOut(title), FadeOut(step_p), FadeOut(gauss_matrix), FadeOut(arrow), FadeOut(vectors_panel), run_time=self.TIME_FAST)

    def show_final_assembly(self):
        title = self.make_section_title("Bước 3: Tổng hợp kết quả Phân rã", GREEN, 30).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=self.TIME_NORMAL)

        # Xếp 3 ma trận nằm ngang nhau ở nửa trên
        p_matrix = Matrix(self.to_manim_str_matrix(self.P), element_to_mobject=lambda value: MathTex(value), h_buff=1.2).scale(0.5)
        p_label = MathTex("P =", color=ORANGE).scale(0.8).next_to(p_matrix, UP)
        p_group = VGroup(p_label, p_matrix)

        d_matrix = Matrix(
            [[self.fmt(self.lambdas[0]), "0", "0"], ["0", self.fmt(self.lambdas[1]), "0"], ["0", "0", self.fmt(self.lambdas[2])]],
            element_to_mobject=lambda value: MathTex(value), h_buff=1.2
        ).scale(0.5)
        d_label = MathTex("D =", color=GREEN).scale(0.8).next_to(d_matrix, UP)
        d_group = VGroup(d_label, d_matrix)

        pinv_matrix = Matrix(self.to_manim_str_matrix(self.P_inv), element_to_mobject=lambda value: MathTex(value), h_buff=1.2).scale(0.5)
        pinv_label = MathTex("P^{-1} =", color=BLUE).scale(0.8).next_to(pinv_matrix, UP)
        pinv_group = VGroup(pinv_label, pinv_matrix)

        matrices_panel = VGroup(p_group, d_group, pinv_group).arrange(RIGHT, buff=0.8).move_to(UP * 0.5)
        self.play(FadeIn(matrices_panel, shift=UP*0.2), run_time=self.TIME_NORMAL)

        # Chốt công thức cuối cùng ở dưới đáy
        final_eq = MathTex(r"A = P \cdot D \cdot P^{-1}", color=YELLOW).scale(1.8).move_to(DOWN * 2.2)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.3, stroke_width=4)
        self.play(Write(final_eq), Create(final_box), run_time=self.TIME_SLOW)
        self.wait(self.WAIT_LONG)
        
        self.clear()

    def show_final_verification(self):
        title = self.make_section_title("Đối chiếu trị riêng bằng numpy.linalg.eig", BLUE, 34).to_edge(UP, buff=0.6)
        
        np_A = np.array(self.A)
        eigenvalues, _ = np.linalg.eig(np_A)
        numpy_sorted = sorted((float(value.real) for value in eigenvalues), reverse=True)
        manual_sorted = sorted(self.lambdas, reverse=True)

        manual_text = Text("Tính toán thủ công:", color=WHITE, font_size=26)
        manual_value = MathTex(
            rf"\lambda_{{manual}} = [{self.fmt(manual_sorted[0])}, \ {self.fmt(manual_sorted[1])}, \ {self.fmt(manual_sorted[2])}]",
            color=ORANGE,
        ).scale(0.9)
        
        numpy_text = Text("Thư viện Numpy:", color=WHITE, font_size=26)
        numpy_value = MathTex(
            rf"\lambda_{{numpy}} = [{self.fmt(numpy_sorted[0])}, \ {self.fmt(numpy_sorted[1])}, \ {self.fmt(numpy_sorted[2])}]",
            color=GREEN,
        ).scale(0.9)

        # Căn lề chuẩn: Chữ xếp sát lề phải, Số xếp sát lề trái -> Dấu = tự động thẳng hàng
        text_group = VGroup(manual_text, numpy_text).arrange(DOWN, aligned_edge=RIGHT, buff=0.8)
        value_group = VGroup(manual_value, numpy_value).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        
        comparison = VGroup(text_group, value_group).arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        
        msg = Text("✓ Kết quả trị riêng trùng khớp tuyệt đối!", color=GREEN, font_size=30, weight="BOLD").next_to(comparison, DOWN, buff=1.2)

        self.play(Write(title), run_time=self.TIME_NORMAL)
        
        self.play(FadeIn(manual_text), FadeIn(manual_value, shift=RIGHT*0.2), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_SHORT)
        self.play(FadeIn(numpy_text), FadeIn(numpy_value, shift=RIGHT*0.2), run_time=self.TIME_NORMAL)
        
        self.wait(self.WAIT_SHORT)
        self.play(Write(msg), run_time=self.TIME_NORMAL)
        self.wait(self.WAIT_LONG)
        self.clear()


# class Scene3_Diagonalization(BaseMathScene):
#     def construct(self):
#         # 2.1. Giới thiệu Bài toán
#         self.show_transition_roadmap(2, "2.1. Giới thiệu Bài toán")
#         self.show_characteristic_equation()

#         # 2.2. Thuật toán Chéo hóa (Tìm D, P)
#         self.show_transition_roadmap(2, "2.2. Thuật toán Chéo hóa (Tìm D, P)")
#         self.show_eigenvector_construction()

#         self.show_final_verification()

#     def show_characteristic_equation(self):
#         title = self.make_section_title("Tìm ma trận D từ trị riêng", YELLOW, 34).to_edge(UP, buff=0.4)
        
#         # 1. HIỂN THỊ MỤC TIÊU VÀ DỌN DẸP SẠCH
#         goal = MathTex(r"A = P \cdot D \cdot P^{-1}", color=GREEN).scale(1.5).move_to(UP * 0.5)
#         desc = Text("Mục tiêu: Giải phương trình đặc trưng để tìm các trị riêng", color=WHITE, font_size=26).next_to(goal, DOWN, buff=0.5)

#         self.play(Write(title), run_time=self.TIME_NORMAL)
#         self.play(Write(goal), FadeIn(desc, shift=UP*0.2), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_LONG)
        
#         # Dọn sạch để lấy chỗ vẽ ma trận (KHÔNG ĐỂ TRÙNG LẶP)
#         self.play(FadeOut(goal), FadeOut(desc), run_time=self.TIME_FAST)

#         # 2. HIỂN THỊ PHƯƠNG TRÌNH ĐẶC TRƯNG
#         char_eq = MathTex(r"\det(A - \lambda I) = 0", color=WHITE).scale(1.2).move_to(UP * 1.8)
#         self.play(Write(char_eq), run_time=self.TIME_NORMAL)

#         # Ma trận đẩy sang trái một chút
#         mat_a_lam = Matrix(
#             [["4-\\lambda", "12", "-16"], ["12", "37-\\lambda", "-43"], ["-16", "-43", "98-\\lambda"]],
#             h_buff=2.0,
#             element_to_mobject=lambda value: MathTex(value),
#         ).scale(0.65).move_to(LEFT * 3.0 + DOWN * 0.5)
#         self.play(FadeIn(mat_a_lam), run_time=self.TIME_NORMAL)
        
#         # Nháy sáng đường chéo
#         self.play(
#             Indicate(mat_a_lam.get_entries()[0], color=YELLOW),
#             Indicate(mat_a_lam.get_entries()[4], color=YELLOW),
#             Indicate(mat_a_lam.get_entries()[8], color=YELLOW),
#             run_time=self.TIME_SLOW,
#         )

#         # 3. KẾT QUẢ LAMBDA & MA TRẬN D ĐẶT BÊN PHẢI
#         lambdas_text = VGroup(
#             MathTex(r"\lambda_1 \approx 123.48", color=GREEN),
#             MathTex(r"\lambda_2 \approx 15.50", color=GREEN),
#             MathTex(r"\lambda_3 \approx 0.02", color=GREEN),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8)
        
#         # Nhóm kết quả lambda và ma trận D nằm dọc ở nửa phải màn hình
#         d_matrix = Matrix(
#             [[self.fmt(self.lambdas[0]), "0", "0"], ["0", self.fmt(self.lambdas[1]), "0"], ["0", "0", self.fmt(self.lambdas[2])]],
#             element_to_mobject=lambda value: MathTex(value),
#             h_buff=1.2,
#         ).scale(0.7)
#         d_label = MathTex("D =", color=GREEN).scale(0.8).next_to(d_matrix, LEFT)
#         d_group = VGroup(d_label, d_matrix)
        
#         right_panel = VGroup(lambdas_text, d_group).arrange(DOWN, buff=0.8).move_to(RIGHT * 3.0 + DOWN * 0.5)

#         self.play(FadeIn(lambdas_text, shift=LEFT*0.2), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)
#         self.play(FadeIn(d_group, shift=UP*0.2), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_LONG)

#         self.play(FadeOut(char_eq), FadeOut(mat_a_lam), FadeOut(right_panel), FadeOut(title), run_time=self.TIME_FAST)

#     def show_eigenvector_construction(self):
#         title = self.make_section_title("Tìm ma trận P từ vector riêng", BLUE, 34).to_edge(UP, buff=0.4)
#         self.play(Write(title), run_time=self.TIME_NORMAL)

#         # 1. KHỬ GAUSS (TRÁI)
#         step_p = Text("Hệ phương trình: (A - λ₁ I)v₁ = 0", color=WHITE, font_size=28, weight="BOLD").move_to(UP * 1.8)
#         self.play(Write(step_p), run_time=self.TIME_NORMAL)

#         gauss_matrix = Matrix(
#             [["-119.48", "12", "-16"], ["12", "-86.48", "-43"], ["-16", "-43", "-25.48"]],
#             h_buff=2.0,
#             element_to_mobject=lambda value: MathTex(value),
#         ).scale(0.6).move_to(LEFT * 3.5 + DOWN * 0.5)
#         self.play(FadeIn(gauss_matrix), run_time=self.TIME_NORMAL)

#         # Hiện phép biến đổi hàng, sau đó FADE OUT để nhường chỗ cho mũi tên
#         row_ops = VGroup(
#             MathTex(r"R_2 \leftarrow R_2 + 0.10R_1", color=YELLOW),
#             MathTex(r"R_3 \leftarrow R_3 - 0.13R_1", color=YELLOW),
#         ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.7).next_to(gauss_matrix, RIGHT, buff=0.8)
        
#         self.play(Write(row_ops), run_time=self.TIME_SLOW)
#         self.wait(1.5)
#         self.play(FadeOut(row_ops), run_time=self.TIME_FAST) # XÓA QUAN TRỌNG ĐỂ KHÔNG TRÙNG

#         # 2. HIỆN KẾT QUẢ VECTOR (PHẢI)
#         arrow = MathTex(r"\Longrightarrow", color=GREEN).scale(1.2).move_to(DOWN * 0.5) # Mũi tên ở chính giữa
        
#         v1_label = MathTex("v_1 =", color=ORANGE).scale(0.8)
#         v1_vec = Matrix([["0.16"], ["-0.21"], ["0.96"]], element_to_mobject=lambda value: MathTex(value)).scale(0.65)
#         v1_group = VGroup(v1_label, v1_vec).arrange(RIGHT, buff=0.2)

#         v2_label = MathTex("v_2 =", color=ORANGE).scale(0.8)
#         v2_vec = Matrix([["0.45"], ["-0.84"], ["-0.26"]], element_to_mobject=lambda value: MathTex(value)).scale(0.65)
#         v2_group = VGroup(v2_label, v2_vec).arrange(RIGHT, buff=0.2)

#         v3_label = MathTex("v_3 =", color=ORANGE).scale(0.8)
#         v3_vec = Matrix([["-0.87"], ["-0.48"], ["0.04"]], element_to_mobject=lambda value: MathTex(value)).scale(0.65)
#         v3_group = VGroup(v3_label, v3_vec).arrange(RIGHT, buff=0.2)

#         # Xếp 3 vector ngang nhau ở nửa bên phải
#         vectors_panel = VGroup(v1_group, v2_group, v3_group).arrange(RIGHT, buff=0.6).move_to(RIGHT * 3.2 + DOWN * 0.5)

#         self.play(Write(arrow), FadeIn(v1_group), run_time=self.TIME_NORMAL)
#         self.wait(1.0)
        
#         # Đổi dòng text thành chữ "Tương tự ta có:" để logic hơn
#         step_p2 = Text("Tương tự cho λ₂ và λ₃:", color=WHITE, font_size=28, weight="BOLD").move_to(UP * 1.8)
#         self.play(Transform(step_p, step_p2), FadeIn(v2_group), FadeIn(v3_group), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)

#         # 3. DỌN SẠCH MỌI THỨ VÀ HIỆN P, P^-1
#         self.play(
#             FadeOut(step_p), FadeOut(gauss_matrix), FadeOut(arrow), FadeOut(vectors_panel), # Xóa sạch bóng dáng vector
#             run_time=self.TIME_FAST
#         )

#         p_matrix = Matrix(self.to_manim_str_matrix(self.P), element_to_mobject=lambda value: MathTex(value), h_buff=1.4).scale(0.6)
#         p_label = MathTex("P =", color=ORANGE).scale(0.9).next_to(p_matrix, LEFT)
#         p_group = VGroup(p_label, p_matrix).move_to(LEFT * 3.2 + UP * 0.5) # Đặt P lên trên cùng bên trái

#         pinv_matrix = Matrix(self.to_manim_str_matrix(self.P_inv), element_to_mobject=lambda value: MathTex(value), h_buff=1.4).scale(0.6)
#         pinv_label = MathTex("P^{-1} =", color=BLUE).scale(0.9).next_to(pinv_matrix, LEFT)
#         pinv_group = VGroup(pinv_label, pinv_matrix).move_to(RIGHT * 3.2 + UP * 0.5) # P^-1 bên phải

#         self.play(FadeIn(p_group, shift=UP*0.2), FadeIn(pinv_group, shift=UP*0.2), run_time=self.TIME_NORMAL)

#         # CHỐT CÔNG THỨC CUỐI CÙNG Ở ĐÁY MÀN HÌNH
#         final_eq = MathTex(r"A = P \cdot D \cdot P^{-1}", color=YELLOW).scale(1.8).move_to(DOWN * 2.2)
#         final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.3, stroke_width=4)
#         self.play(Write(final_eq), Create(final_box), run_time=self.TIME_SLOW)
#         self.wait(self.WAIT_LONG)
        
#         self.clear()

#     def show_final_verification(self):
#         title = self.make_section_title("Đối chiếu trị riêng bằng Numpy", BLUE, 34).to_edge(UP, buff=0.6)
        
#         np_A = np.array(self.A)
#         eigenvalues, _ = np.linalg.eig(np_A)
#         numpy_sorted = sorted((float(value.real) for value in eigenvalues), reverse=True)
#         manual_sorted = sorted(self.lambdas, reverse=True)

#         # TÁCH TEXT VÀ MATH ĐỂ CĂN LỀ CHUẨN DẤU "="
#         manual_text = Text("Tính toán thủ công:", color=WHITE, font_size=26)
#         manual_value = MathTex(
#             rf"\lambda_{{manual}} = [{self.fmt(manual_sorted[0])}, \ {self.fmt(manual_sorted[1])}, \ {self.fmt(manual_sorted[2])}]",
#             color=ORANGE,
#         ).scale(0.9)
        
#         numpy_text = Text("Thư viện Numpy:", color=WHITE, font_size=26)
#         numpy_value = MathTex(
#             rf"\lambda_{{numpy}} = [{self.fmt(numpy_sorted[0])}, \ {self.fmt(numpy_sorted[1])}, \ {self.fmt(numpy_sorted[2])}]",
#             color=GREEN,
#         ).scale(0.9)

#         # Đẩy Text về cùng một size chiều rộng để Value (có dấu =) tự động thẳng hàng nhau
#         text_group = VGroup(manual_text, numpy_text).arrange(DOWN, aligned_edge=RIGHT, buff=0.8)
#         value_group = VGroup(manual_value, numpy_value).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        
#         comparison = VGroup(text_group, value_group).arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        
#         msg = Text("✓ Kết quả trị riêng trùng khớp tuyệt đối!", color=GREEN, font_size=30, weight="BOLD").next_to(comparison, DOWN, buff=1.2)

#         self.play(Write(title), run_time=self.TIME_NORMAL)
        
#         # Hiện lần lượt từng dòng
#         self.play(FadeIn(manual_text), FadeIn(manual_value, shift=RIGHT*0.2), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_SHORT)
#         self.play(FadeIn(numpy_text), FadeIn(numpy_value, shift=RIGHT*0.2), run_time=self.TIME_NORMAL)
        
#         self.wait(self.WAIT_SHORT)
#         self.play(Write(msg), run_time=self.TIME_NORMAL)
#         self.wait(self.WAIT_LONG)
#         self.clear()

Scene1Introduction = Scene1_Cholesky_IntroAndSPD
Scene2CholeskyProcess = Scene2_Cholesky_Calculation
Scene3DiagonalizationProcess = Scene3_Diagonalization


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render modular Manim scenes.")
    parser.add_argument("--scene", default="all", help="Scene name to render, or 'all'")
    parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="m")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    file_name = Path(__file__).name
    stem = Path(__file__).stem

    scenes_to_run = [
        "Scene0_Overview",
        "Scene1_Cholesky_IntroAndSPD",
        "Scene2_Cholesky_Calculation",
        "Scene3_Diagonalization",
    ] if args.scene == "all" else [args.scene]

    for scene_name in scenes_to_run:
        print(f"\n[Rendering] {scene_name} at quality {args.quality}...")
        command = [sys.executable, "-m", "manim", f"-q{args.quality}", file_name, scene_name]
        subprocess.run(command, cwd=str(project_dir), check=True)

    if args.scene == "all":
        print("\n[Joining] Concatenating rendered scenes into Full_Presentation.mp4...")
        quality_map = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
        output_folder = project_dir / "media" / "videos" / stem / quality_map[args.quality]
        output_folder.mkdir(parents=True, exist_ok=True)

        list_file = output_folder / "scenes_list.txt"
        final_video = output_folder / "Full_Presentation.mp4"

        with open(list_file, "w", encoding="utf-8") as handle:
            for scene_name in scenes_to_run:
                handle.write(f"file '{scene_name}.mp4'\n")

        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            "scenes_list.txt",
            "-c",
            "copy",
            "Full_Presentation.mp4",
        ]

        subprocess.run(ffmpeg_command, cwd=str(output_folder), check=True)
        print(f"[Done] Final video: {final_video}")
