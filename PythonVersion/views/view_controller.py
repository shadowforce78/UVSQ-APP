
from services.api_service import get_edt_data

class ViewController:
    @staticmethod
    def show_menu(window, classe, start, end):
        # Import here to avoid circular imports
        from .menu_view import create_menu_view
        create_menu_view(window, classe, start, end)
    
    @staticmethod
    def show_schedule(window, classe, start, end):
        from .schedule_view import show_schedule
        data = get_edt_data(classe, start, end)
        show_schedule(window, data, classe, start, end)