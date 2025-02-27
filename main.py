import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons, TextBox
import sympy as sp

class FractalExplorer:
    def __init__(self):
        # Default paramters for rendring
        self.max_iters = 100
        self.escape_val = 2.0
        self.x_range = (-2.5, 1.5)
        self.y_range = (-1.5, 1.5)
        self.pixels = 500
        self.color_style = 'viridis'
        self.frac_type = 'mandelbrot'
        self.julia_c = complex(-0.7, 0.27)
        
        
        self.setup_plot()
        
    def setup_plot(self):
        plt.style.use('dark_background')
        
        self.fig = plt.figure(figsize=(16/1.33, 9/1.5))
        self.fig.patch.set_facecolor('#121212')
        
        
       
        self.ax = self.fig.add_axes([0.1, 0.15, 0.65, 0.80])
        self.ax.set_title(f"{self.frac_type.capitalize()} Set", color='white')
        
       
        self.setup_controls()
        
       
        self.render_fractal()
        
        # Conect mouse events
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.click_start = None
        
    def setup_controls(self):
       
        slider_height = 0.03  
        slider_width = 0.15

        
        reset_ax = self.fig.add_axes([0.8, 0.85, 0.15, 0.04])
        self.reset_button = Button(reset_ax, 'Reset View', color='#333333', hovercolor='gray')
        self.reset_button.label.set_color('white')
        self.reset_button.on_clicked(self.reset_view)
        
        
        iter_ax = self.fig.add_axes([0.8, 0.70, slider_width, slider_height])
        self.iter_slider = Slider(iter_ax, 'Iterations', 10, 500, valinit=self.max_iters, valstep=10)
        self.iter_slider.on_changed(self.update_iterations)
        iter_ax.tick_params(colors='white')
        
        
        escape_ax = self.fig.add_axes([0.8, 0.65, slider_width, slider_height])
        self.escape_slider = Slider(escape_ax, 'Escape', 1.5, 5.0, valinit=self.escape_val, valstep=0.1)
        self.escape_slider.on_changed(self.update_escape_value)
        escape_ax.tick_params(colors='white')
        
        
        pixels_ax = self.fig.add_axes([0.8, 0.60, slider_width, slider_height])
        self.pixels_box = TextBox(pixels_ax, 'Pixels', initial=str(self.pixels),
                                   color='#333333', hovercolor='gray')
        self.pixels_box.on_submit(self.update_pixels)
        try:
            self.pixels_box.text_disp.set_color('white')
        except Exception:
            pass
        
        
        cmap_ax = self.fig.add_axes([0.8, 0.35, 0.15, 0.19])
        self.color_radio = RadioButtons(cmap_ax, ('vidis', 'plasma', 'magma', 'hot', 'cool'))
        for txt in self.color_radio.labels:
            txt.set_color('white')
            txt.set_fontsize(10)
        self.color_radio.on_clicked(self.change_colormap)
        
        
        type_ax = self.fig.add_axes([0.8, 0.15, 0.15, 0.17])
        self.frac_type_radio = RadioButtons(type_ax, ('Mandelbrot', 'Julia'))
        for txt in self.frac_type_radio.labels:
            txt.set_color('white')
            txt.set_fontsize(15)
        self.frac_type_radio.on_clicked(self.change_fractal_type)
        
        
        save_ax = self.fig.add_axes([0.8, 0.02, 0.15, 0.05])
        self.save_button = Button(save_ax, 'Save Image', color='#333333', hovercolor='gray')
        self.save_button.label.set_color('white')
        self.save_button.on_clicked(self.save_image)
        
        #  Info Display: Coordinates and Julia Constant 
        self.coord_text = self.fig.text(0.11, 0.025, f"View: x={self.x_range}, y={self.y_range}",
                                        fontsize=10, color='white')
        self.julia_text = self.fig.text(0.11, 0.88, f"Julia constant: {self.julia_c}",
                                        fontsize=10, color='white')
        self.julia_text.set_visible(self.frac_type == 'julia')
        
    def mandelbrot_iteration(self, c, max_iter, escape_radius=2.0):
        z = 0
        for i in range(max_iter):
            z = z**2 + c
            if abs(z) > escape_radius:
                return i
        return max_iter
    
    def julia_iteration(self, z, c, max_iter, escape_radius=2.0):
        for i in range(max_iter):
            z = z**2 + c
            if abs(z) > escape_radius:
                return i
        return max_iter
    
    def compute_fractal(self):
        x = np.linspace(self.x_range[0], self.x_range[1], self.pixels)
        y = np.linspace(self.y_range[0], self.y_range[1], self.pixels)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        iters = np.zeros(Z.shape, dtype=int)
        if self.frac_type == 'mandelbrot':
            for i in range(iters.shape[0]):
                for j in range(iters.shape[1]):
                    iters[i, j] = self.mandelbrot_iteration(Z[i, j], self.max_iters, self.escape_val)
        else:
            for i in range(iters.shape[0]):
                for j in range(iters.shape[1]):
                    iters[i, j] = self.julia_iteration(Z[i, j], self.julia_c, self.max_iters, self.escape_val)
        return iters
    
    def render_fractal(self):
        self.ax.clear()
        iters = self.compute_fractal()
        norm_iters = np.log(iters + 1) / np.log(self.max_iters + 1)
        self.ax.imshow(norm_iters, extent=[self.x_range[0], self.x_range[1], self.y_range[0], self.y_range[1]], 
                       cmap=self.color_style, origin='lower', interpolation='bilinear')
        title = f"{self.frac_type.capitalize()} Set"
        if self.frac_type == 'julia':
            title += f" (c = {self.julia_c})"
        self.ax.set_title(title, color='white')
        self.coord_text.set_text(f"View: x={self.x_range}, y={self.y_range}")
        self.julia_text.set_visible(self.frac_type == 'julia')
        self.julia_text.set_text(f"Julia constant: {self.julia_c}")
        plt.draw()
    
    def update_iterations(self, val):
        self.max_iters = int(val)
        self.render_fractal()
    
    def update_escape_value(self, val):
        self.escape_val = float(val)
        self.render_fractal()
    
    def update_pixels(self, text):
        try:
            val = int(text)
            if val > 0:
                self.pixels = val
                self.render_fractal()
            else:
                print("Pixel value must be > 0.")
        except ValueError:
            print("Invalid pixel input. Must be a number.")
    
    def change_colormap(self, label):
        self.color_style = label
        self.render_fractal()
    
    def change_fractal_type(self, label):
        self.frac_type = label
        if label == 'mandelbrot':
            self.reset_view(None)
        else:
            if hasattr(self, 'last_click_pos') and self.frac_type == 'julia':
                x, y = self.last_click_pos
                self.julia_c = complex(x, y)
                self.julia_text.set_text(f"Julia constant: {self.julia_c}")
        self.render_fractal()
    
    def on_click(self, event):
        if event.inaxes == self.ax:
            self.click_start = (event.xdata, event.ydata)
            self.last_click_pos = (event.xdata, event.ydata)
            if event.button == 3 and self.frac_type == 'julia':
                self.julia_c = complex(event.xdata, event.ydata)
                self.julia_text.set_text(f"Julia constant: {self.julia_c}")
                self.render_fractal()
    
    def on_release(self, event):
        if event.inaxes == self.ax and self.click_start:
            if event.button == 1:
                x_start, y_start = self.click_start
                x_end, y_end = event.xdata, event.ydata
                if abs(x_end - x_start) > 0.01 or abs(y_end - y_start) > 0.01:
                    x_min, x_max = min(x_start, x_end), max(x_start, x_end)
                    y_min, y_max = min(y_start, y_end), max(y_start, y_end)
                    self.x_range = (x_min, x_max)
                    self.y_range = (y_min, y_max)
                    self.render_fractal()
                elif self.frac_type == 'mandelbrot':
                    self.julia_c = complex(x_start, y_start)
                    self.julia_text.set_text(f"Julia constant: {self.julia_c}")
                    self.render_fractal()
            self.click_start = None
    
    def reset_view(self, event):
        if self.frac_type == 'mandelbrot':
            self.x_range = (-2.5, 1.5)
            self.y_range = (-1.5, 1.5)
        else:
            self.x_range = (-2.0, 2.0)
            self.y_range = (-2.0, 2.0)
        self.render_fractal()
    
    def save_image(self, event):
        filename = f"{self.frac_type}_{self.color_style}_{self.max_iters}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Image saved as {filename}")
    
    def show(self):
        plt.show()
    
    def symbolic_representation(self):
        z, c = sp.symbols('z c')
        if self.frac_type == 'mandelbrot':
            formula = z**2 + c
            desc = "Mandelbrot set: iterating z = z² + c starting with z = 0."
        else:
            c_val = self.julia_c
            formula = z**2 + c_val
            desc = f"Julia set: iterating z = z² + c where c = {c_val}."
        return formula, desc

def analyze_fractal_formula(formula, var_name='z'):
    z = sp.Symbol(var_name)
    derivative = sp.diff(formula, z)
    critical_points = sp.solve(derivative, z)
    fixed_points_eq = formula - z
    fixed_points = sp.solve(fixed_points_eq, z)
    return {
        "formula": formula,
        "derivative": derivative,
        "critical_points": critical_points,
        "fixed_points": fixed_points
    }

def main():
    explorer = FractalExplorer()
    print("Welcome to the Fractal Explorer!")
    print("\nControls:")
    print("- Left-click and drag: Zoom to selected rectangle")
    print("- Right-click in Julia mode: Change Julia constant")
    print("- Click in Mandelbrot mode: Set Julia constant")
    print("- Use sliders and textbox to adjust iterations, escape limit, and pixel resolution")
    print("- 'Reset View' resets the view")
    print("- 'Save Image' saves current fractal as PNG")
    formula, desc = explorer.symbolic_representation()
    print("\nMath Representation:")
    print(desc)
    print(f"Formula: z → {formula}")
    explorer.show()

if __name__ == "__main__":
    main()
