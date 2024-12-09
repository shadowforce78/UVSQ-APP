import ttkbootstrap as ttk
import requests

API = "http://localhost:8000"
EDTEndpoint = "/uvsq/edt/{classe}+{start}+{end}"


def get_edt(classe, start, end):
    response = requests.get(
        API + EDTEndpoint.format(classe=classe, start=start, end=end)
    )
    data = response.json()
    show_schedule(data)


def show_menu():
    # Destroy all widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Configure window grid
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create a new frame for the menu
    menu_frame = ttk.Frame(window)
    menu_frame.grid(row=0, column=0)

    # Menu options
    schedule_button = ttk.Button(
        menu_frame,
        text="Emploi du temps",
        command=lambda: get_edt("inf1-b", "2024-12-09", "2024-12-13"),
    )
    schedule_button.grid(row=0, pady=5)

    grades_button = ttk.Button(menu_frame, text="Bulletins")
    grades_button.grid(row=1, pady=5)

    absences_button = ttk.Button(menu_frame, text="Absences")
    absences_button.grid(row=2, pady=5)

    settings_button = ttk.Button(menu_frame, text="Paramètres")
    settings_button.grid(row=3, pady=5)


def show_schedule(data):
    # Resize window for schedule view
    window.geometry("1200x800")
    
    # Destroy the menu frame
    for widget in window.winfo_children():
        widget.destroy()

    # Configure window grid
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create main frame for schedule
    schedule_frame = ttk.Frame(window)
    schedule_frame.grid(sticky="nsew", padx=10, pady=10)

    # Add back button
    back_button = ttk.Button(schedule_frame, text="Retour", command=show_menu)
    back_button.grid(row=0, column=0, columnspan=6, pady=(0, 20), sticky="w")

    # Create a table-like structure for the schedule
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    hours = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", 
             "15:00", "16:00", "17:00", "18:00"]

    # Style for headers
    header_style = {"font": ("Helvetica", 11, "bold"), "padding": 10}
    
    # Create time column
    for i, hour in enumerate(hours):
        ttk.Label(schedule_frame, text=hour, **header_style).grid(
            row=i+2, column=0, padx=2, pady=2, sticky="e"
        )

    # Create day headers
    for i, day in enumerate(days):
        ttk.Label(schedule_frame, text=day, **header_style).grid(
            row=1, column=i+1, padx=2, pady=2, sticky="nsew"
        )

    # Create empty cells for the grid
    for row in range(len(hours)):
        for col in range(len(days)):
            frame = ttk.Frame(schedule_frame, style="secondary.TFrame")
            frame.grid(row=row+2, column=col+1, padx=1, pady=1, sticky="nsew")
            schedule_frame.grid_rowconfigure(row+2, weight=1, minsize=80)
            schedule_frame.grid_columnconfigure(col+1, weight=1, minsize=150)

    # Populate events
    colors = ["primary", "info", "success", "warning"]  # Different styles for events
    for event in data:
        elements = {elem["label"]: elem["content"] for elem in event["elements"]}
        day = elements.get("Jour", "Jour non spécifié")
        time_range = elements.get("Heure", "").split(" - ")
        
        if len(time_range) == 2 and day in days:
            start_time, end_time = time_range
            if start_time in hours:
                start_row = hours.index(start_time) + 2
                # Calculer le nombre de créneaux horaires
                end_row = start_row
                if end_time in hours:
                    end_row = hours.index(end_time) + 2
                row_span = end_row - start_row
                col = days.index(day) + 1
                
                # Créer le cadre de l'événement
                event_frame = ttk.Frame(
                    schedule_frame,
                    style=f"{colors[hash(elements.get('Matière', '')) % len(colors)]}.TFrame",
                    padding=5
                )
                event_frame.grid(
                    row=start_row, 
                    column=col, 
                    sticky="nsew", 
                    padx=1, 
                    pady=1,
                    rowspan=row_span
                )
                
                # Ajouter les détails de l'événement
                ttk.Label(
                    event_frame,
                    text=elements.get('Matière', ''),
                    font=("Helvetica", 10, "bold"),
                    wraplength=140
                ).pack(anchor="w")
                
                if time_range:
                    ttk.Label(
                        event_frame,
                        text=f"⏰ {' - '.join(time_range)}",
                        font=("Helvetica", 9)
                    ).pack(anchor="w")
                
                if "Salle" in elements and elements["Salle"]:
                    ttk.Label(
                        event_frame,
                        text=f"🏢 {elements['Salle']}",
                        font=("Helvetica", 9)
                    ).pack(anchor="w")
                
                if "Personnel" in elements and elements["Personnel"]:
                    ttk.Label(
                        event_frame,
                        text=f"👤 {elements['Personnel']}",
                        font=("Helvetica", 9),
                        wraplength=140
                    ).pack(anchor="w")

    # Configure scroll region
    schedule_frame.update_idletasks()


window = ttk.Window(themename="superhero")
window.title("UVSQ - Application")
window.geometry("400x600")

# Configure window grid
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Create a frame for the login form
login_frame = ttk.Frame(window)
login_frame.grid(row=0, column=0)

# Student number label and entry
student_number_label = ttk.Label(login_frame, text="Numéro étudiant")
student_number_label.grid(row=0, pady=5)
student_number_entry = ttk.Entry(login_frame)
student_number_entry.grid(row=1, pady=5)

# Password label and entry
password_label = ttk.Label(login_frame, text="Mot de passe")
password_label.grid(row=2, pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=3, pady=5)

# Login button
login_button = ttk.Button(login_frame, text="Se connecter", command=show_menu)
login_button.grid(row=4, pady=20)

window.mainloop()
