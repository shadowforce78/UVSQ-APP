import ttkbootstrap as ttk
from .schedule_view import show_schedule

def show_menu(window, classe, start, end):
    for widget in window.winfo_children():
        widget.destroy()

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    menu_frame = ttk.Frame(window)
    menu_frame.grid(row=0, column=0)

    schedule_button = ttk.Button(
        menu_frame, 
        text="Emploi du temps", 
        command=lambda: show_schedule(window, classe, start, end)
    )
    schedule_button.grid(row=0, pady=5)

    grades_button = ttk.Button(menu_frame, text="Bulletins")
    grades_button.grid(row=1, pady=5)

    absences_button = ttk.Button(menu_frame, text="Absences")
    absences_button.grid(row=2, pady=5)

    settings_button = ttk.Button(menu_frame, text="Paramètres")
    settings_button.grid(row=3, pady=5)