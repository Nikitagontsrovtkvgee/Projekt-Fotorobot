import tkinter as tk
from tkinter import Checkbutton, Canvas, IntVar, messagebox
from PIL import Image, ImageTk
import os

# Глобальные переменные
pildid = {}       # Для хранения PhotoImage
objektid = {}     # ID объектов на Canvas
olemas = {}       # Какие части выбраны
canvas = None     # Сюда добавим позже Canvas

# Конфигурация частей лица
nao_osad = {
    "näo ovaal": ("naovorm1.png", 200, 200),
    "silmad": ("silmad1.png", 200, 200),
    "nina": ("nina1.png", 200, 200),
    "suu": ("suu1.png", 200, 200),
    "kulmud": ("kulmud1.png", 200, 200)
}

def toggle_osa(nimi):
    """Добавляет или убирает часть лица"""
    if olemas.get(nimi):
        canvas.delete(objektid[nimi])
        olemas[nimi] = False
    else:
        fail, x, y = nao_osad[nimi]
        if not os.path.exists(fail):
            messagebox.showwarning("Ошибка", f"Файл не найден: {fail}")
            return
        img = Image.open(fail).convert("RGBA").resize((400, 400))
        tk_img = ImageTk.PhotoImage(img)
        pildid[nimi] = tk_img
        objektid[nimi] = canvas.create_image(x, y, image=tk_img)
        olemas[nimi] = True

def salvesta_robot():
    """Сохраняет текущую комбинацию"""
    valitud = [nimi for nimi in nao_osad if olemas.get(nimi)]
    with open("fotorobotid.txt", "a", encoding="utf-8") as f:
        f.write(",".join(valitud) + "\n")
    messagebox.showinfo("Сохранено", "Фоторобот сохранён!")

def lae_viimane_robot():
    """Загружает последний сохранённый фоторобот"""
    if not os.path.exists("fotorobotid.txt"):
        messagebox.showinfo("Нет данных", "Сохранений пока нет.")
        return
    with open("fotorobotid.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return
        viimane = lines[-1].strip().split(",")

    # Удаляем старые части
    for nimi in olemas:
        if olemas[nimi]:
            canvas.delete(objektid.get(nimi))
            olemas[nimi] = False

    # Добавляем заново
    for nimi in viimane:
        if nimi in nao_osad:
            toggle_osa(nimi)

def loo_gui():
    """Создаёт окно"""
    global canvas
    root = tk.Tk()
    root.title("Fotorobot")
    root.geometry("800x500")

    # Левая панель с Checkbuttons
    frame = tk.Frame(root)
    frame.pack(side="left", padx=10, pady=10)

    variablid = {}
    for nimi in nao_osad:
        var = IntVar()
        chk = Checkbutton(frame, text=nimi, variable=var,
                          command=lambda n=nimi: toggle_osa(n))
        chk.pack(anchor="w")
        variablid[nimi] = var

    tk.Button(frame, text="💾 Сохранить", command=salvesta_robot).pack(pady=10)
    tk.Button(frame, text="📂 Показать последний", command=lae_viimane_robot).pack(pady=5)

    # Правая часть – Canvas
    canvas = Canvas(root, width=400, height=400, bg="white")
    canvas.pack(side="right", padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    # Инициализация переменных
    for k in nao_osad:
        olemas[k] = False
    loo_gui()
