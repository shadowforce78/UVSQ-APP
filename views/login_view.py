import ttkbootstrap as ttk
from tkinter import messagebox
from ..services.api_service import login
from .menu_view import show_menu

def create_login_view(window, classe, start, end):
    login_frame = ttk.Frame(window)
    login_frame.grid(row=0, column=0)

    student_number_label = ttk.Label(login_frame, text="Numéro étudiant")
    student_number_label.grid(row=0, pady=5)
    student_number_entry = ttk.Entry(login_frame)
    student_number_entry.grid(row=1, pady=5)

    password_label = ttk.Label(login_frame, text="Mot de passe")
    password_label.grid(row=2, pady=5)
    password_entry = ttk.Entry(login_frame, show="*")
    password_entry.grid(row=3, pady=5)

    def check_login():
        data = login(student_number_entry.get(), password_entry.get())
        if "detail" not in data:
            show_menu(window, classe, start, end)
        else:
            messagebox.showerror("Erreur", "Identifiants invalides !")

    login_button = ttk.Button(
        login_frame,
        text="Se connecter",
        command=check_login
    )
    login_button.grid(row=4, pady=20)