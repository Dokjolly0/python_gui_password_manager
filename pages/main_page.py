import tkinter as tk
from pages.login_page import LoginWindow
from pages.register_pages import RegistrationWindow
from pages.password_manager_page import PasswordManagerPage

class MainPage:
    def __init__(self, main_page, user_info):
        self.main_page = main_page
        self.user_info = user_info
        self.initialize_ui()

    def initialize_ui(self):
        """Inizializza la UI della pagina principale."""
        title_label = tk.Label(self.main_page, text="Benvenuto nel Password Manager", font=("Arial", 16))
        title_label.pack(pady=10)
        # Bottone registrazione
        button_register = tk.Button(self.main_page, text="Registrati", command=self.open_registration)
        button_register.pack(pady=20)
        # Bottone login
        button_login = tk.Button(self.main_page, text="Accedi", command=self.open_login)
        button_login.pack(pady=20)

    def open_registration(self):
        """Mostra la finestra di registrazione."""
        self.registration_window = RegistrationWindow(self.main_page, self.on_registration_success)
    
    def open_login(self):
        """Mostra la finestra di login."""
        self.login_window = LoginWindow(self.main_page, self.on_login_success)

    def on_registration_success(self, name, surname, email):
        """Callback chiamato al termine della registrazione con successo."""
        self.user_info = (name, surname, email)  # Aggiorna le informazioni dell'utente
        #print(f"Registrazione completata per: {name} {surname} ({email})")
        self.registration_window.registration_window.destroy()

    def on_login_success(self, email):
        """Callback chiamato al termine del login con successo."""
        print(f"User {email} has logged in successfully.")
        # Chiudi la finestra di login
        self.login_window.login_window.destroy()
        # Rimuovi tutti i widget dalla pagina principale
        for widget in self.main_page.winfo_children():
            widget.destroy()
        # Inizializza PasswordManagerPage come nuova interfaccia della finestra principale
        self.password_manager_page = PasswordManagerPage(self.main_page)
        
