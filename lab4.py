import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Лабораторная работа №4")
        self.pack()
        self.create_widgets()
        self.transformations = []


    def create_widgets(self):
        button_width = 24

        self.image_frame = tk.Frame(self)
        self.image_frame.pack(side="top", fill="both", expand=True)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x")

        self.left_button_frame = tk.Frame(self.button_frame)
        self.left_button_frame.pack(side="left", fill="x", expand=True)

        self.open_button = tk.Button(self.left_button_frame, width=button_width)
        self.open_button["text"] = "Изображение"
        self.open_button["command"] = self.load_image
        self.open_button.pack(side="top")

        self.affine_button = tk.Button(self.left_button_frame, width=button_width)
        self.affine_button["text"] = "Поворот и масштабирование"
        self.affine_button["command"] = self.apply_affine_transformation
        self.affine_button.pack(side="top")

        self.restore_button = tk.Button(self.left_button_frame, width=button_width)
        self.restore_button["text"] = "Восстановить исходник"
        self.restore_button["command"] = self.restore_original
        self.restore_button.pack(side="top")

        self.right_button_frame = tk.Frame(self.button_frame)
        self.right_button_frame.pack(side="right", fill="x", expand=True)

        self.nonlinear_button = tk.Button(self.right_button_frame, width=button_width)
        self.nonlinear_button["text"] = "Нелинейные преобразования"
        self.nonlinear_button["command"] = self.apply_nonlinear_transformation
        self.nonlinear_button.pack(side="top")

        self.save_button = tk.Button(self.right_button_frame, width=button_width)
        self.save_button["text"] = "Сохранить изображение"
        self.save_button["command"] = self.save_result
        self.save_button.pack(side="top")

        self.original_image = None
        self.transformed_image = None

    def load_image(self):
        image_path = filedialog.askopenfilename()
        self.source_image = Image.open(image_path)
        self.processed_image = self.source_image.copy()
        self.display_image = ImageTk.PhotoImage(self.processed_image)
        self.image_label.config(image=self.display_image)
        self.transformation_history = []
    
    
    def apply_affine_transformation(self):
        if self.processed_image:
            rotation_angle = 10
            scale_factor = 1.2

            width, height = self.processed_image.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

            self.processed_image = self.processed_image.resize((new_width, new_height), Image.LANCZOS)
            self.processed_image = self.processed_image.rotate(rotation_angle, expand=True)
            self.processed_image = self.processed_image.resize((width, height), Image.LANCZOS)
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            self.image_label.config(image=self.display_image)
            self.transformation_history.append(("affine", rotation_angle, scale_factor))
    
    def apply_nonlinear_transformation(self):
        if self.processed_image:
            pixel_array = np.array(self.processed_image)
            width, height = pixel_array.shape[1], pixel_array.shape[0]
            transformed_array = np.zeros_like(pixel_array)
            coordinate_map = []
            for i in range(height):
                for j in range(width):
                    x_prime = np.sinh(j)
                    y_prime = i
                    if np.isinf(np.sinh(x_prime)):
                        i_prime = 0
                    else:
                        i_prime = int(np.sinh(x_prime))
                    j_prime = int(y_prime)
                    if 0 <= i_prime < height and 0 <= j_prime < width:
                        transformed_array[i, j] = pixel_array[i_prime, j_prime]
                        coordinate_map.append((i_prime, j_prime))
            self.processed_image = Image.fromarray(transformed_array)
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            self.image_label.config(image=self.display_image)
            self.transformation_history.append(("nonlinear", coordinate_map))
    
    def save_result(self):
        if self.processed_image:
            filename, file_extension = os.path.splitext(self.source_image.filename)
            output_filename = f"{filename}_out.jpg"
            self.processed_image.save(output_filename)
    
    def restore_original(self):
        if self.transformation_history:
            for transformation in reversed(self.transformation_history):
                if transformation[0] == "affine":
                    rotation_angle, scale_factor = transformation[1:]
                    width, height = self.processed_image.size
                    self.processed_image = self.processed_image.resize((int(width), int(height)), Image.LANCZOS)
                    self.processed_image = self.processed_image.rotate(-rotation_angle, expand=True)
                    self.processed_image = self.processed_image.resize((width, height), Image.LANCZOS)
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            self.image_label.config(image=self.display_image)
            self.transformation_history = []
    
root = tk.Tk()
app = Application(master=root)
app.mainloop()