import tkinter as tk
from pages.register_pages import RegistrationWindow
from pages.main_page import MainPage

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("600x400")

        # Avvia direttamente la finestra principale
        self.show_main_page()

    def show_main_page(self):
        """Mostra la pagina principale."""
        self.main_page = MainPage(self.master, self.on_registration_success)

    def on_registration_success(self, name, surname, email):
        """Callback chiamato al termine della registrazione con successo."""
        self.main_page.update_user_info(name, surname, email)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = App(root)  # Inizializza l'app
        root.mainloop()  # Avvia il loop principale
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"Unknown error: {e}")
        exit()
