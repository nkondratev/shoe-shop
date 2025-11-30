import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from config import *

db_users = {
    ("admin", "123"): "admin",
    ("manager", "321"): "manager",
    ("user", "122"): "user",
}

class EditOrderWindow(tk.Toplevel):
    def __init__(self, parent_card):
        super().__init__(parent_card)
        self.card = parent_card

        self.title(f"Редактирование товара №{self.card.product_number}")
        self.geometry("400x350")

        tk.Label(self, text=f"Редактирование товара №{self.card.product_number}", font=("Times New Roman", 16, "bold")).pack(pady=10)

        fields = [
            ("Категория | Наименование", "name_text"),
            ("Описание", "desc_text"),
            ("Производитель", "vendor_text"),
            ("Поставщик", "provider_text"),
            ("Цена", "price_value"),
            ("Единица измерения", "unit_text"),
            ("Количество на складе", "count_value"),
        ]

        self.entries = {}

        for label, attr in fields:
            tk.Label(self, text=label + ":", font=("Times New Roman", 12)).pack(anchor="w", padx=20)
            entry = tk.Entry(self, font=("Times New Roman", 12))
            entry.insert(0, str(getattr(self.card, attr)))
            entry.pack(fill="x", padx=20)
            self.entries[attr] = entry

        tk.Button(self, text="Сохранить", font=("Times New Roman", 12, "bold"), bg="lightgreen", command=self.save_changes).pack(pady=15)

    def save_changes(self):
        try:
            price = float(self.entries["price_value"].get())
            count = int(self.entries["count_value"].get())
        except ValueError:
            messagebox.showerror("Ошибка", "Цена и количество должны быть числами!")
            return

        for key, entry in self.entries.items():
            if key not in ("price_value", "count_value") and not entry.get().strip():
                messagebox.showerror("Ошибка", f"Поле '{key}' не может быть пустым!")
                return

        self.card.price_value = price
        self.card.count_value = count
        self.card.name_text = self.entries["name_text"].get()
        self.card.desc_text = self.entries["desc_text"].get()
        self.card.vendor_text = self.entries["vendor_text"].get()
        self.card.provider_text = self.entries["provider_text"].get()
        self.card.unit_text = self.entries["unit_text"].get()

        self.card.name_label.config(text=self.card.name_text)
        self.card.desc_label.config(text=f"Описание: {self.card.desc_text}")
        self.card.vendor_label.config(text=f"Производитель: {self.card.vendor_text}")
        self.card.provider_label.config(text=f"Поставщик: {self.card.provider_text}")
        self.card.price_label.config(text=f"Цена: {self.card.price_value:.2f} руб.")
        self.card.unit_label.config(text=f"Ед. изм.: {self.card.unit_text}")
        self.card.count_label.config(text=f"Количество: {self.card.count_value}")

        if hasattr(self.master, 'apply_filters'):
            self.master.apply_filters()
        self.destroy()

