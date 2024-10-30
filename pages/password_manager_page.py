import os
import tkinter as tk
from tkinter import messagebox
from utils.database_utils import DatabaseUtils, DBConfig  # Ensure the correct module path

class PasswordManagerPage:
    def __init__(self, master, user_info):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("600x400")
        self.user_info = user_info

        # Build the absolute path for the database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'user.db')  
        self.db_config = DBConfig(path=os.path.dirname(db_path), name=os.path.basename(db_path))
        self.db_utils = DatabaseUtils(self.db_config)

        # Create the table if it doesn't exist
        self.create_table()

        # Clear any previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # UI Configuration for Password Manager Page
        title_label = tk.Label(self.master, text="Gestore delle Password", font=("Arial", 16))
        title_label.pack(pady=10)

        # Add Password Button
        add_password_btn = tk.Button(self.master, text="Aggiungi Nuova Password", command=self.add_password)
        add_password_btn.pack(pady=10)

        # Frame for storing passwords
        self.password_frame = tk.Frame(self.master)
        self.password_frame.pack(pady=10, fill="both", expand=True)

        # Displaying passwords
        self.display_passwords()
        
    def create_table(self):
        """Create passwords table if it doesn't exist."""
        try:
            conn = self.db_utils.get_database()
            self.db_utils.execute_query(conn, '''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            ''')
            self.db_utils.close_connection(conn)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error creating table: {e}")

    def display_passwords(self):
        """Load and display passwords from the database."""
        for widget in self.password_frame.winfo_children():
            widget.destroy()

        if self.user_info is None:
            print("Error: User info is None. Cannot display passwords.")
            return  # Exit the method if user_info is None

        # Connect to the database and retrieve passwords
        conn = self.db_utils.get_database()
        try:
            cursor = self.db_utils.execute_query(conn, "SELECT site, username, password FROM passwords WHERE user_id = ?", (self.user_info[0],))
            passwords = cursor.fetchall() if cursor else []

            # Display headers
            headers = ["Sito", "Nome Utente", "Password", "Azioni"]
            for col, text in enumerate(headers):
                tk.Label(self.password_frame, text=text, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=5, pady=5)

            # Display password entries
            for idx, entry in enumerate(passwords):
                site, username, password = entry
                tk.Label(self.password_frame, text=site).grid(row=idx+1, column=0, padx=5, pady=5)
                tk.Label(self.password_frame, text=username).grid(row=idx+1, column=1, padx=5, pady=5)
                tk.Label(self.password_frame, text="******").grid(row=idx+1, column=2, padx=5, pady=5)

                # Edit and Delete buttons
                edit_btn = tk.Button(self.password_frame, text="Modifica", command=lambda s=site, u=username, p=password: self.edit_password(s, u, p))
                edit_btn.grid(row=idx+1, column=3, padx=5, pady=5)

                delete_btn = tk.Button(self.password_frame, text="Elimina", command=lambda s=site: self.delete_password(s))
                delete_btn.grid(row=idx+1, column=4, padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error retrieving passwords: {e}")
        finally:
            self.db_utils.close_connection(conn)

    def add_password(self):
        """Popup for adding a new password."""
        self.password_popup("Aggiungi Password")

    def edit_password(self, site, username, password):
        """Popup for modifying an existing password."""
        self.password_popup("Modifica Password", {"site": site, "username": username, "password": password})

    def password_popup(self, title, entry=None):
        """Set up the popup window for adding/modifying passwords."""
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x200")
        
        tk.Label(popup, text="Sito:").pack(pady=5)
        site_entry = tk.Entry(popup)
        site_entry.pack(pady=5)
        site_entry.insert(0, entry["site"] if entry else "")
        
        tk.Label(popup, text="Nome Utente:").pack(pady=5)
        user_entry = tk.Entry(popup)
        user_entry.pack(pady=5)
        user_entry.insert(0, entry["username"] if entry else "")
        
        tk.Label(popup, text="Password:").pack(pady=5)
        pass_entry = tk.Entry(popup, show="*")
        pass_entry.pack(pady=5)
        pass_entry.insert(0, entry["password"] if entry else "")

        save_btn = tk.Button(popup, text="Salva", command=lambda: self.save_password(entry, site_entry.get(), user_entry.get(), pass_entry.get(), popup))
        save_btn.pack(pady=10)

    def save_password(self, entry, site, username, password, popup):
        """Save the password in the database."""
        conn = self.db_utils.get_database()
        try:
            if entry:
                # Modify an existing password
                query = "UPDATE passwords SET site = ?, username = ?, password = ? WHERE site = ? AND user_id = ?"
                params = (site, username, password, entry["site"], self.user_info[0])
            else:
                # Add a new password
                query = "INSERT INTO passwords (site, username, password, user_id) VALUES (?, ?, ?, ?)"
                params = (site, username, password, self.user_info[0])

            self.db_utils.execute_query(conn, query, params)
            self.display_passwords()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving password: {e}")
        finally:
            self.db_utils.close_connection(conn)

    def delete_password(self, site):
        """Delete a password from the database."""
        confirm = messagebox.askyesno("Conferma Eliminazione", f"Sei sicuro di voler eliminare la password per {site}?")
        if confirm:
            conn = self.db_utils.get_database()
            try:
                query = "DELETE FROM passwords WHERE site = ? AND user_id = ?"
                params = (site, self.user_info[0])
                self.db_utils.execute_query(conn, query, params)
                self.display_passwords()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error deleting password: {e}")
            finally:
                self.db_utils.close_connection(conn)
