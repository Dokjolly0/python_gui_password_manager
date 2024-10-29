import tkinter as tk
from utils.database_utils import DBConfig, DatabaseUtils
from utils.cript_utils import cript_utils

class LoginWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.login_window = tk.Toplevel(master)
        self.login_window.title("Accesso")
        self.login_window.geometry("400x300")

        label_login = tk.Label(self.login_window, text="Schermata di Accesso", font=("Arial", 16))
        label_login.pack(pady=10)

        # Email Field
        label_email = tk.Label(self.login_window, text="Email:")
        label_email.pack(pady=5)
        self.input_email = tk.Entry(self.login_window, width=40)
        self.input_email.pack(pady=5)

        # Password Field
        label_password = tk.Label(self.login_window, text="Password:")
        label_password.pack(pady=5)
        self.input_password = tk.Entry(self.login_window, show="*", width=40)
        self.input_password.pack(pady=5)

        # Login Button
        button_login = tk.Button(self.login_window, text="Accedi", command=self.login)
        button_login.pack(pady=20)

        # Result Label
        self.label_result = tk.Label(self.login_window, text="")
        self.label_result.pack()

    def login(self):
        """Gestisce la logica di accesso."""
        email = f"{self.input_email.get()}".lower()
        password = self.input_password.get()

        # Controlla se i campi sono vuoti
        if not email or not password:
            self.label_result.config(text="Email e password devono essere riempiti.", fg="red")
            return

        # Controlla nel database se l'email esiste
        db_config = DBConfig(path=".", name="user.db")
        db_utils = DatabaseUtils(db_config)
        conn = db_utils.create_connection(db_config.path + "/" + db_config.name)

        cursor = db_utils.execute_query(conn, f"SELECT password FROM users WHERE username = '{email}'")
        
        if cursor is None:
            self.label_result.config(text="Credenziali errate.", fg="red")
            return
        
        # Verifica se la query ha restituito un risultato valido
        result = cursor.fetchone()
        if result is None:
            self.label_result.config(text="Credenziali errate.", fg="red")
            print(email)
            conn.close()
            return

        # Recupera la password hashed dal database
        hashed_password = result[0]

        # Verifica se la password inserita corrisponde a quella nel database
        if cript_utils.check_cript(password, hashed_password):
            self.label_result.config(text="Accesso effettuato con successo!", fg="green")
            self.on_login_success(email)  # Chiama il callback di successo
            self.login_window.destroy()  # Chiudi la finestra di login
        else:
            self.label_result.config(text="Password errata.", fg="red")

        conn.close()
