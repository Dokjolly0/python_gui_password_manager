import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import PIL for image handling
from utils.database_utils import DBConfig, DatabaseUtils
from utils.cript_utils import cript_utils

class LoginWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.login_window = tk.Toplevel(master)
        self.login_window.title("Accesso")
        self.login_window.geometry("400x300")
        self.login_window.configure(bg="#f0f0f0")

        # Percorso cartella principale progetto (password manager)
        absolute_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(absolute_path)
        parent_directory = os.path.dirname(current_directory)

        # Header
        label_login = tk.Label(self.login_window, text="Schermata di Accesso", font=("Arial", 24, "bold"), bg="#f0f0f0")
        label_login.pack(pady=20)

        # Email Field
        label_email = tk.Label(self.login_window, text="Email:", bg="#f0f0f0")
        label_email.pack(pady=5)
        self.input_email = ttk.Entry(self.login_window, width=40)
        self.input_email.pack(pady=5)

        # Password Field
        label_password = tk.Label(self.login_window, text="Password:", bg="#f0f0f0")
        label_password.pack(pady=5)

        # Frame for password entry and eye icon
        password_frame = tk.Frame(self.login_window, bg="#f0f0f0")
        password_frame.pack(pady=5)

        self.input_password = ttk.Entry(password_frame, show="*", width=37)
        self.input_password.grid(row=0, column=0, padx=(0, 5))

        # Load eye icons
        self.eye_open_img = ImageTk.PhotoImage(Image.open(f"{parent_directory}/img/eye_visible.png").resize((20, 20)))
        self.eye_closed_img = ImageTk.PhotoImage(Image.open(f"{parent_directory}/img/eye_hidden.png").resize((20, 20)))

        # Toggle password visibility button
        self.toggle_password_button = tk.Button(password_frame, image=self.eye_closed_img, command=self.toggle_password_visibility, bg="#f0f0f0", borderwidth=0)
        self.toggle_password_button.grid(row=0, column=1)

        # Frame for buttons
        button_frame = tk.Frame(self.login_window, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Switch to registration button (now comes first)
        self.switch_to_registration_button = ttk.Button(button_frame, text="Registrati", command=self.open_registration_window, width=15)
        self.switch_to_registration_button.grid(row=0, column=0, padx=(0, 10))  # Add spacing to the right

        # Login Button (now comes second)
        button_login = ttk.Button(button_frame, text="Accedi", command=self.login, width=15)
        button_login.grid(row=0, column=1)

        # Result Label
        self.label_result = tk.Label(self.login_window, text="", bg="#f0f0f0", fg="red")
        self.label_result.pack(pady=10)

        # Bind enter key to login method
        self.login_window.bind('<Return>', lambda event: self.login())

    def toggle_password_visibility(self):
        """Toggle the visibility of the password."""
        if self.input_password.cget('show') == "":
            self.input_password.config(show="*")
            self.toggle_password_button.config(image=self.eye_closed_img)
        else:
            self.input_password.config(show="")
            self.toggle_password_button.config(image=self.eye_open_img)

    def login(self):
        """Handles the login logic."""
        email = f"{self.input_email.get()}".lower()
        password = self.input_password.get()

        # Check if fields are empty
        if not email or not password:
            self.label_result.config(text="Email e password devono essere riempiti.", fg="red")
            return

        # Check if email exists in the database
        db_config = DBConfig(path=".", name="user.db")
        db_utils = DatabaseUtils(db_config)
        conn = db_utils.create_connection(db_config.path + "/" + db_config.name)

        cursor = db_utils.execute_query(conn, f"SELECT password FROM users WHERE username = '{email}'")
        
        if cursor is None:
            self.label_result.config(text="Credenziali errate.", fg="red")
            conn.close()
            return
        
        # Verify if the query returned a valid result
        result = cursor.fetchone()
        if result is None:
            self.label_result.config(text="Credenziali errate.", fg="red")
            conn.close()
            return

        # Retrieve the hashed password from the database
        hashed_password = result[0]

        # Verify if the entered password matches the one in the database
        if cript_utils.check_cript(password, hashed_password):
            self.label_result.config(text="Accesso effettuato con successo!", fg="green")
            self.on_login_success(email)  # Call the success callback
            self.login_window.destroy()  # Close the login window
        else:
            self.label_result.config(text="Password errata.", fg="red")

        conn.close()

    def open_registration_window(self):
        from pages.register_page import RegistrationWindow
        """Open the registration window."""
        self.login_window.destroy()  # Close the login window
        RegistrationWindow(self.master, self.on_login_success)  # Open the registration window
