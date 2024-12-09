import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import requests

API = "http://localhost:8000"
EDTEndpoint = "/uvsq/edt/{classe}+{start}+{end}"

classe = 'INF1-B'
start = '2024-12-09'
end = '2024-12-13'

def get_edt(classe, start, end):
    response = requests.get(
        API + EDTEndpoint.format(classe=classe, start=start, end=end)
    )
    data = response.json()
    show_schedule(data)


def show_menu(classe, start, end):
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
        command=lambda: get_edt(classe, start, end)
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
        return None

def generate_time_slots():
    """Génère les créneaux horaires de 15 minutes"""
    slots = []
    for hour in range(8, 19):  # De 8h à 18h
        for minute in [0, 15, 30, 45]:
            slots.append(f"{hour:02d}:{minute:02d}")
    return slots

def show_time_label(time_str):
    """Détermine si l'heure doit être affichée dans la colonne"""
    return time_str.endswith(":00")

def get_nearest_time_slot(time_str):
    """Trouve le créneau de 15 minutes le plus proche"""
    hour, minute = map(int, time_str.split(":"))
    # Arrondir aux 15 minutes les plus proches
    minute = round(minute / 15) * 15
    if minute == 60:
        hour += 1
        minute = 0
    return f"{hour:02d}:{minute:02d}"

def get_day_position(date_str):
    """Détermine la position du jour dans la semaine (0=Lundi, 4=Vendredi)"""
    try:
        day = int(date_str.strip().split()[0].split('/')[0])
        start_day = int(start.split('-')[2])  # Récupère le jour du début de semaine
        return day - start_day
    except:
        return None

def show_schedule(data):
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    # Destroy the menu frame
    for widget in window.winfo_children():
        widget.destroy()

    # Configure window grid
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create main frame for schedule
    schedule_frame = ttk.Frame(window)
    schedule_frame.grid(sticky="nsew", padx=10, pady=10)

    # Define schedule structure first
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    hours = generate_time_slots()  # Déplacé ici avant son utilisation

    # Calculate cell dimensions based on screen size
    cell_width = (screen_width - 100) // 6  # 5 days + 1 time column
    cell_height = (screen_height - 150) // (len(hours) + 1)  # +1 pour l'en-tête

    # Style for headers with smaller font for time slots
    header_style = {"font": ("Helvetica", 9, "bold"), "padding": 5}

    # Create time column - Modifié pour n'afficher que les heures complètes
    for i, hour in enumerate(hours):
        if show_time_label(hour):
            ttk.Label(schedule_frame, text=hour, **header_style).grid(
                row=i + 2, column=0, padx=2, pady=2, sticky="e"
            )
        else:
            ttk.Label(schedule_frame, text="", **header_style).grid(
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
                height=cell_height,
                width=cell_width
            )
            cell_frame.grid(
                row=row + 2,
                column=col + 1,
                padx=1,
                pady=1,
                sticky="nsew"
            )
            cell_frame.grid_propagate(False)
            
    # Configure grid avec les nouvelles dimensions
    for row in range(len(hours)):
        schedule_frame.grid_rowconfigure(row + 2, weight=1, minsize=cell_height)
    for col in range(len(days)):
        schedule_frame.grid_columnconfigure(col + 1, weight=1, minsize=cell_width)

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
            start_time = get_nearest_time_slot(start_raw)
            end_time = get_nearest_time_slot(end_raw)
            day_num = get_day_from_date(date_debut)

            if not day_num:
                continue

            # Nouvelle façon de déterminer le jour
            day_position = get_day_position(date_debut)
            if day_position is None or day_position < 0 or day_position >= 5:
                continue
                
            col = day_position + 1  # +1 car la première colonne est pour les heures

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

            # Créer le frame d'événement
            event_frame = ttk.Frame(
                schedule_frame,
                style=f"{colors[hash(elements.get('Matière', '')) % len(colors)]}.TFrame",
                height=cell_height * row_span,
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
                    font=("Helvetica", 8, "bold"),
                    wraplength=140
                ).pack(fill="x", padx=2, pady=1)

                ttk.Label(
                    event_frame,
                    text=f"⏰ {start_time} - {end_time}",
                    font=("Helvetica", 7),
                ).pack(anchor="w")

                if "Salle" in elements and elements["Salle"]:
                    ttk.Label(
                        event_frame,
                        text=f"🏢 {elements['Salle']}",
                        font=("Helvetica", 7),
                    ).pack(anchor="w")

                if "Personnel" in elements and elements["Personnel"]:
                    ttk.Label(
                        event_frame,
                        text=f"👤 {elements['Personnel']}",
                        font=("Helvetica", 7),
                        wraplength=140,
                    ).pack(anchor="w")

        except Exception as e:
            continue  # Ignorer silencieusement les erreurs

    # Configure scroll region
    schedule_frame.update_idletasks()


window = ttk.Window(themename="superhero")
window.title("UVSQ - Application")
window.state('zoomed')  # Démarre en plein écran

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

# Au lieu d'appeler directement show_menu, on crée une fonction lambda
login_button = ttk.Button(
    login_frame, 
    text="Se connecter", 
    command=lambda: show_menu(classe, start, end)
)
login_button.grid(row=4, pady=20)

window.mainloop()
