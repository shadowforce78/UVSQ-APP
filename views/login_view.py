import ttkbootstrap as ttk
from tkinter import messagebox
from services.api_service import login, autocomplete, get_edt_data
from .view_controller import ViewController

def check_login(window, id, password, classe, start, end):
    data = login(id, password)
    if "detail" not in data:
        ViewController.show_menu(window, classe, start, end)
    else:
        messagebox.showerror("Erreur", "Identifiants invalides!")

def create_login_view(window, default_classe, start, end):
    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")

    # Create class selection frame
    class_frame = ttk.LabelFrame(frame, text="Sélection de classe")
    class_frame.pack(pady=20, padx=20, fill="x")

    class_var = ttk.StringVar()
    class_combobox = ttk.Combobox(class_frame, textvariable=class_var)
    class_combobox.pack(pady=10, padx=10, fill="x")

    def on_type(event):
        if len(class_combobox.get()) >= 2:
            results = autocomplete(class_combobox.get())
            class_combobox['values'] = [item['text'] for item in results.get('results', [])]

    class_combobox.bind('<KeyRelease>', on_type)
    class_var.set(default_classe)

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

    login_button = ttk.Button(
        login_frame,
        text="Connexion",
        command=lambda: check_login(window, id_entry.get(), password_entry.get(), class_var.get(), start, end)
    )
    login_button.grid(row=2, column=0, columnspan=2, pady=10)