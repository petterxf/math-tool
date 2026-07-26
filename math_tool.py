import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import math


class MathTool:
    def __init__(self, root):
        self.root = root
        self.root.title("数学工具 - 函数图像绘制器")
        self.root.geometry("1200x800")
        
        self.shapes = []
        self.current_color = '#1f77b4'
        
        self.x_min = -10
        self.x_max = 10
        self.y_min = -10
        self.y_max = 10
        
        self.canvas_width = 800
        self.canvas_height = 700
        
        self.setup_ui()
        self.draw_coordinate_system()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        point_frame = ttk.LabelFrame(control_frame, text="添加坐标点", padding=5)
        point_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(point_frame, text="X:").grid(row=0, column=0, padx=2)
        self.point_x = ttk.Entry(point_frame, width=8)
        self.point_x.grid(row=0, column=1, padx=2)
        
        ttk.Label(point_frame, text="Y:").grid(row=0, column=2, padx=2)
        self.point_y = ttk.Entry(point_frame, width=8)
        self.point_y.grid(row=0, column=3, padx=2)
        
        ttk.Button(point_frame, text="添加点", command=self.add_point).grid(row=1, column=0, columnspan=4, pady=5)
        
        circle_frame = ttk.LabelFrame(control_frame, text="添加圆", padding=5)
        circle_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(circle_frame, text="圆心X:").grid(row=0, column=0, padx=2)
        self.circle_x = ttk.Entry(circle_frame, width=8)
        self.circle_x.grid(row=0, column=1, padx=2)
        self.circle_x.insert(0, "0")
        
        ttk.Label(circle_frame, text="圆心Y:").grid(row=0, column=2, padx=2)
        self.circle_y = ttk.Entry(circle_frame, width=8)
        self.circle_y.grid(row=0, column=3, padx=2)
        self.circle_y.insert(0, "0")
        
        ttk.Label(circle_frame, text="半径:").grid(row=1, column=0, padx=2)
        self.circle_r = ttk.Entry(circle_frame, width=8)
        self.circle_r.grid(row=1, column=1, padx=2)
        self.circle_r.insert(0, "1")
        
        ttk.Button(circle_frame, text="添加圆", command=self.add_circle).grid(row=2, column=0, columnspan=4, pady=5)
        
        ellipse_frame = ttk.LabelFrame(control_frame, text="添加椭圆", padding=5)
        ellipse_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ellipse_frame, text="中心X:").grid(row=0, column=0, padx=2)
        self.ellipse_x = ttk.Entry(ellipse_frame, width=8)
        self.ellipse_x.grid(row=0, column=1, padx=2)
        self.ellipse_x.insert(0, "0")
        
        ttk.Label(ellipse_frame, text="中心Y:").grid(row=0, column=2, padx=2)
        self.ellipse_y = ttk.Entry(ellipse_frame, width=8)
        self.ellipse_y.grid(row=0, column=3, padx=2)
        self.ellipse_y.insert(0, "0")
        
        ttk.Label(ellipse_frame, text="长轴a:").grid(row=1, column=0, padx=2)
        self.ellipse_a = ttk.Entry(ellipse_frame, width=8)
        self.ellipse_a.grid(row=1, column=1, padx=2)
        self.ellipse_a.insert(0, "2")
        
        ttk.Label(ellipse_frame, text="短轴b:").grid(row=1, column=2, padx=2)
        self.ellipse_b = ttk.Entry(ellipse_frame, width=8)
        self.ellipse_b.grid(row=1, column=3, padx=2)
        self.ellipse_b.insert(0, "1")
        
        ttk.Button(ellipse_frame, text="添加椭圆", command=self.add_ellipse).grid(row=2, column=0, columnspan=4, pady=5)
        
        color_frame = ttk.LabelFrame(control_frame, text="颜色设置", padding=5)
        color_frame.pack(fill=tk.X, pady=5)
        
        self.color_label = tk.Label(color_frame, text="当前颜色", bg=self.current_color, width=15, fg='white')
        self.color_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(color_frame, text="选择颜色", command=self.choose_color).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.LabelFrame(control_frame, text="图形列表", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.shape_listbox = tk.Listbox(list_frame, height=10)
        self.shape_listbox.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="删除选中", command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="清空全部", command=self.clear_all).pack(side=tk.LEFT, padx=2)
        
        view_frame = ttk.LabelFrame(control_frame, text="视图控制", padding=5)
        view_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(view_frame, text="X范围:").grid(row=0, column=0, padx=2)
        self.x_min_entry = ttk.Entry(view_frame, width=6)
        self.x_min_entry.grid(row=0, column=1, padx=2)
        self.x_min_entry.insert(0, "-10")
        
        ttk.Label(view_frame, text="到").grid(row=0, column=2, padx=2)
        self.x_max_entry = ttk.Entry(view_frame, width=6)
        self.x_max_entry.grid(row=0, column=3, padx=2)
        self.x_max_entry.insert(0, "10")
        
        ttk.Label(view_frame, text="Y范围:").grid(row=1, column=0, padx=2)
        self.y_min_entry = ttk.Entry(view_frame, width=6)
        self.y_min_entry.grid(row=1, column=1, padx=2)
        self.y_min_entry.insert(0, "-10")
        
        ttk.Label(view_frame, text="到").grid(row=1, column=2, padx=2)
        self.y_max_entry = ttk.Entry(view_frame, width=6)
        self.y_max_entry.grid(row=1, column=3, padx=2)
        self.y_max_entry.insert(0, "10")
        
        ttk.Button(view_frame, text="应用范围", command=self.apply_range).grid(row=2, column=0, columnspan=4, pady=5)
        ttk.Button(view_frame, text="自动适应", command=self.auto_fit).grid(row=3, column=0, columnspan=4, pady=2)
        
        canvas_frame = ttk.LabelFrame(main_frame, text="坐标系", padding=5)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        
    def on_canvas_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.draw_coordinate_system()
        
    def world_to_screen(self, x, y):
        margin = 50
        plot_width = self.canvas_width - 2 * margin
        plot_height = self.canvas_height - 2 * margin
        
        sx = margin + (x - self.x_min) / (self.x_max - self.x_min) * plot_width
        sy = self.canvas_height - margin - (y - self.y_min) / (self.y_max - self.y_min) * plot_height
        
        return sx, sy
    
    def screen_to_world_length_x(self, length):
        margin = 50
        plot_width = self.canvas_width - 2 * margin
        return length / plot_width * (self.x_max - self.x_min)
    
    def screen_to_world_length_y(self, length):
        margin = 50
        plot_height = self.canvas_height - 2 * margin
        return length / plot_height * (self.y_max - self.y_min)
        
    def draw_coordinate_system(self):
        self.canvas.delete("all")
        
        margin = 50
        plot_width = self.canvas_width - 2 * margin
        plot_height = self.canvas_height - 2 * margin
        
        self.canvas.create_rectangle(margin, margin, 
                                     self.canvas_width - margin, 
                                     self.canvas_height - margin,
                                     outline='gray', width=1)
        
        ox, oy = self.world_to_screen(0, 0)
        
        if self.x_min <= 0 <= self.x_max:
            self.canvas.create_line(ox, margin, ox, self.canvas_height - margin, fill='black', width=1)
        
        if self.y_min <= 0 <= self.y_max:
            self.canvas.create_line(margin, oy, self.canvas_width - margin, oy, fill='black', width=1)
        
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        
        x_step = self.calculate_step(x_range)
        y_step = self.calculate_step(y_range)
        
        x = math.ceil(self.x_min / x_step) * x_step
        while x <= self.x_max:
            if abs(x) > 1e-10:
                sx, _ = self.world_to_screen(x, 0)
                self.canvas.create_line(sx, margin, sx, self.canvas_height - margin, fill='lightgray', width=1, dash=(2, 4))
                _, sy = self.world_to_screen(0, 0)
                if self.y_min <= 0 <= self.y_max:
                    self.canvas.create_text(sx, sy + 15, text=f'{x:.1f}', font=('Arial', 8))
            x += x_step
        
        y = math.ceil(self.y_min / y_step) * y_step
        while y <= self.y_max:
            if abs(y) > 1e-10:
                _, sy = self.world_to_screen(0, y)
                self.canvas.create_line(margin, sy, self.canvas_width - margin, sy, fill='lightgray', width=1, dash=(2, 4))
                sx, _ = self.world_to_screen(0, 0)
                if self.x_min <= 0 <= self.x_max:
                    self.canvas.create_text(sx - 15, sy, text=f'{y:.1f}', font=('Arial', 8))
            y += y_step
        
        self.canvas.create_text(self.canvas_width - margin - 20, oy - 15, text='X', font=('Arial', 10, 'bold'))
        self.canvas.create_text(ox + 15, margin + 15, text='Y', font=('Arial', 10, 'bold'))
        
        self.draw_shapes()
        
    def calculate_step(self, range_val):
        ideal_steps = 10
        raw_step = range_val / ideal_steps
        magnitude = 10 ** math.floor(math.log10(raw_step))
        normalized = raw_step / magnitude
        
        if normalized < 1.5:
            step = magnitude
        elif normalized < 3:
            step = 2 * magnitude
        elif normalized < 7:
            step = 5 * magnitude
        else:
            step = 10 * magnitude
        
        return step
        
    def draw_shapes(self):
        for shape in self.shapes:
            if shape['type'] == 'point':
                self.draw_point(shape)
            elif shape['type'] == 'circle':
                self.draw_circle(shape)
            elif shape['type'] == 'ellipse':
                self.draw_ellipse(shape)
                
    def draw_point(self, shape):
        sx, sy = self.world_to_screen(shape['x'], shape['y'])
        r = 5
        self.canvas.create_oval(sx - r, sy - r, sx + r, sy + r, fill=shape['color'], outline=shape['color'])
        self.canvas.create_text(sx + 10, sy - 10, text=f"({shape['x']:.1f}, {shape['y']:.1f})", 
                               font=('Arial', 9), anchor='w', fill=shape['color'])
        
    def draw_circle(self, shape):
        cx, cy = self.world_to_screen(shape['x'], shape['y'])
        
        margin = 50
        plot_width = self.canvas_width - 2 * margin
        plot_height = self.canvas_height - 2 * margin
        
        rx = shape['r'] / (self.x_max - self.x_min) * plot_width
        ry = shape['r'] / (self.y_max - self.y_min) * plot_height
        
        self.canvas.create_oval(cx - rx, cy - ry, cx + rx, cy + ry, outline=shape['color'], width=2)
        
        r = 3
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=shape['color'], outline=shape['color'])
        
    def draw_ellipse(self, shape):
        cx, cy = self.world_to_screen(shape['x'], shape['y'])
        
        margin = 50
        plot_width = self.canvas_width - 2 * margin
        plot_height = self.canvas_height - 2 * margin
        
        rx = shape['a'] / (self.x_max - self.x_min) * plot_width
        ry = shape['b'] / (self.y_max - self.y_min) * plot_height
        
        self.canvas.create_oval(cx - rx, cy - ry, cx + rx, cy + ry, outline=shape['color'], width=2)
        
        r = 3
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=shape['color'], outline=shape['color'])
        
    def add_point(self):
        try:
            x = float(self.point_x.get())
            y = float(self.point_y.get())
            
            shape = {
                'type': 'point',
                'x': x,
                'y': y,
                'color': self.current_color
            }
            self.shapes.append(shape)
            self.shape_listbox.insert(tk.END, f"点 ({x}, {y})")
            self.draw_coordinate_system()
            
            self.point_x.delete(0, tk.END)
            self.point_y.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的坐标值")
            
    def add_circle(self):
        try:
            x = float(self.circle_x.get())
            y = float(self.circle_y.get())
            r = float(self.circle_r.get())
            
            if r <= 0:
                messagebox.showerror("错误", "半径必须大于0")
                return
            
            shape = {
                'type': 'circle',
                'x': x,
                'y': y,
                'r': r,
                'color': self.current_color
            }
            self.shapes.append(shape)
            self.shape_listbox.insert(tk.END, f"圆 中心({x}, {y}) r={r}")
            self.draw_coordinate_system()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
            
    def add_ellipse(self):
        try:
            x = float(self.ellipse_x.get())
            y = float(self.ellipse_y.get())
            a = float(self.ellipse_a.get())
            b = float(self.ellipse_b.get())
            
            if a <= 0 or b <= 0:
                messagebox.showerror("错误", "长轴和短轴必须大于0")
                return
            
            shape = {
                'type': 'ellipse',
                'x': x,
                'y': y,
                'a': a,
                'b': b,
                'color': self.current_color
            }
            self.shapes.append(shape)
            self.shape_listbox.insert(tk.END, f"椭圆 中心({x}, {y}) a={a} b={b}")
            self.draw_coordinate_system()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
            
    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)
        if color[1]:
            self.current_color = color[1]
            self.color_label.config(bg=self.current_color)
            
    def delete_selected(self):
        selection = self.shape_listbox.curselection()
        if selection:
            index = selection[0]
            self.shape_listbox.delete(index)
            del self.shapes[index]
            self.draw_coordinate_system()
            
    def clear_all(self):
        self.shapes.clear()
        self.shape_listbox.delete(0, tk.END)
        self.draw_coordinate_system()
        
    def apply_range(self):
        try:
            self.x_min = float(self.x_min_entry.get())
            self.x_max = float(self.x_max_entry.get())
            self.y_min = float(self.y_min_entry.get())
            self.y_max = float(self.y_max_entry.get())
            
            if self.x_min >= self.x_max or self.y_min >= self.y_max:
                messagebox.showerror("错误", "最小值必须小于最大值")
                return
                
            self.draw_coordinate_system()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
        
    def auto_fit(self):
        if not self.shapes:
            self.x_min = -10
            self.x_max = 10
            self.y_min = -10
            self.y_max = 10
            self.x_min_entry.delete(0, tk.END)
            self.x_min_entry.insert(0, "-10")
            self.x_max_entry.delete(0, tk.END)
            self.x_max_entry.insert(0, "10")
            self.y_min_entry.delete(0, tk.END)
            self.y_min_entry.insert(0, "-10")
            self.y_max_entry.delete(0, tk.END)
            self.y_max_entry.insert(0, "10")
            self.draw_coordinate_system()
            return
        
        x_coords = []
        y_coords = []
        
        for shape in self.shapes:
            if shape['type'] == 'point':
                x_coords.append(shape['x'])
                y_coords.append(shape['y'])
            elif shape['type'] == 'circle':
                x_coords.extend([shape['x'] - shape['r'], shape['x'] + shape['r']])
                y_coords.extend([shape['y'] - shape['r'], shape['y'] + shape['r']])
            elif shape['type'] == 'ellipse':
                x_coords.extend([shape['x'] - shape['a'], shape['x'] + shape['a']])
                y_coords.extend([shape['y'] - shape['b'], shape['y'] + shape['b']])
        
        if x_coords and y_coords:
            margin = 1.5
            self.x_min = min(x_coords) - margin
            self.x_max = max(x_coords) + margin
            self.y_min = min(y_coords) - margin
            self.y_max = max(y_coords) + margin
            
            self.x_min_entry.delete(0, tk.END)
            self.x_min_entry.insert(0, f"{self.x_min:.1f}")
            self.x_max_entry.delete(0, tk.END)
            self.x_max_entry.insert(0, f"{self.x_max:.1f}")
            self.y_min_entry.delete(0, tk.END)
            self.y_min_entry.insert(0, f"{self.y_min:.1f}")
            self.y_max_entry.delete(0, tk.END)
            self.y_max_entry.insert(0, f"{self.y_max:.1f}")
            
        self.draw_coordinate_system()


def main():
    root = tk.Tk()
    app = MathTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()
