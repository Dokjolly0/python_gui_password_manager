import os
import tkinter as tk
from tkinter import ttk
from pages.login_page import LoginWindow
from pages.register_page import RegistrationWindow
from pages.password_manager_page import PasswordManagerPage
from utils.database_utils import DatabaseUtils, DBConfig  # Make sure to import your DatabaseUtils

user_info = None

class MainPage:
    def __init__(self, main_page, user_info):
        self.main_page = main_page
        self.user_info = user_info

        # Initialize Database Utils
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'user.db')  
        db_config = DBConfig(path=os.path.dirname(db_path), name=os.path.basename(db_path))
        self.db_utils = DatabaseUtils(db_config)

        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the UI for the main page."""
        self.main_page.configure(bg="#f0f0f0")
        title_label = tk.Label(self.main_page, text="Benvenuto nel Password Manager", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)

        # Create a frame for buttons
        button_frame = ttk.Frame(self.main_page)
        button_frame.pack(pady=20)

        # Registration button
        button_register = ttk.Button(button_frame, text="Registrati", command=self.open_registration, width=15)
        button_register.grid(row=0, column=0, padx=10, pady=10)

        # Login button
        button_login = ttk.Button(button_frame, text="Accedi", command=self.open_login, width=15)
        button_login.grid(row=0, column=1, padx=10, pady=10)

        # Add some visual separation
        separator = ttk.Separator(self.main_page, orient='horizontal')
        separator.pack(fill='x', pady=20)

        # Footer label
        footer_label = tk.Label(self.main_page, text="Gestisci le tue password in modo sicuro!", font=("Arial", 10), bg="#f0f0f0")
        footer_label.pack(pady=10)

    def open_registration(self):
        """Show the registration window."""
        self.registration_window = RegistrationWindow(self.main_page, self.on_registration_success)

    def open_login(self):
        """Show the login window."""
        self.login_window = LoginWindow(self.main_page, self.on_login_success)

    def on_registration_success(self, name, surname, email):
        """Callback chiamato al successo della registrazione."""
        self.user_info = (name, surname, email)
        print(f"user_info assegnato: {self.user_info}, Type: {type(self.user_info)}")
        self.registration_window.registration_window.destroy()

    def get_user_info(self, email):
        """Recupera le informazioni dell'utente dal database."""
        conn = self.db_utils.get_database()
        cursor = self.db_utils.execute_query(conn, "SELECT name, surname, username FROM users WHERE username = ?", (email,))
        
        if cursor:
            return cursor.fetchone()  # This should return (first_name, last_name, email)
        print("Torna none")
        return None

    def on_login_success(self, email):
        """Callback chiamato al successo del login."""
        print(f"User {email} has logged in successfully.")
        self.login_window.login_window.destroy()

        # Recupera informazioni dell'utente
        self.user_info = self.get_user_info(email)

        # Controllo user_info prima di passarlo
        print(f"user_info prima della PasswordManagerPage: {self.user_info}, Type: {type(self.user_info)}")

        # Clear the main page
        for widget in self.main_page.winfo_children():
            widget.destroy()

        # Inizializza PasswordManagerPage come nuova interfaccia per la finestra principale
        self.password_manager_page = PasswordManagerPage(self.main_page, self.user_info)
