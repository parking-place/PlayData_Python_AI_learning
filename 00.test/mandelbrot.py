import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

class MandelbrotSet(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.zoom_ratio = 1
        self.center_point = (-0.5, 0)
        self.draw_mandelbrot()

    def on_click(self, event):
        x, y = event.x, event.y
        dx = (x - 200) / 200
        dy = (y - 200) / 200
        new_center_x = self.center_point[0] + self.zoom_ratio * dx
        new_center_y = self.center_point[1] - self.zoom_ratio * dy
        self.zoom_ratio *= 0.5
        self.center_point = (new_center_x, new_center_y)
        self.draw_mandelbrot()

    def draw_mandelbrot(self):
        width, height = 400, 400
        iterations = 300
        mandelbrot_array = np.zeros((width, height))

        for w in range(width):
            for h in range(height):
                real = self.center_point[0] - self.zoom_ratio + self.zoom_ratio * 2 * w / width
                imag = self.center_point[1] - self.zoom_ratio + self.zoom_ratio * 2 * h / height
                c = complex(real, imag)
                z = complex(0, 0)
                in_set = 1

                for i in range(iterations):
                    z = z * z + c
                    if abs(z) > 2:
                        in_set = 0
                        break

                mandelbrot_array[h, w] = in_set

        img = Image.fromarray(np.uint8(mandelbrot_array * 255), "L")
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=img, anchor="nw")
        self.canvas.image = img

if __name__ == "__main__":
    app = MandelbrotSet()
    app.mainloop()
