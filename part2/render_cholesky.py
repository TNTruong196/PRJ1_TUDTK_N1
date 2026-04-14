#!/usr/bin/env python3
"""Render Scene2CholeskyProcess directly."""
import os
import sys
os.chdir(r'd:\File of Phuc\CSC_HCMUS\TUDTK\PRJ1_TUDTK_N1\part2')

from manim import config
config.quality = "low_quality_1080p"  # faster rendering

from manim_scene import Scene2SPDProof  # CholeskyProcess scene

# Render using manim CLI
os.system(r'.\.venv\Scripts\python.exe -m manim -ql manim_scene.py Scene2SPDProof --disable_caching')
