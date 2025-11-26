import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from config import *

db_users = {("admin", "123"): "admin", ("user", "122"): "user"}


class OrderCard(tk.Frame):
    def __init__(self, parent, order_number):
        super().__init__(parent, bg="white", bd=2, relief="ridge")
        self.pack(padx=100, pady=10, fill="x", anchor="center")

        img = Image.new("RGB", (120, 120), "gray")
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(self, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(side="left", padx=10, pady=10)

        info = tk.Frame(self, bg="white")
        info.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        tk.Label(info, text=f"Заказ №{order_number}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(info, text="Статус заказа: В обработке", bg="white").pack(anchor="w")
        tk.Label(info, text="Адрес пункта выдачи: Текст адреса", bg="white").pack(anchor="w")
        tk.Label(info, text="Дата заказа: 25.11.2025", bg="white").pack(anchor="w")
        tk.Label(info, text="Цена: 3490 руб.", font=("Arial", 12, "bold"), fg="green", bg="white").pack(anchor="w")

        discount = tk.Frame(self, bg="#fafafa", bd=1, relief="solid", width=140, height=140)
        discount.pack(side="right", padx=15, pady=10)
        discount.pack_propagate(False)
        tk.Label(discount, text="Действующая\nскидка", font=("Arial", 11), bg="#fafafa").pack(pady=(20, 5))
        tk.Label(discount, text="-15%", font=("Arial", 24, "bold"), fg="red", bg="#fafafa").pack()


class OrdersWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.app = root

        tk.Label(self, text="Гость", font=("Arial", 20, "bold"), bg="#e6e6e6").pack(pady=10)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#e6e6e6")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.items_frame = tk.Frame(canvas, bg="#e6e6e6")
        canvas.create_window((0, 0), window=self.items_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.items_frame.bind("<Configure>", on_frame_configure)

        for i in range(1, 21):
            OrderCard(self.items_frame, i)


class LoginWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.app = root
        tk.Label(self, text="Логин").pack()
        self.login = tk.Entry(self)
        self.login.pack()
        tk.Label(self, text="Пароль").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()
        tk.Button(self, text="Войти", command=self.loggin).pack()
        tk.Button(self, text="Войти как гость", command=self.loggin_as_guest).pack(pady=10)

    def deleteframe(self):
        self.pack_forget()  
        self.destroy()


    def loggin(self):
        role_key = (self.login.get(), self.password.get())
        if role_key in db_users:
            self.app.current_role = db_users[role_key]
            self.deleteframe()
            self.app.orders_window.pack(fill="both", expand=True)

    def loggin_as_guest(self):
        self.app.current_role = "guest"
        self.deleteframe()
        self.app.orders_window.pack(fill="both", expand=True)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x600")
        self.current_role = None
        self.loginFrame = LoginWindow(self)
        self.loginFrame.pack()
        self.orders_window = OrdersWindow(self)


if __name__ == "__main__":
    root = App()
    root.mainloop()
