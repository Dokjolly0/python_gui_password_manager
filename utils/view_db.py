from database_utils import DBConfig, DatabaseUtils

def main():
    # Configurazione del database
    db_config = DBConfig(path=".", name="user.db")
    db_utils = DatabaseUtils(db_config)
    # Ottieni la connessione al database
    conn = db_utils.get_database()
    # Esegui una query per selezionare tutti gli utenti
    cursor = db_utils.execute_query(conn, "SELECT * FROM users;")
    
    if cursor:
        results = cursor.fetchall()  # Recupera tutti i risultati
        if results:  # Controlla se ci sono risultati
            print("Elenco degli utenti:")
            for row in results:
                print(f"ID: {row[0]}, Nome: {row[1]}, Cognome: {row[2]}, Username: {row[3]}, PW: {row[4]}")
        else:
            print("Nessun utente trovato.")
    else:
        print("Si è verificato un errore nell'esecuzione della query.")

    # Chiudi la connessione
    db_utils.close_connection(conn)

if __name__ == "__main__":
    main()
