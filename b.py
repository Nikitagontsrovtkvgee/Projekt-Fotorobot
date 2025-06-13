import os
import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from collections import OrderedDict

class FotorobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fotorobot")
        
        # Установка размеров окна
        self.root.geometry("800x600")
        
        # Категории (все элементы будут на одном месте)
        self.categories = OrderedDict([
            ("skinColor", {"folder": "skinColor"}),
            ("T-shirt", {"folder": "T-shirt"}),
            ("pants", {"folder": "pants"}),
            ("boots", {"folder": "boots"}),
            ("Hairs", {"folder": "Hairs"}),
        ])
        
        # Общие координаты и размер для всех элементов
        self.image_x = 300
        self.image_y = 50
        self.image_size = (300, 500)
        
        self.selected_indices = {}
        self.image_refs = {}
        
        # Проверка существования папок
        self.check_folders()
        
        self.create_widgets()
        self.update_canvas()

    def check_folders(self):
        """Проверяет наличие необходимых папок"""
        for category in self.categories:
            folder = self.categories[category]["folder"]
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Создана папка: {folder}")

    def create_widgets(self):
        # Главный фрейм
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Фрейм управления (левая часть)
        control_frame = tk.Frame(main_frame, width=200)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Заголовок
        tk.Label(control_frame, text="Fotorobot", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Разделитель
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Элементы выбора для каждой категории
        for category in self.categories:
            frame = tk.Frame(control_frame)
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=category, width=10, anchor='w').pack(side=tk.LEFT)
            
            self.selected_indices[category] = tk.IntVar(value=1)
            
            # Spinbox для выбора вариантов
            spinbox = tk.Spinbox(frame, from_=1, to=5, width=5, 
                               textvariable=self.selected_indices[category],
                               command=lambda cat=category: self.on_selection_change(cat))
            spinbox.pack(side=tk.RIGHT)
        
        # Разделитель
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Кнопки управления
        buttons_frame = tk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X)
        
        tk.Button(buttons_frame, text="Случайный персонаж", command=self.randomize,
                bg="#e0e0ff", activebackground="#c0c0ff").pack(fill=tk.X, pady=5)
        tk.Button(buttons_frame, text="Сохранить", command=self.save_robot,
                bg="#ffe0e0", activebackground="#ffc0c0").pack(fill=tk.X, pady=5)
        tk.Button(buttons_frame, text="Сбросить", command=self.reset,
                bg="#e0ffe0", activebackground="#c0ffc0").pack(fill=tk.X, pady=5)
        
        # Canvas для отображения персонажа (правая часть)
        self.canvas = tk.Canvas(main_frame, width=600, height=550, bg='white')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def on_selection_change(self, category):
        """Обработчик изменения выбора"""
        self.update_canvas()

    def load_image(self, category, index):
        """Загружает изображение для указанной категории и индекса"""
        folder = self.categories[category]["folder"]
        path = os.path.join(folder, f"{folder}{index}.png")
        
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGBA")
                img = img.resize(self.image_size)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
                return None
        else:
            print(f"Файл не найден: {path}")
            return None

    def update_canvas(self):
        """Обновляет изображение на Canvas"""
        self.canvas.delete("all")
        
        # Создаем базовое изображение (прозрачное)
        base_img = Image.new("RGBA", self.image_size, (0, 0, 0, 0))
        
        # Комбинируем все выбранные элементы
        for category in self.categories:
            index = self.selected_indices[category].get()
            img = self.load_image(category, index)
            
            if img:
                # Накладываем изображение на базовое
                img_pil = ImageTk.getimage(img)
                base_img = Image.alpha_composite(base_img, img_pil)
        
        # Отображаем итоговое изображение
        if base_img:
            final_img = ImageTk.PhotoImage(base_img)
            self.image_refs["final"] = final_img
            self.canvas.create_image(self.image_x, self.image_y, anchor=tk.NW, image=final_img)

    def randomize(self):
        """Случайный выбор всех частей персонажа"""
        for category in self.categories:
            rnd = random.randint(1, 5)
            self.selected_indices[category].set(rnd)
        self.update_canvas()

    def reset(self):
        """Сброс к начальным значениям"""
        for category in self.categories:
            self.selected_indices[category].set(1)
        self.update_canvas()

    def save_robot(self):
        """Сохраняет текущую комбинацию в файл"""
        selected = []
        for category in self.categories:
            index = self.selected_indices[category].get()
            selected.append(f"{category}{index}")
        
        try:
            with open("fotorobotid.txt", "a") as f:
                f.write(", ".join(selected) + "\n")
            messagebox.showinfo("Сохранено", "Комбинация сохранена в fotorobotid.txt")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FotorobotApp(root)
    root.mainloop()
