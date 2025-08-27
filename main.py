import random
from manim import *
import numpy as np

class FicksLaw(MovingCameraScene):
    def construct(self):

        intro = Text("Fick's Law of Diffusion", font_size=48, color=YELLOW)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))
        self.atom()
        self.show_stock()
        self.show_concentration_gradient()
        self.show_equation()
        self.show_summary()
        self.wait(2)

    def show_concentration_gradient(self):
        rectangles = VGroup()
        colors = [BLUE, BLUE_C, BLUE_D, BLUE_E, PURPLE_E]
        for i, color in enumerate(colors):
            rect = Rectangle(width=1.2, height=2, fill_color=color, fill_opacity=0.8)
            rect.shift(RIGHT * (i - 2) * 1.5)
            rectangles.add(rect)

        high_label = Text("High C", font_size=24).next_to(rectangles[0], DOWN)
        low_label = Text("Low C", font_size=24).next_to(rectangles[-1], DOWN)
        arrow = Arrow(start=LEFT*2, end=RIGHT*2, color=RED, buff=0).shift(DOWN*2)

        self.play(Create(rectangles), Write(high_label), Write(low_label))
        self.play(Create(arrow))
        self.wait(1)
        self.play(FadeOut(rectangles, high_label, low_label, arrow))
        
    def atom(self):
        # Create two regions of atoms - high and low concentration
        # High density region - randomly scattered atoms
        atoms_high_density = VGroup()
        for _ in range(100):
            atom = Dot(radius=0.05, color=BLUE)
            # Random position within the high density area
            x = -3 + (random.random() - 0.5) * 2.5  # Scatter around x = -3
            y = (random.random() - 0.5) * 3  # Scatter vertically
            atom.move_to([x, y, 0])
            atoms_high_density.add(atom)

        # Low density region - randomly scattered atoms
        atoms_low_density = VGroup()
        for _ in range(25):
            atom = Dot(radius=0.05, color=BLUE)
            # Random position within the low density area
            x = 3 + (random.random() - 0.5) * 2.5  # Scatter around x = 3
            y = (random.random() - 0.5) * 3  # Scatter vertically
            atom.move_to([x, y, 0])
            atoms_low_density.add(atom)

        # Add labels for the regions
        high_label = Text("High Concentration", font_size=24, color=YELLOW).next_to(atoms_high_density, UP, buff=0.3)
        low_label = Text("Low Concentration", font_size=24, color=YELLOW).next_to(atoms_low_density, UP, buff=0.3)
        
        # Add arrow showing direction of diffusion
        diffusion_arrow = Arrow(start=LEFT*1.5, end=RIGHT*1.5, color=RED, buff=0.5, stroke_width=6)
        diffusion_arrow.shift(DOWN*2.5)
        arrow_label = Text("Net Diffusion", font_size=20, color=RED).next_to(diffusion_arrow, DOWN, buff=0.2)

        # Show the full setup first
        self.play(
            FadeIn(atoms_high_density), 
            FadeIn(atoms_low_density),
            Write(high_label),
            Write(low_label)
        )
        self.wait(0.5)
        
        # Show the diffusion arrow
        self.play(Create(diffusion_arrow), Write(arrow_label))
        self.wait(1)

        # 1. Zoom into individual atoms to see them bouncing randomly
        self.camera.frame.save_state()
        target_atom = atoms_high_density[45]  # Pick an atom in the middle of high density region
        self.play(self.camera.frame.animate.scale(0.2).move_to(target_atom))
        
        # Show individual atoms bouncing around randomly (Brownian motion)
        for _ in range(3):
            random_wiggles = []
            # Focus on atoms near our target
            nearby_atoms = atoms_high_density[40:50]  # Get atoms around our focus area
            for atom in nearby_atoms:
                # Random small movements to simulate thermal motion
                shift_x = (random.random() - 0.5) * 0.3
                shift_y = (random.random() - 0.5) * 0.3
                random_wiggles.append(atom.animate.shift(RIGHT * shift_x + UP * shift_y))
            
            self.play(LaggedStart(*random_wiggles, lag_ratio=0.1, run_time=1))
            self.wait(0.5)

        # 2. Zoom out to show the overall movement from higher to lower concentration
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(0.5)

        # 3. Show the net diffusion from high to low concentration
        # Animate atoms moving from higher to lower concentration area
        diffusion_animations = []
        atoms_to_move = atoms_high_density[:35]  # Move 35 atoms from high to low density
        
        for atom in atoms_to_move:
            # Calculate movement towards low density area with more randomness
            base_shift = RIGHT * (4 + random.random() * 3)  # Move rightward
            random_shift = UP * (random.random() - 0.5) * 4  # Add vertical randomness
            final_shift = base_shift + random_shift
            diffusion_animations.append(atom.animate.shift(final_shift))

        # Add random movement to existing low density atoms
        for atom in atoms_low_density:
            # More chaotic movement for existing atoms
            random_shift = (random.random() - 0.5) * 1.5 * RIGHT + (random.random() - 0.5) * 1.5 * UP
            diffusion_animations.append(atom.animate.shift(random_shift))

        # Also add some movement to remaining high density atoms
        remaining_atoms = atoms_high_density[35:]
        for atom in remaining_atoms:
            small_shift = (random.random() - 0.5) * 0.8 * RIGHT + (random.random() - 0.5) * 0.8 * UP
            diffusion_animations.append(atom.animate.shift(small_shift))

        self.play(LaggedStart(*diffusion_animations, lag_ratio=0.02, run_time=5))
        self.wait(1)

        # 4. Clean up
        self.play(
            FadeOut(atoms_high_density), 
            FadeOut(atoms_low_density),
            FadeOut(high_label),
            FadeOut(low_label),
            FadeOut(diffusion_arrow),
            FadeOut(arrow_label)
        )
        self.wait(0.5)     
    def show_stock(self):
        # Create axes for "time" vs "price"
        axes = Axes(
            x_range=[0, 10, 1],    # time from 0 to 10
            y_range=[0, 25, 5],    # price from 0 to 25 (increased range for multiple lines)
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)  # move down so it's nicely framed

        labels = axes.get_axis_labels(x_label="Time", y_label="Price")
        self.play(Create(axes), Write(labels))

        # Define 8 different colors for the lines
        colors = [YELLOW, BLUE, RED, GREEN, PURPLE, ORANGE, PINK, TEAL]
        
        # Generate 8 different stock price lines
        x_vals = np.linspace(0, 10, 25)
        stock_lines = []
        y_values_list = []
        
        for i, color in enumerate(colors):
            # Start at different price levels
            start_price = 5 + i * 2
            # Generate random walk with slight upward bias (positive drift)
            returns = np.random.normal(0.05, 0.8, 25)  # Small positive drift
            y_vals = start_price + np.cumsum(returns)
            
            # Ensure the line ends higher than it starts (stock-like behavior)
            if y_vals[-1] <= y_vals[0]:
                y_vals = y_vals + (y_vals[0] + 2 - y_vals[-1])
            
            y_values_list.append(y_vals)
            line = axes.plot_line_graph(x_vals, y_vals, add_vertex_dots=False, line_color=color)
            stock_lines.append(line)

        # Animate all lines being drawn with a staggered effect
        self.play(LaggedStart(*[Create(line, run_time=1.5) for line in stock_lines], lag_ratio=0.2))
        self.wait(1)
        
        # Add overall trend lines for each stock
        trend_lines = []
        for i, (y_vals, color) in enumerate(zip(y_values_list, colors)):
            # Create trend line from start to end
            trend_start = axes.coords_to_point(0, y_vals[0])
            trend_end = axes.coords_to_point(10, y_vals[-1])
            trend_line = Line(trend_start, trend_end, color=color, stroke_width=6, stroke_opacity=0.7)
            trend_lines.append(trend_line)
        
        # Show all trend lines
        self.play(LaggedStart(*[Create(trend) for trend in trend_lines], lag_ratio=0.1))
        self.wait(1)
        
        # Now combine all lines into one final upward trend
        # Calculate average y values across all stocks
        combined_y_vals = np.mean(y_values_list, axis=0)
        
        # Add some randomness but ensure strong upward trend
        for i in range(len(combined_y_vals)):
            combined_y_vals[i] += i * 0.3 + np.random.normal(0, 0.2)  # Strong upward bias
        
        # Create the final combined line
        final_line = axes.plot_line_graph(x_vals, combined_y_vals, add_vertex_dots=False, 
                                        line_color=WHITE, stroke_width=8)
        
        # Fade out individual lines and show the combined trend
        self.play(
            *[FadeOut(line) for line in stock_lines],
            *[FadeOut(trend) for trend in trend_lines],
        )
        self.play(Create(final_line, run_time=2))
        
        # Add label for the final trend
        trend_label = Text("Combined Positive Trend", font_size=24, color=WHITE)
        trend_label.next_to(final_line, UP, buff=0.5)
        self.play(Write(trend_label))
        self.wait(2)
        
        # Clean up
        all_objects = VGroup(final_line, trend_label, axes, labels)
        self.play(FadeOut(all_objects))
        self.wait(1)

    def show_equation(self):
        eq = MathTex(r"J = -D \frac{dC}{dx}", font_size=72, color=WHITE)
        self.play(Write(eq))
        self.wait(4)
        self.play(FadeOut(eq))


    def show_summary(self):
        points = VGroup(
            Text("• High → Low concentration", font_size=30),
            Text("• Rate ∝ gradient", font_size=30),
            Text("• D affects speed", font_size=30),
            Text("• Negative sign = opposite direction", font_size=30)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)

        for p in points:
            self.play(Write(p))
            self.wait(0.5)

        final_eq = MathTex(r"J = -D \frac{dC}{dx}", font_size=60, color=BLUE).to_edge(DOWN)
        self.play(Write(final_eq))
