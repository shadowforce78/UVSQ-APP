import ttkbootstrap as ttk
import requests

API = "http://localhost:8000"
EDTEndpoint = "/uvsq/edt/{classe}+{start}+{end}"

def get_edt(classe, start, end):
    response = requests.get(API + EDTEndpoint.format(classe=classe, start=start, end=end))
    data = response.json()
    show_schedule(data)

def show_menu():
    # Destroy the login frame
    login_frame.destroy()

    # Create a new frame for the menu
    menu_frame = ttk.Frame(window)
    menu_frame.pack(pady=100)

    # Menu options
    schedule_button = ttk.Button(menu_frame, text="Emploi du temps", command=lambda: get_edt("inf1-b", "2024-12-09", "2024-12-09"))
    schedule_button.pack(pady=5)

    grades_button = ttk.Button(menu_frame, text="Bulletins")
    grades_button.pack(pady=5)

    absences_button = ttk.Button(menu_frame, text="Absences")
    absences_button.pack(pady=5)

    settings_button = ttk.Button(menu_frame, text="Paramètres")
    settings_button.pack(pady=5)

def show_schedule(data):
    # Destroy the menu frame
    for widget in window.winfo_children():
        widget.destroy()

    # Create main frame for schedule
    schedule_frame = ttk.Frame(window)
    schedule_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add back button
    back_button = ttk.Button(schedule_frame, text="Retour", command=show_menu)
    back_button.pack(pady=(0, 20))

    # Create scrollable frame for events
    canvas = ttk.Canvas(schedule_frame)
    scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # For each event in the schedule
    for event in data:
        # Create a frame for each event
        event_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        event_frame.pack(pady=5, padx=10, fill="x")

        # Get event details with default values for missing keys
        elements = {elem["label"]: elem["content"] for elem in event["elements"]}
        
        # Add event details with safe access
        ttk.Label(event_frame, text=elements.get("Heure", "Horaire non spécifié"), 
                 font=("Helvetica", 10, "bold")).pack(anchor="w", padx=5)
        ttk.Label(event_frame, text=elements.get("Matière", "Matière non spécifiée")).pack(anchor="w", padx=5)
        
        if "Personnel" in elements and elements["Personnel"]:
            ttk.Label(event_frame, text=f"Prof: {elements['Personnel']}").pack(anchor="w", padx=5)
        
        if "Salle" in elements and elements["Salle"]:
            ttk.Label(event_frame, text=f"Salle: {elements['Salle']}").pack(anchor="w", padx=5)
        
        group = elements.get("Groupe", "Groupe non spécifié")
        ttk.Label(event_frame, text=f"Groupe: {group}").pack(anchor="w", padx=5)
        
        event_type = elements.get("Catégorie d'événement", "Type non spécifié")
        if event_type:
            ttk.Label(event_frame, text=event_type).pack(anchor="w", padx=5)
        
        ttk.Separator(scrollable_frame).pack(fill="x", pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

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
