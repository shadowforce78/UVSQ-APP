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


def normalize_time(time_str):
    """Convertit n'importe quel format d'heure en format HH:00"""
    # Gestion des formats spéciaux comme "08:45" ou "11:15"
    hour = int(time_str.split(":")[0])
    return f"{hour:02d}:00"

def format_time(time_str):
    """Convertit le format '12/12/2024 13:00' en '13:00'"""
    return normalize_time(time_str.strip().split()[1])

def get_day_from_date(date_str):
    """Extrait le jour du mois d'une date '12/12/2024 13:00'"""
    try:
        return date_str.strip().split()[0].split('/')[0]
    except:
        print(f"Erreur lors du parsing de la date: {date_str}")
        return None

def get_nearest_hour(time_str):
    """Trouve l'heure la plus proche dans la grille"""
    hours = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", 
             "14:00", "15:00", "16:00", "17:00", "18:00"]
    
    try:
        hour, minute = map(int, time_str.split(":"))
        if minute >= 30:
            hour += 1
        target = f"{hour:02d}:00"
        
        if target in hours:
            return target
        elif hour < 8:
            return "08:00"
        elif hour > 18:
            return "18:00"
        else:
            # Trouver l'heure la plus proche
            for h in hours:
                if h > target:
                    return h
            return hours[-1]
    except:
        return "08:00"  # Valeur par défaut en cas d'erreur


def show_schedule(data):
    # Déboguer les données reçues
    print("Données reçues:", data)

    # Resize window for schedule view
    window.geometry("1200x800")

    # Destroy the menu frame
    for widget in window.winfo_children():
        widget.destroy()

    # Configure window grid
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create a canvas and a scrollbar
    canvas = ttk.Canvas(window)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Create main frame for schedule
    schedule_frame = ttk.Frame(scrollable_frame)
    schedule_frame.grid(sticky="nsew", padx=10, pady=10)

    # Add back button
    back_button = ttk.Button(schedule_frame, text="Retour", command=show_menu)
    back_button.grid(row=0, column=0, columnspan=6, pady=(0, 20), sticky="w")

    # Create a table-like structure for the schedule
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    hours = [
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
    ]

    # Style for headers
    header_style = {"font": ("Helvetica", 11, "bold"), "padding": 10}

    # Create time column
    for i, hour in enumerate(hours):
        ttk.Label(schedule_frame, text=hour, **header_style).grid(
            row=i + 2, column=0, padx=2, pady=2, sticky="e"
        )

    # Create day headers
    for i, day in enumerate(days):
        ttk.Label(schedule_frame, text=day, **header_style).grid(
            row=1, column=i + 1, padx=2, pady=2, sticky="nsew"
        )

    # Créer d'abord la grille vide
    for row in range(len(hours)):
        for col in range(len(days)):
            cell_frame = ttk.Frame(
                schedule_frame,
                style="secondary.TFrame",
                height=80,
                width=150
            )
            cell_frame.grid(
                row=row + 2,
                column=col + 1,
                padx=1,
                pady=1,
                sticky="nsew"
            )
            # Forcer les dimensions minimales
            cell_frame.grid_propagate(False)
            
    # Configure grid
    for row in range(len(hours)):
        schedule_frame.grid_rowconfigure(row + 2, weight=1, minsize=80)
    for col in range(len(days)):
        schedule_frame.grid_columnconfigure(col + 1, weight=1, minsize=150)

    # Populate events with raised priority
    colors = ["primary", "info", "success", "warning"]
    for event in data:
        try:
            elements = {elem["label"]: elem["content"] for elem in event["elements"]}
            heure = elements.get("Heure", "")
            
            if not heure or "-" not in heure:
                continue
                
            date_debut, heure_fin = heure.split("-")
            
            # Extraire uniquement l'heure de la date complète
            start_raw = date_debut.strip().split()[1]
            end_raw = heure_fin.strip().split()[1] if " " in heure_fin else heure_fin.strip()
            
            # Trouver les heures les plus proches dans la grille
            start_time = get_nearest_hour(start_raw)
            end_time = get_nearest_hour(end_raw)
            day_num = get_day_from_date(date_debut)

            print(f"Debug - Start: {start_time}, End: {end_time}, Day: {day_num}")

            if not day_num:
                continue

            # Convertir le jour en format attendu
            days_map = {
                "09": "Lundi",
                "10": "Mardi",
                "11": "Mercredi",
                "12": "Jeudi",
                "13": "Vendredi"
            }
            day = days_map.get(day_num)
            
            if not day or start_time not in hours:
                print(f"Jour non valide ou heure de début non trouvée: {day}, {start_time}")
                continue

            # Trouver l'index de fin le plus proche
            end_hour = int(end_time.split(":")[0])
            closest_end = f"{end_hour:02d}:00"
            if closest_end not in hours:
                closest_end = f"{(end_hour-1):02d}:00"

            start_row = hours.index(start_time) + 2
            end_row = hours.index(closest_end) + 2
            row_span = end_row - start_row
            if row_span < 1:
                row_span = 1
            col = days.index(day) + 1

            # Créer le frame d'événement
            event_frame = ttk.Frame(
                schedule_frame,
                style=f"{colors[hash(elements.get('Matière', '')) % len(colors)]}.TFrame",
                height=80 * row_span,  # Hauteur fixe basée sur row_span
                padding=5
            )
            event_frame.grid(
                row=start_row,
                column=col,
                rowspan=row_span,
                sticky="nsew",
                padx=1,
                pady=1
            )
            event_frame.grid_propagate(False)  # Forcer les dimensions
            event_frame.lift()

            # Afficher les détails de l'événement
            matiere = elements.get('Matière', elements.get('Matières', ''))
            if matiere:
                ttk.Label(
                    event_frame,
                    text=matiere,
                    font=("Helvetica", 10, "bold"),
                    wraplength=140
                ).pack(fill="x", padx=2, pady=1)

                ttk.Label(
                    event_frame,
                    text=f"⏰ {start_time} - {end_time}",
                    font=("Helvetica", 9),
                ).pack(anchor="w")

                if "Salle" in elements and elements["Salle"]:
                    ttk.Label(
                        event_frame,
                        text=f"🏢 {elements['Salle']}",
                        font=("Helvetica", 9),
                    ).pack(anchor="w")

                if "Personnel" in elements and elements["Personnel"]:
                    ttk.Label(
                        event_frame,
                        text=f"👤 {elements['Personnel']}",
                        font=("Helvetica", 9),
                        wraplength=140,
                    ).pack(anchor="w")

        except Exception as e:
            print(f"Erreur détaillée: {str(e)}")
            print(f"Événement problématique: {elements if 'elements' in locals() else 'N/A'}")

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
