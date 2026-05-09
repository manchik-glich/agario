import customtkinter as ctk
import tkinter as tk
import random

from connection import Launcher

app = Launcher()
app.run
host = app.host
nickname = app.username
port = app.port

print(host,port,nickname)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("520x380")
        self.title("agario.launcher")
        self.resizable(False, False)

        self.bubbles = []

        self.username = None
        self.host = None
        self.port = None

        self.setup_ui()
        self.create_background()
        self.animate()

    def setup_ui(self):
        self.root = ctk.CTkFrame(self, corner_radius=0)
        self.root.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.root, width=520, height=380, highlightthickness=0, bg="#0f172a")
        self.canvas.place(x=0, y=0)

        self.frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color="#111827")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(
            self.frame,
            text="AGARIO LAUNCHER",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=15)

        self.nickname_entry = ctk.CTkEntry(self.frame, placeholder_text="Ваш нік", height=40)
        self.nickname_entry.pack(pady=8, padx=25, fill="x")

        self.ip_entry = ctk.CTkEntry(self.frame, placeholder_text="IP сервера", height=40)
        self.ip_entry.pack(pady=8, padx=25, fill="x")

        self.port_entry = ctk.CTkEntry(self.frame, placeholder_text="Порт", height=40)
        self.port_entry.pack(pady=8, padx=25, fill="x")

        self.status = ctk.CTkLabel(self.frame, text="")
        self.status.pack(pady=5)

        self.button = ctk.CTkButton(
            self.frame,
            text="УВІЙТИ",
            height=45,
            corner_radius=12,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.connect
        )
        self.button.pack(pady=15, padx=25, fill="x")

    def create_background(self):
        for _ in range(20):
            x = random.randint(0, 520)
            y = random.randint(0, 380)
            r = random.randint(10, 30)

            bubble = self.canvas.create_oval(
                x, y, x + r, y + r,
                outline="#3b82f6",
                width=2
            )

            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)

            self.bubbles.append([bubble, dx, dy])

    def animate(self):
        for i in range(len(self.bubbles)):
            b, dx, dy = self.bubbles[i]

            coords = self.canvas.coords(b)
            if not coords:
                continue

            x1, y1, x2, y2 = coords

            self.canvas.move(b, dx, dy)

            if x1 <= 0 or x2 >= 520:
                dx *= -1
            if y1 <= 0 or y2 >= 380:
                dy *= -1

            self.bubbles[i][1] = dx
            self.bubbles[i][2] = dy

        self.after(30, self.animate)

    def connect(self):
        self.username = self.entry_name.get()
        self.host = self.entry_ip.get()
        self.port = int(self.entry_port.get())

        self.app.destroy()

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
    