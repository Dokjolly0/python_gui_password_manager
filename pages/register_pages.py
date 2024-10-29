import tkinter as tk
import re  # Importing regex for email validation
from utils.database_utils import DBConfig, DatabaseUtils
from utils.cript_utils import cript_utils

class RegistrationWindow:
    def __init__(self, master, on_success_callback):
        self.master = master
        self.on_success_callback = on_success_callback
        self.registration_window = tk.Toplevel(master)  # Create a new top-level window
        self.registration_window.title("Password Manager - Registrazione")
        self.registration_window.geometry("350x400")
        self.center_window()

        # Create a label for the title
        title_label = tk.Label(self.registration_window, text="Schermata di Registrazione", font=("Arial", 16))
        title_label.pack(pady=10)

        # Name Field
        label_name = tk.Label(self.registration_window, text="Nome:", anchor="w")
        label_name.pack(fill="x", padx=10)
        self.input_name = tk.Entry(self.registration_window)
        self.input_name.pack(fill="x", padx=10)

        # Surname Field
        label_surname = tk.Label(self.registration_window, text="Cognome:", anchor="w")
        label_surname.pack(fill="x", padx=10)
        self.input_surname = tk.Entry(self.registration_window)
        self.input_surname.pack(fill="x", padx=10)

        # Email Field
        label_email = tk.Label(self.registration_window, text="Email:", anchor="w")
        label_email.pack(fill="x", padx=10)
        self.input_email = tk.Entry(self.registration_window)
        self.input_email.pack(fill="x", padx=10)

        # Password Field
        label_password = tk.Label(self.registration_window, text="Password:", anchor="w")
        label_password.pack(fill="x", padx=10)
        self.input_password = tk.Entry(self.registration_window, show="*")
        self.input_password.pack(fill="x", padx=10)

        # Confirm Password Field
        label_check_password = tk.Label(self.registration_window, text="Conferma Password:", anchor="w")
        label_check_password.pack(fill="x", padx=10)
        self.input_check_password = tk.Entry(self.registration_window, show="*")
        self.input_check_password.pack(fill="x", padx=10)

        # Registration Button
        button_registra = tk.Button(self.registration_window, text="Registra", command=self.registra)
        button_registra.pack(pady=20)

        # Result Label
        self.label_result = tk.Label(self.registration_window, text="")
        self.label_result.pack()

    def center_window(self):
        """Center the window on the screen."""
        self.registration_window.update_idletasks()  # Update "requested size" from geometry manager
        width = self.registration_window.winfo_width()
        height = self.registration_window.winfo_height()
        x = (self.master.winfo_width() // 2) - (width // 2) + self.master.winfo_x()
        y = (self.master.winfo_height() // 2) - (height // 2) + self.master.winfo_y()
        self.registration_window.geometry(f"{width}x{height}+{x}+{y}")

    def is_valid_email(self, email):
        """Check if the provided email is valid."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def is_strong_password(self, password):
        """Check if the password is strong."""
        return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password)

    def registra(self):
        """Handles the registration logic."""
        name = self.input_name.get()
        surname = self.input_surname.get()
        email = self.input_email.get()
        password = self.input_password.get()
        check_password = self.input_check_password.get()

        # Check for empty fields
        if not all([name, surname, email, password, check_password]):
            self.label_result.config(text="Tutti i campi devono essere riempiti.", fg="red")
            return

        # Validate email
        if not self.is_valid_email(email):
            self.label_result.config(text="Email non valida.", fg="red")
            return

        # Check password strength
        if not self.is_strong_password(password):
            self.label_result.config(text="La password deve contenere almeno 8 caratteri, un numero e una lettera maiuscola.", fg="red")
            return

        # Check password match
        if password != check_password:
            self.label_result.config(text="Le password non corrispondono.", fg="red")
            return
        
        db_config = DBConfig(path=".", name="user.db")
        db_utils = DatabaseUtils(db_config)
        db_file = db_utils.create_database()
        conn = db_utils.create_connection(db_file)

        # Crea la tabella se non esiste già
        db_utils.execute_query(conn, """CREATE TABLE IF NOT EXISTS users (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            surname TEXT NOT NULL,
                                            username TEXT NOT NULL,
                                            password TEXT NOT NULL
                                    );""")

        # Verifica se l'email (username) esiste già nel database
        cursor = db_utils.execute_query(conn, "SELECT COUNT(*) FROM users WHERE username = ?", (email,))
        if cursor is None:
            self.label_result.config(text="Errore nell'esecuzione della query.", fg="red")
            return
        else: 
            print(cursor)

        email_exists = cursor.fetchone()[0] > 0  # Ottieni il conteggio delle righe

        if email_exists:
            self.label_result.config(text="L'email è già registrata.", fg="red")
            return

        # Se l'email non esiste, procedi all'inserimento
        hash_password = cript_utils.cript(password)  # Usa `password` qui
        db_utils.execute_query(conn, "INSERT INTO users(name, surname, username, password) VALUES(?, ?, ?, ?)", 
                               (name, surname, email.lower(), hash_password))

        self.label_result.config(text=f"Registrazione completata per {name} {surname}.", fg="green")
        
        # Chiamata al callback per notificare il successo della registrazione
        self.on_success_callback(name, surname, email.lower())
