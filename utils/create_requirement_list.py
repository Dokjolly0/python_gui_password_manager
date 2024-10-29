import os
import sys
import subprocess

def get_installed_packages():
    """Restituisce un elenco di pacchetti installati manualmente."""
    # Ottieni l'elenco dei pacchetti installati
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
    # Restituisci solo le righe che non contengono '==' (indicando che non è un pacchetto installato)
    return result.stdout.strip().split('\n')

def generate_requirements_file(output_file='requirements.txt'):
    # Ottieni l'elenco dei pacchetti esterni
    external_packages = get_installed_packages()

    # Scrivi l'elenco dei pacchetti in requirements.txt
    with open(output_file, 'w') as f:
        f.write('\n'.join(external_packages))

    print(f"requirements.txt è stato generato con successo in {output_file}.")

if __name__ == "__main__":
    generate_requirements_file()
