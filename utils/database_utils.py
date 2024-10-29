import sqlite3
import os

class DBConfig:
    """Classe per gestire i parametri di configurazione del database."""
    def __init__(self, path=".", name="users.db"):
        self.path = path
        self.name = name

class DatabaseUtils:
    def __init__(self, config):
        """Inizializza l'oggetto con i parametri dell'interfaccia."""
        self.config = config

    def create_database(self):
        """Crea un database SQLite se non esiste già, utilizzando i parametri forniti."""
        db_file = os.path.join(self.config.path, self.config.name)  # Combina path e nome del database
        try:
            # Controlla se il percorso della cartella esiste
            if not os.path.exists(self.config.path):
                raise FileNotFoundError(f"La cartella '{self.config.path}' non esiste.")

            # Controlla se il file del database esiste già
            if not os.path.exists(db_file):
                # Crea un file vuoto per il database
                open(db_file, 'w').close()
                #print(f"Database '{db_file}' creato.")
            else:
                print(f"Database '{db_file}' già esistente.")

            return db_file  # Restituisce il percorso completo del database
        except FileNotFoundError as e:
            print("Path non esistente:", e)
            exit()
        except Exception as e:
            print(f"Si è verificato un errore imprevisto: {e}")  # Gestisce altri errori
            exit()

    def create_connection(self, db_file):
        """Crea una connessione al database SQLite."""
        try:
            conn = sqlite3.connect(db_file)
            #print(f"Connessione al database '{db_file}' riuscita.")
            return conn
        except sqlite3.Error as e:
            print(f"Errore nella connessione al database: {e}")
            return None
    
    def close_connection(self, conn):
        """Chiude la connessione al database."""
        if conn:
            try:
                conn.close()
                #print("Connessione chiusa.")
            except sqlite3.Error as e:
                print(f"Errore nella chiusura della connessione: {e}")

    def execute_query(self, conn, query, params=()):
        """
        Esegue una query SQL sul database, esempi: 
        Cerca un utente -> SELECT * FROM users WHERE username = ?
        
        Inserisci un utente -> INSERT INTO users(username, password) VALUES(?, ?)
        
        Crea la tabella user -> CREATE TABLE IF NOT EXISTS users (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            username TEXT NOT NULL,
                                            password TEXT NOT NULL
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()  # Impegna le modifiche
            #print("Query eseguita con successo.")
            return cursor  # Restituisce il cursore per ulteriori operazioni, se necessario
        except sqlite3.Error as e:
            print(f"Errore nell'esecuzione della query: {e}")
            
    def get_database(self):
        """Ottiene una connessione al database esistente o crea un nuovo database se non esiste."""
        try:
            db_file = os.path.join(self.config.path, self.config.name)  # Combina path e nome del database
            # Verifica se il file del database esiste
            if not os.path.exists(db_file):
                raise FileNotFoundError
        except FileNotFoundError:
            print("Database non esistente")
            exit()

        # Crea una connessione al database
        conn = self.create_connection(db_file)
        return conn

# # Esempio
# # Crea un oggetto di configurazione
# db_config = DBConfig(path=".", name="user.db") 
# # Crea un'istanza di DatabaseUtils con il file di configurazione
# db_utils = DatabaseUtils(db_config)
# db_file = db_utils.create_database()
# conn = db_utils.create_connection(db_file)

# # Crea la tabella utenti
# db_utils.execute_query(conn, """CREATE TABLE IF NOT EXISTS users (
#                                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                     username TEXT NOT NULL,
#                                     password TEXT NOT NULL
#                                 );""")
# # Inserisci un utente
# db_utils.execute_query(conn, "INSERT INTO users(username, password) VALUES(?, ?)", ("alex", "alex"))
# # Esegui una query di selezione per cercare l'utente
# cursor = db_utils.execute_query(conn, "SELECT * FROM users WHERE username = ?", ("alex",))
# if cursor:
#     results = cursor.fetchall()  # Recupera tutti i risultati
#     for row in results:
#         print(f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}")
# # Chiudi la connessione
# db_utils.close_connection(conn)
