import ttkbootstrap as ttk
from .view_controller import ViewController

def create_menu_view(window, classe, start, end):
    # Clear window
    for widget in window.winfo_children():
        widget.destroy()

    # Create menu frame
    menu_frame = ttk.Frame(window)
    menu_frame.grid(row=0, column=0)

    # Menu buttons
    schedule_button = ttk.Button(
        menu_frame, 
        text="Emploi du temps", 
        command=lambda: ViewController.show_schedule(window, classe, start, end)
    )
    schedule_button.grid(row=0, pady=5)

    grades_button = ttk.Button(menu_frame, text="Bulletins")
    grades_button.grid(row=1, pady=5)

    absences_button = ttk.Button(menu_frame, text="Absences")
    absences_button.grid(row=2, pady=5)

    settings_button = ttk.Button(menu_frame, text="Paramètres")
    settings_button.grid(row=3, pady=5)