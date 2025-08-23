from manim import *

class TestLatex(Scene):
    def construct(self):
        # LaTeX math rendering
        formula = MathTex(r"E = mc^2")
        self.play(Write(formula))
        self.wait(2)
