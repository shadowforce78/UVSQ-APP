import ttkbootstrap as ttk
from datetime import datetime, timedelta
from utils.date_utils import get_week_dates
from utils.constants import CLASSES_CHOICES
from services.api_service import get_edt_data
from .view_controller import ViewController

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
        return date_str.strip().split()[0].split("/")[0]
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

def get_day_position(date_str, start):
    """Détermine la position du jour dans la semaine (0=Lundi, 4=Vendredi)"""
    try:
        day = int(date_str.strip().split()[0].split("/")[0])
        start_day = int(start.split("-")[2])  # Récupère le jour du début de semaine
        return day - start_day
    except:
        return None

def format_week_display(start_date):
    """Formate l'affichage de la semaine"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=4)
    return f"Semaine du {start.strftime('%d/%m/%Y')} au {end.strftime('%d/%m/%Y')}"

def on_class_change(event, window, start, end):
    """Handle class selection change"""
    classe = event.widget.get()  
    data = get_edt_data(classe, start, end)
    show_schedule(window, data, classe, start, end)

def change_week(window, offset, classe, start, end):
    """Change la semaine affichée"""
    new_date = datetime.strptime(start, "%Y-%m-%d") + timedelta(weeks=offset)
    new_start, new_end = get_week_dates(new_date)
    data = get_edt_data(classe, new_start, new_end)
    show_schedule(window, data, classe, new_start, new_end)

def show_schedule(window, data, classe, start, end):
    """Schedule view implementation"""
    # Get screen dimensions and setup window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    # Clear window
    for widget in window.winfo_children():
        widget.destroy()

    # Configure window grid
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create main frame for schedule
    schedule_frame = ttk.Frame(window)
    schedule_frame.grid(sticky="nsew", padx=10, pady=10)

    # Create header frame for back button
    header_frame = ttk.Frame(schedule_frame)
    header_frame.grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))

    # Add back button
    back_button = ttk.Button(
        header_frame,
        text="← Retour au menu",
        command=lambda: ViewController.show_menu(window, classe, start, end),
        style="secondary.TButton",
    )
    back_button.pack(side="left")

    # Add class selector
    class_frame = ttk.Frame(header_frame)
    class_frame.pack(side="left", padx=20)

    class_label = ttk.Label(class_frame, text="Classe:")
    class_label.pack(side="left", padx=5)

    class_combo = ttk.Combobox(
        class_frame, values=CLASSES_CHOICES, state="readonly", width=15
    )
    class_combo.set(classe)
    class_combo.pack(side="left", padx=5)
    class_combo.bind("<<ComboboxSelected>>", 
                    lambda e: on_class_change(e, window, start, end))

    # Create navigation frame
    nav_frame = ttk.Frame(header_frame)
    nav_frame.pack(side="right", padx=20)

    # Add navigation buttons with updated start and end dates
    prev_week = ttk.Button(
        nav_frame,
        text="◀",
        command=lambda: change_week(window, -1, classe, start, end),
        style="secondary.TButton",
        width=3,
    )
    prev_week.pack(side="left", padx=5)

    # Week label with current start date
    week_label = ttk.Label(
        nav_frame,
        text=format_week_display(start),  # Utilise la variable globale start
        font=("Helvetica", 10),
    )
    week_label.pack(side="left", padx=10)

    next_week = ttk.Button(
        nav_frame,
        text="▶",
        command=lambda: change_week(window, 1, classe, start, end),
        style="secondary.TButton",
        width=3,
    )
    next_week.pack(side="left", padx=5)

    # Adjust row numbers for the rest of the grid (+1 for all row indices)
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
                row=i + 3, column=0, padx=2, pady=2, sticky="e"
            )
        else:
            ttk.Label(schedule_frame, text="", **header_style).grid(
                row=i + 3, column=0, padx=2, pady=2, sticky="e"
            )

    # Create day headers
    for i, day in enumerate(days):
        ttk.Label(schedule_frame, text=day, **header_style).grid(
            row=2, column=i + 1, padx=2, pady=2, sticky="nsew"
        )

    # Créer d'abord la grille vide
    for row in range(len(hours)):
        for col in range(len(days)):
            cell_frame = ttk.Frame(
                schedule_frame,
                style="secondary.TFrame",
                height=cell_height,
                width=cell_width,
            )
            cell_frame.grid(row=row + 3, column=col + 1, padx=1, pady=1, sticky="nsew")
            cell_frame.grid_propagate(False)

    # Configure grid avec les nouvelles dimensions
    for row in range(len(hours)):
        schedule_frame.grid_rowconfigure(row + 3, weight=1, minsize=cell_height)
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
            end_raw = (
                heure_fin.strip().split()[1] if " " in heure_fin else heure_fin.strip()
            )

            # Trouver les heures les plus proches dans la grille
            start_time = get_nearest_time_slot(start_raw)
            end_time = get_nearest_time_slot(end_raw)
            day_num = get_day_from_date(date_debut)

            if not day_num:
                continue

            # Nouvelle façon de déterminer le jour
            day_position = get_day_position(date_debut, start)
            if day_position is None or day_position < 0 or day_position >= 5:
                continue

            col = day_position + 1  # +1 car la première colonne est pour les heures

            # Trouver l'index de fin le plus proche
            end_hour = int(end_time.split(":")[0])
            closest_end = f"{end_hour:02d}:00"
            if closest_end not in hours:
                closest_end = f"{(end_hour-1):02d}:00"

            start_row = hours.index(start_time) + 3
            end_row = hours.index(closest_end) + 3
            row_span = end_row - start_row
            if row_span < 1:
                row_span = 1

            # Créer le frame d'événement
            event_frame = ttk.Frame(
                schedule_frame,
                style=f"{colors[hash(elements.get('Matière', '')) % len(colors)]}.TFrame",
                height=cell_height * row_span,
                padding=5,
            )
            event_frame.grid(
                row=start_row,
                column=col,
                rowspan=row_span,
                sticky="nsew",
                padx=1,
                pady=1,
            )
            event_frame.grid_propagate(False)  # Forcer les dimensions
            event_frame.lift()

            # Afficher les détails de l'événement
            matiere = elements.get("Matière", elements.get("Matières", ""))
            if matiere:
                # Label pour la matière
                ttk.Label(
                    event_frame,
                    text=matiere,
                    font=("Helvetica", 8, "bold"),
                    wraplength=140,
                ).pack(fill="x", padx=2, pady=1)

                # Frame horizontal pour les détails
                details_frame = ttk.Frame(event_frame)
                details_frame.pack(fill="x", padx=2)

                # Afficher l'heure, la salle et le personnel sur la même ligne
                ttk.Label(
                    details_frame,
                    text=f"⏰ {start_time}-{end_time}",
                    font=("Helvetica", 7),
                ).pack(side="left", padx=(0, 5))

                if "Salle" in elements and elements["Salle"]:
                    ttk.Label(
                        details_frame,
                        text=f"🏢 {elements['Salle']}",
                        font=("Helvetica", 7),
                    ).pack(side="left", padx=(0, 5))

                if "Personnel" in elements and elements["Personnel"]:
                    ttk.Label(
                        details_frame,
                        text=f"👤 {elements['Personnel']}",
                        font=("Helvetica", 7),
                        wraplength=140,
                    ).pack(side="left")

        except Exception as e:
            continue  # Ignorer silencieusement les erreurs

    # Configure scroll region
    schedule_frame.update_idletasks()