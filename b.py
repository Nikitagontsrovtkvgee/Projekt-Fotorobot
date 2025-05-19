from tkinter.messagebox import showinfo
import customtkinter as ctk
from tkinter import simpledialog,Canvas
from PIL import Image, ImageTk
import pygame

pildid = {}
objektid = {}
olemas = {}

def toggle_osa(nimi, fail, x, y):
    if olemas.get(nimi):
        canvas.delete(objektid[nimi])
        olemas[nimi] = False
    else:
        pil_img = Image.open(fail).convert("RGBA").resize((400, 400))
        tk_img = ImageTk.PhotoImage(pil_img)
        pildid[tk_img]
        objektid[nimi]=canvas.create_image(x, y, image=tk_img)
        olemas[nimi] = True

def mängi_muusika():
    pygame.mixer.music.play(loops=-1)

def peata_muusika():
    pygame.mixer.music.stop()

def salvesta_nägu():
    failinimi = simpledialog.askstring("Salvesta pilt", "Sisesta faili nimi (ilma laiendita:)")
    if not failinimi:
        return

    lõpp_pilt = Image.new("RGBA", (400, 400), (255, 255, 255, 255))

    for nimi in ["nägu", "otsmik", "silmad", "nina", "suu"]:
        if olemas.get(nimi):
            failitee = {
                "nägu": "alus.png",
                "otsmik": "otsmik1.png",
                "silmad": "silmad1.png",
                "nina": "nian1.png",
                "suu": "suu1.png"
            }.get(nimi)
            if failitee:
                osa = Image.open(failitee).comvert("RGBA").resize((400, 400))
                lõpp_pilt.alpha_composite(osa)

    lõpp_pilt.save(f"{failinimi}.png")
    showinfo("Horaw! :D:", f"faili nimi on {failinimi}.png")

pygame.mixer.init()
pygame.mixer.music.load("opening.mp3")
# ctk.set_appearence_mode("Light")

app= ctk.CTk()
app.geometry("800x500")
app.title("Neo")

canvas= Canvas(app, width=400, height=400, bg="white")
canvas.pack(side="right", padx=10, pady=10)

toggle_osa("nägu", "alus.png", 200, 200)
olemas["nägu"] = True

frame = ctk.CTkFrame(app)
frame.pack(side="left", padx=10, pady=10)
seaded = {
    "width": 150, "height": 40,
    "font": ("Segoe UI Emoji", 32),
    "fg_color": "white",
    "corner_radius": 20
}

ctk.CTkLabel(frame, text="nose", **seaded).pack(pady=5)
ctk.CtkButton(frame, text="ostmik", command=lambda: toggle_osa("otsmil", "otsmi1.png", 200, 200), **seaded.pack(pady=3))

ctk.CtkButton(frame, text="ostmik", command=lambda: toggle_osa("otsmil", "otsmi1.png", 200, 200), **seaded.pack(pady=3))

ctk.CtkButton(frame, text="ostmik", command=lambda: toggle_osa("otsmil", "otsmi1.png", 200, 200), **seaded.pack(pady=3))

ctk.CtkButton(frame, text="ostmik", command=lambda: toggle_osa("otsmil", "otsmi1.png", 200, 200), **seaded.pack(pady=3))

ctk.CtkButton(frame, text="ostmik", command=lambda: toggle_osa("otsmil", "otsmi1.png", 200, 200), **seaded.pack(pady=3))

nupp = ctk.CtkButton(frame, text="salvesta", command=salvesta_nägu,**seaded.pack(pady=3))
nupp.pack(pady=10)

frame_mus = ctk.CtkFrame(frame)
frame_mus.pack(padx=10, pady=10)
ctk.CtkButton(frame_mus, text="mängi muusika", fg_color="#4CAF50", command=mängi_muusika.pack(side="left", pady=10))
ctk.CtkButton(frame_mus, text="peata muusika", fg_color="#4CAF50", command=peata_muusika.pack(side="left", pady=10))

app.mainloop()
