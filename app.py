import ttkbootstrap as ttk
import requests


def show_menu():
    # Destroy the login frame
    login_frame.destroy()

    # Create a new frame for the menu
    menu_frame = ttk.Frame(window)
    menu_frame.pack(pady=100)

    # Menu options
    schedule_button = ttk.Button(menu_frame, text="Emploi du temps")
    schedule_button.pack(pady=5)

    grades_button = ttk.Button(menu_frame, text="Bulletins")
    grades_button.pack(pady=5)

    absences_button = ttk.Button(menu_frame, text="Absences")
    absences_button.pack(pady=5)

    settings_button = ttk.Button(menu_frame, text="Paramètres")
    settings_button.pack(pady=5)


window = ttk.Window(themename="superhero")
window.title("UVSQ - Application")
window.geometry("600x800")

# Create a frame for the login form
login_frame = ttk.Frame(window)
login_frame.pack(pady=100)

# Student number label and entry
student_number_label = ttk.Label(login_frame, text="Numéro étudiant")
student_number_label.pack(pady=5)
student_number_entry = ttk.Entry(login_frame)
student_number_entry.pack(pady=5)

# Password label and entry
password_label = ttk.Label(login_frame, text="Mot de passe")
password_label.pack(pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack(pady=5)

# Login button
login_button = ttk.Button(login_frame, text="Se connecter", command=show_menu)
login_button.pack(pady=20)

window.mainloop()
