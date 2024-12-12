import ttkbootstrap as ttk
from tkinter import messagebox
from services.api_service import login, autocomplete, get_edt_data
from .view_controller import ViewController
from utils.constants import CLASSES_CHOICES

def check_login(window, id, password, classe, start, end):
    data = login(id, password)
    if "detail" not in data:
        ViewController.show_menu(window, classe, start, end)
    else:
        messagebox.showerror("Erreur", "Identifiants invalides!")

def create_login_view(window, default_classe, start, end):
    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")


    login_frame = ttk.Frame(window)
    login_frame.grid(row=0, column=0)

    id_label = ttk.Label(login_frame, text="Identifiant:")
    id_label.grid(row=0, column=0, pady=5)
    id_entry = ttk.Entry(login_frame)
    id_entry.grid(row=0, column=1, pady=5)

    password_label = ttk.Label(login_frame, text="Mot de passe:")
    password_label.grid(row=1, column=0, pady=5)
    password_entry = ttk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    classes = CLASSES_CHOICES

    class_label = ttk.Label(login_frame, text="Classe:")
    class_label.grid(row=2, column=0, pady=5)
    class_combobox = ttk.Combobox(login_frame, textvariable=default_classe, values=classes)
    class_combobox.grid(row=2, column=1, pady=5)

    login_button = ttk.Button(
        login_frame,
        text="Connexion",
        command=lambda: check_login(window, id_entry.get(), password_entry.get(), class_combobox.get(), start, end)
    )
    login_button.grid(row=3, column=0, columnspan=2, pady=10)