class ProductCard(tk.Frame):
    def __init__(self, parent, product_number, role):
        super().__init__(parent, bg="white", bd=2, relief="ridge", padx=100)
        self.product_number = product_number
        self.role = role

        self.name_text = f"Категория | Наименование {product_number}"
        self.desc_text = f"Описание товара {product_number}"
        self.vendor_text = f"Производитель {product_number % 3}"
        self.provider_text = f"Поставщик {product_number % 5}"
        self.price_value = 1000 + product_number * 10
        self.unit_text = "шт."
        self.count_value = 50 + product_number

        self.pack(padx=100, pady=10, fill="x", anchor="center")

        img = Image.new("RGB", (120, 120), "gray")
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(self, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(side="left", padx=10, pady=10)

        info = tk.Frame(self, bg="white")
        info.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        self.name_label = tk.Label(info, text=self.name_text, font=("Times New Roman", 14, "bold"), bg="white")
        self.name_label.pack(anchor="w")

        self.desc_label = tk.Label(info, text=f"Описание: {self.desc_text}", font=("Times New Roman", 12), bg="white")
        self.desc_label.pack(anchor="w")

        self.vendor_label = tk.Label(info, text=f"Производитель: {self.vendor_text}", font=("Times New Roman", 12), bg="white")
        self.vendor_label.pack(anchor="w")

        self.provider_label = tk.Label(info, text=f"Поставщик: {self.provider_text}", font=("Times New Roman", 12), bg="white")
        self.provider_label.pack(anchor="w")

        self.price_label = tk.Label(info, text=f"Цена: {self.price_value:.2f} руб.", font=("Times New Roman", 14, "bold"), fg="green", bg="white")
        self.price_label.pack(anchor="w")

        self.unit_label = tk.Label(info, text=f"Ед. изм.: {self.unit_text}", font=("Times New Roman", 12), bg="white")
        self.unit_label.pack(anchor="w")

        self.count_label = tk.Label(info, text=f"Количество: {self.count_value}", font=("Times New Roman", 12), bg="white")
        self.count_label.pack(anchor="w")

        if self.role == "admin":
            self.bind_all_children(self, "<Button-1>", self.open_edit_window)

    def bind_all_children(self, widget, sequence, func):
        """Привязывает событие ко всем потомкам виджета"""
        widget.bind(sequence, func)
        for child in widget.winfo_children():
            self.bind_all_children(child, sequence, func)

    def open_edit_window(self, event=None):
        EditOrderWindow(self)

class ProductsWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.app = root
        self.products = []
        self.filtered_products = []

        topbar = tk.Frame(self, bg="#e6e6e6")
        topbar.pack(fill="x")

        tk.Label(topbar, text=("Гость" if self.app.current_role is None else self.app.current_role.capitalize()), font=("Times New Roman", 22, "bold"), bg="#e6e6e6").pack(side="left", padx=20, pady=10)

        tk.Button(topbar, text="Товары", command=self.app.open_products_window).pack(side="left", padx=5)
        tk.Button(topbar, text="Выйти", bg="#ff6666", fg="white", font=("Times New Roman", 14, "bold"), command=self.logout).pack(side="right", padx=20, pady=10)

        if self.app.current_role in ('admin', 'manager'):
            control_frame = tk.Frame(self, bg="#f0f0f0")
            control_frame.pack(fill="x", pady=5)

            tk.Label(control_frame, text="Поиск:").pack(side="left", padx=5)
            self.search_var = tk.StringVar()
            self.search_var.trace_add("write", lambda *args: self.apply_filters())
            tk.Entry(control_frame, textvariable=self.search_var).pack(side="left", padx=5)

            tk.Label(control_frame, text="Фильтр по поставщику:").pack(side="left", padx=5)
            self.provider_var = tk.StringVar()
            self.provider_var.trace_add("write", lambda *args: self.apply_filters())
            self.provider_menu = ttk.Combobox(control_frame, textvariable=self.provider_var, state="readonly")
            self.provider_menu.pack(side="left", padx=5)

            tk.Label(control_frame, text="Сортировка по количеству:").pack(side="left", padx=5)
            self.sort_var = tk.StringVar()
            self.sort_var.trace_add("write", lambda *args: self.apply_filters())
            self.sort_menu = ttk.Combobox(control_frame, textvariable=self.sort_var, state="readonly", values=["По возрастанию", "По убыванию"])
            self.sort_menu.pack(side="left", padx=5)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#f5f5f5")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.items_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas.create_window((0, 0), window=self.items_frame, anchor="nw")

        self.items_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for i in range(1, 21):
            card = ProductCard(self.items_frame, i, self.app.current_role)
            self.products.append(card)

        if self.app.current_role in ('admin', 'manager'):
            providers = [p.provider_text for p in self.products]
            self.provider_menu['values'] = ["Все поставщики"] + sorted(list(set(providers)))
            self.provider_var.set("Все поставщики")

        self.apply_filters()

    def apply_filters(self):
        if self.app.current_role not in ('admin', 'manager'):
            for p in self.products:
                p.pack(padx=100, pady=10, fill="x", anchor="center")
            return

        search_text = self.search_var.get().lower()
        provider_filter = self.provider_var.get()
        sort_order = self.sort_var.get()

        for p in self.products:
            p.pack_forget()

        self.filtered_products = []
        for p in self.products:
            matches_search = search_text in p.name_text.lower() or search_text in p.desc_text.lower() or search_text in p.vendor_text.lower() or search_text in p.provider_text.lower()
            matches_provider = provider_filter == "Все поставщики" or p.provider_text == provider_filter
            if matches_search and matches_provider:
                self.filtered_products.append(p)

        if sort_order == "По возрастанию":
            self.filtered_products.sort(key=lambda x: x.count_value)
        elif sort_order == "По убыванию":
            self.filtered_products.sort(key=lambda x: x.count_value, reverse=True)

        for p in self.filtered_products:
            p.pack(padx=100, pady=10, fill="x", anchor="center")

    def logout(self):
        self.app.current_role = None
        self.app.open_login_window()

class LoginWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        tk.Label(self, text="Вход", font=("Times New Roman", 22, "bold")).pack(pady=20)

        tk.Label(self, text="Логин:").pack()
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        tk.Label(self, text="Пароль:").pack()
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack()

        tk.Button(self, text="Войти", command=self.login).pack(pady=5)
        tk.Button(self, text="Войти как гость", command=self.login_as_guest).pack(pady=10)

    def login(self):
        data = (self.login_entry.get(), self.pass_entry.get())
        if data in db_users:
            self.master.current_role = db_users[data]
            self.master.open_products_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def login_as_guest(self):
        self.master.current_role = None
        self.master.open_products_window()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Товары и заказы")
        self.geometry("1000x700")
        self.current_role = None
        self.open_login_window()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def open_login_window(self):
        self.clear()
        LoginWindow(self).pack(fill="both", expand=True)

    def open_products_window(self):
        self.clear()
        ProductsWindow(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
