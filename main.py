import random
from manim import *
import numpy as np

class FicksLaw(MovingCameraScene):
    def construct(self):

        # intro#2 self.atom()
        # intro#2 self.show_concentration_gradient()
        # intro#2 self.show_change()
        
        self.show_equation()
        # Stock Market self.show_stock()
    def show_change(self):
        low = Text("High concentration").scale(0.6).to_edge(LEFT)
      
        high = Text("Low concentration").scale(0.6).to_edge(RIGHT)
        arrow = Arrow(start=low.get_right(), end=high.get_left(), buff=0.5, stroke_width=6)
        self.play(Write(low), Write(high), Write(arrow))
        self.wait(1)
        self.play(FadeOut(low), FadeOut(high), FadeOut(arrow))

    def show_concentration_gradient(self):
        rectangles = VGroup()
        colors = [BLUE, BLUE_C, BLUE_D, BLUE_E, PURPLE_E]
        for i, color in enumerate(colors):
            rect = Rectangle(width=1.2, height=2, fill_color=color, fill_opacity=0.8)
            rect.shift(RIGHT * (i - 2) * 1.5)
            rectangles.add(rect)
        
        high_label = Text("Dense Group Of Atoms", font_size=24).next_to(rectangles[0], DOWN)
        low_label = Text("Dispersed Group Of Atoms", font_size=24).next_to(rectangles[-1], DOWN)
        arrow = Arrow(start=LEFT*2, end=RIGHT*2, color=RED, buff=0).shift(DOWN*2)
        arrow_label = Text("Over Time", font_size=18, color=BLUE_B).next_to(arrow, DOWN, buff=0.2)
        self.play(Create(rectangles), Write(high_label), Write(low_label))
        self.wait(1)
         # Add arrow showing direction of diffusion (left to right - high to low concentration)
        self.play(Create(arrow), Write(arrow_label))
        self.wait(3)
        

        self.play(FadeOut(rectangles, high_label, low_label, arrow, arrow_label))
        
    def atom(self):
        # Create only high density region initially - randomly scattered atoms
        atoms_high_density = VGroup()
        for _ in range(100):
            atom = Dot(radius=0.05, color=BLUE)
            # Random position within the high density area (left side)
            x = -3 + (random.random() - 0.5) * 2.5  # Scatter around x = -3
            y = (random.random() - 0.5) * 3  # Scatter vertically
            atom.move_to([x, y, 0])
            atoms_high_density.add(atom)

        # Add a divider line between high and low concentration areas
        divider = Line(start=[0, -2, 0], end=[0, 2, 0], color=WHITE, stroke_width=4)
        

        # Add labels for the regions
        high_label = Text("High Concentration", font_size=24, color=YELLOW).move_to([-3, 2.5, 0])
        low_label = Text("Low Concentration", font_size=24, color=YELLOW).move_to([3, 2.5, 0])
        
        # Add arrow showing direction of diffusion (left to right - high to low concentration)
        diffusion_arrow = Arrow(start=LEFT*1.5, end=RIGHT*1.5, color=RED, buff=0.5, stroke_width=6)
        diffusion_arrow.shift(DOWN*2.5)
        arrow_label = Text("Diffusion: High → Low Concentration", font_size=18, color=RED).next_to(diffusion_arrow, DOWN, buff=0.2)

        # Show only the high density atoms first
        self.play(
            FadeIn(atoms_high_density),
            Write(high_label),
            
        )
        self.wait(1)
        

      

        # 1. Zoom into individual atoms to see them bouncing randomly
        self.camera.frame.save_state()
        target_atom = atoms_high_density[45]  # Pick an atom in the middle of high density region
        self.play(self.camera.frame.animate.scale(0.2).move_to(target_atom), run_time=1)
        
        self.play(Create(divider),
                  Write(low_label),
                  Create(diffusion_arrow), 
                  Write(arrow_label), run_time=0.4  )
                  
   
        
        # Show ALL atoms bouncing around randomly (Brownian motion) - faster
        for _ in range(3):  # Reduced from 3 to 2 iterations
            random_wiggles = []
            # Make ALL atoms in the scene move, not just nearby ones
            for atom in atoms_high_density:
                # Random small movements to simulate thermal motion
                shift_x = (random.random() - 0.5) * 0.3
                shift_y = (random.random() - 0.5) * 0.3
                random_wiggles.append(atom.animate.shift(RIGHT * shift_x + UP * shift_y))
            
            self.play(LaggedStart(*random_wiggles, lag_ratio=0.05, run_time=0.8))  # Faster
            self.wait(0.3)  # Shorter wait

        # 2. Zoom out to show the overall movement - faster
        self.play(Restore(self.camera.frame), run_time=1.5)
        self.wait(1)

        # 3. Show atoms moving from HIGH to LOW concentration area (left to right)
        # Move ALL atoms from high density (left) to low density area (right)
        diffusion_animations = []
        # Move ALL atoms, not just 70
        for atom in atoms_high_density:
            # Calculate movement towards LOW density area (RIGHT side) - crosses the divider
            base_shift = RIGHT * (5 + random.random() * 2)  # Move RIGHTWARD across divider to low concentration
            random_shift = UP * (random.random() - 0.5) * 4  # Add vertical randomness
            final_shift = base_shift + random_shift
            diffusion_animations.append(atom.animate.shift(final_shift))
            
            
                # Show the low concentration label and diffusion arrow


        self.play(LaggedStart(*diffusion_animations, lag_ratio=0.005, run_time=4))  # All atoms move
        self.wait(2)

        # 4. Clean up
        self.play(
            FadeOut(atoms_high_density),
            FadeOut(high_label),
            FadeOut(low_label),
            FadeOut(diffusion_arrow),
            FadeOut(arrow_label),
            FadeOut(divider),
         
        )
        self.wait(1)     
    def show_stock(self):
        # Create axes for "time" vs "price"
        axes = Axes(
            x_range=[0, 10, 1],    # time from 0 to 10
            y_range=[0, 25, 5],    # price from 0 to 25 (increased range for multiple lines)
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)  # move down so it's nicely framed

        labels = axes.get_axis_labels(x_label="Time", y_label="Price")
        self.play(Create(axes), Write(labels))
        self.wait(1)

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
        self.play(LaggedStart(*[Create(line, run_time=3) for line in stock_lines], lag_ratio=0.2))
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
            *[FadeOut(line) for line in stock_lines]
            
        )
        self.play(Create(final_line, run_time=2))
        
        # Add label for the final trend
        trend_label = Text("Combined Trend", font_size=24, color=BLUE)
        trend_label.next_to(final_line, UP, buff=0.5)
        self.play(Write(trend_label))
        self.wait(2)
        
        # Clean up
        all_objects = VGroup(final_line, trend_label, axes, labels)
        self.play(FadeOut(all_objects))
      

    def show_equation(self):
        # Define unique colors for each component of the equation
        J_color = BLUE
        D_color = RED
        C_color = GREEN

        # Create the equation, breaking it into parts to be animated individually
        eq = MathTex(r"J", r"=", r"-D", r"\frac{dC}{dx}", font_size=96)
        
        # Create text labels for each part of the equation
        # These will be placed relative to the equation components
        j_label = Text("Rate of Diffusion", font_size=36).next_to(eq[0], UP, buff=0.5)
        d_label = Text("Diffusivity", font_size=36).next_to(eq[2], UP, buff=0.5)
        c_label = Text("Concentration Gradient", font_size=36).next_to(eq[3], DOWN, buff=0.5)

        # --- Animation starts here ---

        # Timestamp 0:00 - 0:02: "All right, time for the equation."
        # The equation is written to the screen in the default color (white).
        self.play(Write(eq))

        # Timestamp 0:02 - 0:06: "This is the rate of diffusion..."
        # Change the color of 'J' and write its corresponding label.
        self.play(
            eq[0].animate.set_color(J_color),
            Write(j_label)
        )
        self.wait(4)

        # Timestamp 0:06 - 0:15: "Next is the diffusivity..."
        # Change the color of '-D' and write its label. The color of 'J' persists.
        self.play(
            eq[2].animate.set_color(D_color),
            Write(d_label)
        )
        self.wait(9)

        # Timestamp 0:15 - 0:30: "Finally, we have the concentration gradient..."
        # Change the color of the gradient term and write its label.
        self.play(
            eq[3].animate.set_color(C_color),
            Write(c_label)
        )
        self.wait(15)

        # Group all the created objects (the equation and all three labels)
        # into a single VGroup for a clean, simultaneous fade-out.
        all_objects = VGroup(eq, j_label, d_label, c_label)
        self.play(FadeOut(all_objects))

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
