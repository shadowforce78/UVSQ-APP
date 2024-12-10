import ttkbootstrap as ttk
from datetime import datetime
from utils.date_utils import get_week_dates
from views.login_view import create_login_view

def main():
    window = ttk.Window(themename="superhero")
    window.title("UVSQ - Application")
    window.state("zoomed")

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    classe = "INF1"  # Simple default value
    start, end = get_week_dates(datetime.now())

    create_login_view(window, classe, start, end)
    window.mainloop()

if __name__ == "__main__":
    main()
