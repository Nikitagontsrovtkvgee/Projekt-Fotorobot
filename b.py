from tkinter import *
from PIL import Image, ImageTk
import os
import random

# Папки с изображениями по категориям
ELEMENTS = {
    "Лицо": "face",
    "Глаза": "eyes",
    "Нос": "nose",
    "Рот": "mouth",
    "Волосы": "hair"
}

# Словарь для хранения выбранных файлов
selected_parts = {}

# Главный интерфейс
root = Tk()
root.title("Фоторобот")
root.geometry("600x400")

# Левая панель — выбор частей
frame_left = Frame(root)
frame_left.pack(side=LEFT, padx=10, pady=10)

# Правая панель — холст для отображения
canvas = Canvas(root, width=200, height=250, bg="white")
canvas.pack(side=RIGHT, padx=10, pady=10)

# Для хранения изображений
image_refs = {}

# Функция для отображения фоторобота
def show_robot():
    canvas.delete("all")
    y_offset = 0
    image_refs.clear()
    for part, folder in ELEMENTS.items():
        if part in selected_parts:
            path = os.path.join(folder, selected_parts[part])
            if os.path.exists(path):
                img = Image.open(path).resize((200, 250), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor=NW, image=img_tk)
                image_refs[part] = img_tk

# Функция при выборе элемента
def update_part(part, var, folder):
    files = os.listdir(folder)
    if var.get() == 1:
        selected_parts[part] = random.choice(files)
    else:
        selected_parts.pop(part, None)
    show_robot()

# Checkbuttons для каждого элемента
for part_name, folder_name in ELEMENTS.items():
    var = IntVar()
    chk = Checkbutton(frame_left, text=part_name, variable=var,
                      command=lambda p=part_name, v=var, f=folder_name: update_part(p, v, f))
    chk.pack(anchor=W)

# Файл для сохранения данных
SAVE_FILE = "fotorobotid.txt"

# Сохраняем текущую сборку
def save_robot():
    with open(SAVE_FILE, "a", encoding="utf-8") as f:
        line = ", ".join(selected_parts.get(part, "-") for part in ELEMENTS)
        f.write(line + "\n")

# Загружаем последний сохранённый робот
def load_last_robot():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last = lines[-1].strip().split(", ")
                for i, part in enumerate(ELEMENTS):
                    if last[i] != "-":
                        selected_parts[part] = last[i]
                    else:
                        selected_parts.pop(part, None)
                show_robot()

# Кнопки управления
Button(frame_left, text="💾 Сохранить фоторобот", command=save_robot).pack(pady=5)
Button(frame_left, text="📂 Загрузить последний", command=load_last_robot).pack(pady=5)

root.mainloop()
