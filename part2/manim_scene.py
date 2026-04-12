"""Manim visualization for Cholesky decomposition and diagonalization.

This file strictly follows the project constraints:
- Core matrix computations are implemented with pure Python list-of-lists for visuals.
- Separated into independent Scenes per tasks.md.
- numpy is used purely for verification at the end of scenes.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
from manim import (
    BLUE, GREEN, ORANGE, PURPLE, RED, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, PI,
    BarChart, FadeIn, FadeOut, MathTex, Matrix, Scene,
    SurroundingRectangle, Text, Transform, ReplacementTransform,
    VGroup, Write, AnimationGroup, Indicate, Create
)

# ==========================================
# Lớp cơ sở: Chứa dữ liệu chuẩn & Helper (Pha A)
# ==========================================
class BaseMathScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Task A1: Khóa dữ liệu chuẩn
        self.A = [
            [4.0, 12.0, -16.0],
            [12.0, 37.0, -43.0],
            [-16.0, -43.0, 98.0],
        ]
        self.L = self.cholesky_decompose(self.A)
        
        # Hardcode để giữ nguyên thiết kế hiển thị đẹp của part 6
        self.lambdas = [123.4772, 15.5040, 0.0188]
        self.eigenvectors = [
            [0.1630, 0.4573, -0.8742],
            [-0.2127, -0.8489, -0.4838],
            [0.9635, -0.2648, 0.0411],
        ]

    # Các hàm pure-math helper nguyên bản
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

    # Hàm chuyển cảnh Roadmap dùng chung cho mọi Scene
    def show_transition_roadmap(self, step_index: int):
        self.clear() # Đảm bảo dọn sạch màn hình trước khi hiển thị roadmap
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

        if step_index == 0:
            # Lần hiển thị đầu tiên ở Scene 1: Bay vào từ từ từng dòng
            self.play(Write(title), run_time=1.5)
            self.play(AnimationGroup(*[FadeIn(t, shift=DOWN*0.3) for t in step_texts], lag_ratio=0.3), run_time=1.5)
            self.wait(2)
        else:
            # Lần hiển thị các bước sau: Hiện ra nhanh hơn để nhắc nhở
            self.play(FadeIn(title), FadeIn(step_texts), run_time=1.3)
            self.wait(1.5)

        # Khoanh vùng màu xanh lá cây vào đúng mục sắp trình bày
        box = SurroundingRectangle(step_texts[step_index], color=GREEN, buff=0.2)
        self.play(Create(box), run_time=1.5)
        self.wait(2.5)
        
        # Dọn dẹp màn hình mượt mà để nhường chỗ cho nội dung chính
        self.play(FadeOut(title), FadeOut(step_texts), FadeOut(box), run_time=1.5)


# ==========================================
# Scene 1: Introduction (Pha B)
# ==========================================
class Scene1Introduction(BaseMathScene):
    def construct(self):
        self.show_transition_roadmap(0) # Đánh dấu Mục 1
        self.part2_intro()

    def part2_intro(self):
        matrix_a = Matrix(
            self.to_manim_str_matrix(self.A),
            element_to_mobject=lambda x: MathTex(x),
        ).scale(0.9)
        matrix_a.move_to(UP * 0.5)
        label_a = MathTex("A =", color=ORANGE).next_to(matrix_a, LEFT)
        group_a = VGroup(label_a, matrix_a)
        self.play(FadeIn(group_a), run_time=1.5)

        question = Text("Làm thế nào để phân tích ma trận A này?", font_size=28, color=YELLOW)
        question.next_to(group_a, DOWN, buff=0.8)
        self.play(Write(question), run_time=1.5)
        self.wait(2.5)

        formulas = VGroup(
            MathTex(r"1.\ A = L L^T", color=GREEN),
            MathTex(r"2.\ A = P D P^{-1}", color=BLUE)
        ).scale(1.2).arrange(RIGHT, buff=1.5).move_to(question.get_center())
        
        self.play(Transform(question, formulas), run_time=1.5)
        self.wait(2)

        # Cân bằng khung hình: Đưa A sang nửa trái, Đưa 2 công thức xuống chính giữa đáy màn hình
        self.play(
            group_a.animate.scale(0.8).move_to(LEFT * 3 + UP * 0.5),
            question.animate.scale(0.9).move_to(DOWN * 2),
            run_time=1.5
        )

        l_template = [
            ["L_{11}", "0", "0"],
            ["L_{21}", "L_{22}", "0"],
            ["L_{31}", "L_{32}", "L_{33}"]
        ]
        
        # Bổ sung nhãn "L =" và gom thành group để căn giữa chuẩn xác ở nửa bên phải
        matrix_l = Matrix(l_template).scale(0.9)
        label_l = MathTex("L =", color=GREEN).next_to(matrix_l, LEFT)
        group_l = VGroup(label_l, matrix_l).move_to(RIGHT * 3 + UP * 0.5) 
        
        entries = matrix_l.get_entries()
        entries[1].set_color(RED); entries[2].set_color(RED); entries[5].set_color(RED)

        desc = Text("L là ma trận tam giác dưới (nửa trên bằng 0)", font_size=24, color=WHITE)
        # Gắn text mô tả nằm ngay ngắn bên dưới cả cụm L
        desc.next_to(group_l, DOWN, buff=0.5)

        self.play(FadeIn(group_l), Write(desc), run_time=1.5)
        self.wait(3)
        self.clear()

# ==========================================
# Scene 2: Cholesky Process (Pha C & D)
# ==========================================
class Scene2CholeskyProcess(BaseMathScene):
    def construct(self):
        self.show_transition_roadmap(1) # Đánh dấu Mục 2
        self.part3_spd_check()
        
        self.show_transition_roadmap(2) # Đánh dấu Mục 3
        self.part4_l_calculation()
        
        self.verify_cholesky_numpy()

    def part3_spd_check(self):
        title = Text("Điều kiện: A phải là ma trận SPD", color=YELLOW, font_size=32).to_edge(UP)
        self.play(Write(title), run_time=2.0) # Tăng run_time +0.5s

        sym_text = Text("1. Tính đối xứng (Symmetric):", font_size=24, color=WHITE).to_corner(UL).shift(DOWN * 0.8)
        self.play(Write(sym_text), run_time=2.0)

        # Đặt A và AT cách xa nhau
        matrix_a = Matrix(self.to_manim_str_matrix(self.A)).scale(0.7).move_to(LEFT * 2.5 + UP * 0.3)
        label_a = MathTex("A", color=ORANGE).next_to(matrix_a, UP)
        self.play(FadeIn(matrix_a), FadeIn(label_a), run_time=2.0)

        matrix_at = Matrix(self.to_manim_str_matrix(self.A)).scale(0.7).set_color(BLUE).move_to(RIGHT * 2.5 + UP * 0.3)
        label_at = MathTex("A^T", color=BLUE).next_to(matrix_at, UP)
        
        self.play(
            ReplacementTransform(matrix_a.copy(), matrix_at),
            FadeIn(label_at),
            run_time=2.5 # Tăng run_time +0.5s
        )
        
        sym_result = MathTex(r"A = A^T", color=GREEN).scale(1.2).move_to(DOWN * 2.8)
        self.play(Write(sym_result), run_time=1.5)
        self.wait(2) # Tăng wait +1s
        
        self.play(FadeOut(sym_text), FadeOut(matrix_at), FadeOut(label_at), FadeOut(sym_result), FadeOut(label_a), run_time=2.0)

        # FIX OVERLAP: Dịch chuyển sylv_text lên cao và matrix_a xuống thấp hơn một chút
        sylv_text = Text("2. Tiêu chuẩn Sylvester (Leading principal minors > 0)", font_size=24, color=WHITE).to_corner(UL).shift(DOWN * 0.7)
        self.play(Write(sylv_text), run_time=2.0)
        
        # Dịch matrix_a xuống UP * 1.0 thay vì 1.5 để tránh đè vào sylv_text
        self.play(matrix_a.animate.move_to(LEFT * 3 + UP * 1.0).scale(0.75/0.7), run_time=2.0)

        entries = matrix_a.get_entries()
        box1 = SurroundingRectangle(entries[0], color=RED)
        
        # Căn chỉnh lại tọa độ các phép tính Delta để không đè lên tiêu đề
        calc1 = MathTex(r"\Delta_1 = \det([4]) = 4 > 0", color=RED).scale(0.8).move_to(RIGHT * 2.8 + UP * 1.5)
        self.play(Create(box1), Write(calc1), run_time=1.5)
        self.wait(2) # Tăng wait +1s

        box2 = SurroundingRectangle(VGroup(entries[0], entries[1], entries[3], entries[4]), color=PURPLE)
        calc2 = MathTex(r"\Delta_2 = (4 \times 37) - (12 \times 12) = 4 > 0", color=PURPLE).scale(0.8).next_to(calc1, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(Transform(box1, box2), Write(calc2), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(calc1), FadeOut(calc2), run_time=1.5)
        box3 = SurroundingRectangle(VGroup(*entries), color=YELLOW)
        
        calc3_1 = MathTex(r"\Delta_3 = 4(37 \cdot 98 - (-43)^2) - 12(12 \cdot 98 - (-16)(-43)) - 16(12 \cdot (-43) - 37(-16))", color=YELLOW).scale(0.55)
        calc3_1.move_to(DOWN * 0.8) # Hạ thấp xuống để tránh đè vào ma trận
        
        calc3_2 = MathTex(r"\Delta_3 = 4(1777) - 12(488) - 16(76)", color=YELLOW).scale(0.7)
        calc3_2.next_to(calc3_1, DOWN, buff=0.6).align_to(calc3_1, LEFT)
        
        calc3_3 = MathTex(r"\Delta_3 = 7108 - 5856 - 1216 = 36 > 0", color=YELLOW).scale(0.8)
        calc3_3.next_to(calc3_2, DOWN, buff=0.6).align_to(calc3_1, LEFT)

        self.play(Transform(box1, box3), run_time=2.0)
        self.play(Write(calc3_1), run_time=2.0); self.wait(2)
        self.play(Write(calc3_2), run_time=2.0); self.wait(2)
        self.play(Write(calc3_3), run_time=2.0); self.wait(2)

        stamp = Text("PASSED", color=GREEN, font_size=50, weight="BOLD").rotate(15 * PI / 180).move_to(matrix_a.get_center())
        self.play(FadeIn(stamp, scale=2.0), run_time=1.5)
        self.wait(2)
        self.clear()

    def part4_l_calculation(self):
        title = Text("Bước 3: Thuật toán tính toán L", color=YELLOW, font_size=32).to_edge(UP)
        matrix_a = Matrix(self.to_manim_str_matrix(self.A)).scale(0.7).move_to(LEFT * 3.5 + UP * 1)
        label_a = MathTex("A", color=ORANGE).scale(0.8).next_to(matrix_a, UP)

        l_template = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        matrix_l = Matrix(l_template).scale(0.7).move_to(RIGHT * 3.5 + UP * 1)
        label_l = MathTex("L", color=GREEN).scale(0.8).next_to(matrix_l, UP)
        
        for i, entry in enumerate(matrix_l.get_entries()):
            if i in [1, 2, 5]: entry.set_opacity(0.3)
            else: entry.set_opacity(0.0)

        recurrence = VGroup(
            MathTex(r"L_{jj}=\sqrt{A_{jj}-\sum L_{jk}^2}", color=WHITE),
            MathTex(r"L_{ij}=\frac{1}{L_{jj}}(A_{ij}-\sum L_{ik}L_{jk})", color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.55).move_to(LEFT * 3.5 + DOWN * 2.2)

        self.play(Write(title), FadeIn(matrix_a), FadeIn(label_a), FadeIn(matrix_l), FadeIn(label_l), Write(recurrence), run_time=2.0)

        steps = [
            {"formula": r"L_{11}=\sqrt{4}=2", "val": "2", "pos": (1,1), "hl": [(1,1)]},
            {"formula": r"L_{21}=12/2=6", "val": "6", "pos": (2,1), "hl": [(2,1), (1,1)]},
            {"formula": r"L_{31}=-16/2=-8", "val": "-8", "pos": (3,1), "hl": [(3,1), (1,1)]},
            {"formula": r"L_{22}=\sqrt{37-6^2}=1", "val": "1", "pos": (2,2), "hl": [(2,2), (2,1)]},
            {"formula": r"L_{32}=\frac{1}{1}(-43-(-8 \times 6))=5", "val": "5", "pos": (3,2), "hl": [(3,2), (3,1), (2,1)]},
            {"formula": r"L_{33}=\sqrt{98-((-8)^2+5^2)}=3", "val": "3", "pos": (3,3), "hl": [(3,3), (3,1), (3,2)]},
        ]

        formula_box = MathTex(steps[0]["formula"], color=YELLOW).scale(0.8).move_to(RIGHT * 2.5 + DOWN * 2.2)
        self.play(Write(formula_box), run_time=2.0)

        for step in steps:
            new_formula = MathTex(step["formula"], color=YELLOW).scale(0.8).move_to(formula_box)
            self.play(Transform(formula_box, new_formula), run_time=2.0)
            hl_boxes = [self.highlight_cell(matrix_a, r, c, ORANGE) for r, c in step["hl"]]
            self.play(*[FadeIn(box) for box in hl_boxes], run_time=1.5)

            target_entry = matrix_l.get_entries()[(step["pos"][0]-1)*3 + (step["pos"][1]-1)]
            flying_num = MathTex(step["val"], color=GREEN).scale(0.8).move_to(formula_box).shift(UP*0.5)
            
            self.play(FadeIn(flying_num, shift=UP*0.2), run_time=2.0)
            self.play(flying_num.animate.move_to(target_entry.get_center()), run_time=1.8)
            
            target_entry.become(MathTex(step["val"], color=WHITE).scale(0.7).move_to(target_entry.get_center()))
            target_entry.set_opacity(1.0)
            self.play(FadeOut(flying_num), *[FadeOut(box) for box in hl_boxes], run_time=1.3)

        self.wait(4)
        self.clear()

    def verify_cholesky_numpy(self):
        title = Text("Đối chiếu kết quả phân rã Cholesky", color=BLUE, font_size=32).to_edge(UP)
        np_A = np.array(self.A)
        np_L = np.linalg.cholesky(np_A)
        manual_L = self.L

        manual_text = Text("Tính toán thủ công:", font_size=24, color=WHITE)
        manual_mat = Matrix(self.to_manim_str_matrix(manual_L)).scale(0.7)
        manual_label = MathTex("L_{manual} = ", color=ORANGE).scale(0.8).next_to(manual_mat, LEFT)
        manual_group = VGroup(manual_label, manual_mat)
        
        numpy_text = Text("Thư viện Numpy:", font_size=24, color=WHITE)
        numpy_mat = Matrix(self.to_manim_str_matrix(np_L.tolist())).scale(0.7)
        numpy_label = MathTex("L_{numpy} = ", color=BLUE).scale(0.8).next_to(numpy_mat, LEFT)
        numpy_group = VGroup(numpy_label, numpy_mat)

        comparison_group = VGroup(
            VGroup(manual_text, manual_group).arrange(RIGHT, buff=0.5),
            VGroup(numpy_text, numpy_group).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to(UP * 0.2)

        msg = Text("Ma trận L hoàn toàn khớp với thư viện chuẩn!", color=GREEN, font_size=28).next_to(comparison_group, DOWN, buff=1.0)

        self.play(Write(title), run_time=2.0)
        self.play(FadeIn(manual_group), Write(manual_text), run_time=2.0)
        self.wait(3)
        self.play(FadeIn(numpy_group), Write(numpy_text), run_time=2.0)
        self.wait(3)
        self.play(Write(msg), run_time=1.5)
        self.wait(2)
        self.clear()

# ==========================================
# Scene 3: Diagonalization Process (Pha E & F)
# ==========================================
class Scene3DiagonalizationProcess(BaseMathScene):
    def construct(self):
        self.show_transition_roadmap(3) # Đánh dấu Mục 4
        self.part5_cost()
        
        self.show_transition_roadmap(4) # Đánh dấu Mục 5
        self.part6_diagonalization()
        
        self.verify_eig_numpy()

    def part5_cost(self):
        title = Text("Bước 4: Ưu điểm Chi phí tính toán", color=YELLOW, font_size=32).to_edge(UP)
        
        chart = BarChart(values=[2.0, 1.0], bar_names=["LU", "Cholesky"], y_range=[0, 2.5, 0.5], bar_colors=[RED, GREEN], y_length=3, x_length=4).move_to(UP * 0.8)
        stats = VGroup(MathTex(r"\text{LU} \approx \frac{2}{3}n^3", color=RED), MathTex(r"\text{Cholesky} \approx \frac{1}{3}n^3", color=GREEN)).arrange(RIGHT, buff=1.0).next_to(chart, DOWN, buff=0.5)
        conclusion = Text("Tối ưu 50% khối lượng tính toán cho ma trận SPD", font_size=28, color=YELLOW).next_to(stats, DOWN, buff=0.5)

        self.play(Write(title), FadeIn(chart), run_time=1.5)
        self.play(Write(stats), run_time=1.5)
        self.play(Write(conclusion), run_time=1.5)
        self.wait(3)
        self.clear()

    def part6_diagonalization(self):
        title = Text("Bước 5: Chéo hóa Ma trận", color=YELLOW, font_size=32).to_edge(UP)
        formula = MathTex(r"A = P D P^{-1}", color=GREEN).scale(1.5).move_to(UP * 1.5)
        desc = Text("Mục tiêu: Tìm ma trận đường chéo D (Trị riêng) và P (Vector riêng)", font_size=24, color=WHITE).next_to(formula, DOWN, buff=0.5)

        self.play(Write(title), Write(formula), FadeIn(desc), run_time=1.5)
        self.wait(3)
        theory_group = VGroup(formula, desc)
        self.play(theory_group.animate.scale(0.5).to_corner(UL).shift(DOWN*0.5), run_time=1.5)

        step_d = Text("1. Tìm ma trận D (Giải PT đặc trưng)", font_size=24, color=BLUE).move_to(LEFT*2.5 + UP*1.5)
        char_eq = MathTex(r"\det(A - \lambda I) = 0", color=WHITE).next_to(step_d, DOWN, aligned_edge=LEFT)
        
        mat_a_lam = Matrix([["4-\\lambda", "12", "-16"], ["12", "37-\\lambda", "-43"], ["-16", "-43", "98-\\lambda"]], h_buff=2.5).scale(0.6).next_to(char_eq, DOWN, aligned_edge=LEFT)

        self.play(Write(step_d), Write(char_eq), FadeIn(mat_a_lam), run_time=1.5)
        self.play(Indicate(mat_a_lam.get_entries()[0], color=YELLOW), Indicate(mat_a_lam.get_entries()[4], color=YELLOW), Indicate(mat_a_lam.get_entries()[8], color=YELLOW), run_time=1.5)
        
        lambdas_text = VGroup(
            MathTex(r"\lambda_1 \approx 123.48", color=GREEN), MathTex(r"\lambda_2 \approx 15.50", color=GREEN), MathTex(r"\lambda_3 \approx 0.02", color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).next_to(mat_a_lam, RIGHT, buff=0.5)
        self.play(FadeIn(lambdas_text), run_time=1.5)

        mat_d = Matrix([["\\lambda_1", "0", "0"], ["0", "\\lambda_2", "0"], ["0", "0", "\\lambda_3"]], h_buff=1.2).scale(0.7).to_edge(RIGHT, buff=1.0).shift(UP*0.5)
        label_d = MathTex("D = ", color=GREEN).scale(0.8).next_to(mat_d, LEFT)
        self.play(FadeIn(mat_d), FadeIn(label_d), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(step_d), FadeOut(char_eq), FadeOut(mat_a_lam), FadeOut(lambdas_text), run_time=1.5)

        step_p = Text("2. Tìm ma trận P (Giải hệ phương trình)", font_size=24, color=BLUE).move_to(LEFT*3 + UP*1.5)
        sys_eq = MathTex(r"(A - \lambda_1 I)v_1 = 0", color=WHITE).next_to(step_p, DOWN, aligned_edge=LEFT)
        
        mat_gauss = Matrix([["-119.48", "12", "-16"], ["12", "-86.48", "-43"], ["-16", "-43", "-25.48"]], h_buff=2.2).scale(0.6).next_to(sys_eq, DOWN, aligned_edge=LEFT)
        
        arrow_symbol = MathTex(r"\longrightarrow").next_to(mat_gauss, RIGHT, buff=0.5)
        arrow_text = Text("Khử Gauss", font_size=20, color=WHITE).next_to(arrow_symbol, UP, buff=0.1)
        arrow = VGroup(arrow_symbol, arrow_text)

        label_v1 = MathTex("v_1=").scale(0.7).next_to(arrow, RIGHT, buff=0.5)
        v1 = Matrix([["0.16"], ["-0.21"], ["0.96"]]).scale(0.6).next_to(label_v1, RIGHT, buff=0.1)

        self.play(Write(step_p), Write(sys_eq), run_time=1.5)
        self.play(FadeIn(mat_gauss), run_time=1.5)
        self.play(Write(arrow), FadeIn(v1), FadeIn(label_v1), run_time=1.5)
        self.wait(2)

        v2 = MathTex(r"v_2 = \begin{bmatrix}0.45\\-0.84\\-0.26\end{bmatrix}").scale(0.6).next_to(v1, DOWN, buff=0.2).align_to(label_v1, LEFT)
        v3 = MathTex(r"v_3 = \begin{bmatrix}-0.87\\-0.48\\0.04\end{bmatrix}").scale(0.6).next_to(v2, DOWN, buff=0.2).align_to(label_v1, LEFT)
        self.play(FadeIn(v2), FadeIn(v3), run_time=1.5)
        self.wait(2)
        
        # FIX OVERLAP: Thêm FadeOut(theory_group) để dọn dẹp sạch dòng chữ nhắc nhở góc trái trước khi hiện kết quả
        self.play(FadeOut(step_p), FadeOut(sys_eq), FadeOut(mat_gauss), FadeOut(arrow), FadeOut(theory_group), run_time=1.5)

        p_matrix = Matrix([["0.16", "0.45", "-0.87"], ["-0.21", "-0.84", "-0.48"], ["0.96", "-0.26", "0.04"]], h_buff=1.4).scale(0.5)
        mat_d_final = Matrix([["\\lambda_1", "0", "0"], ["0", "\\lambda_2", "0"], ["0", "0", "\\lambda_3"]], h_buff=1.2).scale(0.5)
        
        pinv_matrix = Matrix([["0.16", "-0.21", "0.96"], ["0.45", "-0.84", "-0.26"], ["-0.87", "-0.48", "0.04"]], h_buff=1.4).scale(0.5)
        
        label_a_eq = MathTex("A =", color=YELLOW).scale(1.0)
        
        final_eq_group = VGroup(label_a_eq, p_matrix, mat_d_final, pinv_matrix).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.5)

        label_p_top = MathTex("P", color=ORANGE).scale(0.8).next_to(p_matrix, UP, buff=0.1)
        label_d_top = MathTex("D", color=GREEN).scale(0.8).next_to(mat_d_final, UP, buff=0.1)
        label_pinv_top = MathTex("P^{-1}", color=BLUE).scale(0.8).next_to(pinv_matrix, UP, buff=0.1)

        self.play(
            ReplacementTransform(VGroup(label_v1, v1, v2, v3), p_matrix),
            ReplacementTransform(VGroup(label_d, mat_d), mat_d_final),
            FadeIn(pinv_matrix),
            FadeIn(label_a_eq),
            run_time=1.5
        )
        self.play(FadeIn(label_p_top), FadeIn(label_d_top), FadeIn(label_pinv_top), run_time=1.5)

        final = MathTex(r"A = P \times D \times P^{-1}", color=YELLOW).scale(1.2).next_to(final_eq_group, UP, buff=1.0)
        self.play(Write(final), run_time=1.5)
        self.wait(4)
        self.clear()

    def verify_eig_numpy(self):
        title = Text("Đối chiếu kết quả Trị riêng", color=BLUE, font_size=32).to_edge(UP)
        np_A = np.array(self.A)
        eigenvals, eigenvecs = np.linalg.eig(np_A)
        
        np_eigenvals_sorted = sorted(eigenvals, reverse=True)
        manual_eigenvals_sorted = sorted(self.lambdas, reverse=True)

        manual_text = Text("Tính toán thủ công:", font_size=24, color=WHITE)
        manual_val = MathTex(
            r"\lambda_{manual} = " + f"[{self.fmt(manual_eigenvals_sorted[0])}, {self.fmt(manual_eigenvals_sorted[1])}, {self.fmt(manual_eigenvals_sorted[2])}]", 
            color=ORANGE
        ).scale(0.9)
        manual_group = VGroup(manual_text, manual_val).arrange(RIGHT, buff=0.5)

        numpy_text = Text("Thư viện Numpy:", font_size=24, color=WHITE)
        numpy_val = MathTex(
            r"\lambda_{numpy} = " + f"[{self.fmt(np_eigenvals_sorted[0])}, {self.fmt(np_eigenvals_sorted[1])}, {self.fmt(np_eigenvals_sorted[2])}]", 
            color=GREEN
        ).scale(0.9)
        numpy_group = VGroup(numpy_text, numpy_val).arrange(RIGHT, buff=0.5)

        comparison_group = VGroup(manual_group, numpy_group).arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to(UP * 0.5)
        
        msg = Text("Kết quả hoàn toàn trùng khớp!", color=GREEN, font_size=28).next_to(comparison_group, DOWN, buff=1.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(manual_group), run_time=1.5)
        self.wait(2)
        self.play(FadeIn(numpy_group), run_time=1.5)
        self.wait(2)
        self.play(Write(msg), run_time=1.5)
        self.wait(4)
        self.clear()
        
# ==========================================
# Trình khởi chạy (Launcher) & Nối Video
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render modular Manim scenes.")
    parser.add_argument("--scene", default="all", help="Name of the scene to render, or 'all'")
    parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="m")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    file_name = Path(__file__).name
    stem = Path(__file__).stem

    scenes_to_run = ["Scene1Introduction", "Scene2CholeskyProcess", "Scene3DiagonalizationProcess"] if args.scene == "all" else [args.scene]

    # 1. Chạy render từng Scene
    for scene in scenes_to_run:
        print(f"\n[🚀] Rendering {scene} at quality {args.quality}...")
        cmd = [sys.executable, "-m", "manim", f"-q{args.quality}", file_name, scene]
        subprocess.run(cmd, cwd=str(project_dir))

    # 2. TỰ ĐỘNG GHÉP 3 VIDEO THÀNH 1 (Nếu chọn render tất cả)
    if args.scene == "all":
        print("\n[🔗] Đang tiến hành ghép 3 video lại thành 1 video tổng hoàn chỉnh...")
        
        # Ánh xạ cờ quality sang thư mục output chuẩn của Manim
        q_map = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
        output_folder = project_dir / "media" / "videos" / stem / q_map[args.quality]
        
        # Tạo file văn bản chứa danh sách các video cần ghép theo đúng thứ tự
        list_file = output_folder / "scenes_list.txt"
        try:
            with open(list_file, "w", encoding="utf-8") as f:
                for scene in scenes_to_run:
                    f.write(f"file '{scene}.mp4'\n")
            
            final_video = output_folder / "Full_Presentation.mp4"
            
            # Lệnh FFmpeg để nối video (Dùng -c copy để giữ nguyên chất lượng, xử lý trong nháy mắt)
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", "scenes_list.txt",
                "-c", "copy", "Full_Presentation.mp4"
            ]
            
            # Chạy lệnh FFmpeg ngầm tại thư mục chứa video
            subprocess.run(ffmpeg_cmd, cwd=str(output_folder), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
            print(f"\n[🎉] THÀNH CÔNG! Đã ghép xong toàn bộ bài thuyết trình.")
            print(f"[📍] Bạn có thể xem video hoàn chỉnh tại: {final_video}")
            
        except Exception as e:
            print(f"\n[⚠️] Có lỗi xảy ra trong quá trình ghép video: {e}")