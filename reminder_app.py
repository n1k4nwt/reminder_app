import sqlite3
import os
from colorama import Fore, Back, Style
from terminaltables import SingleTable

def anzeigen_erinnerungen(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM erinnerungen")
    erinnerungen = cursor.fetchall()
    
    if not erinnerungen:
        print("Keine Erinnerungen vorhanden.")
    else:
        table_data = [["Index", "Erinnerung"]]
        for erinnerung in erinnerungen:
            index, text = erinnerung
            table_data.append([str(index), text])

        table = SingleTable(table_data)
        table.title = "Erinnerungen"
        table.inner_row_border = True

        print(table.table)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear_console()
    print(Fore.CYAN + "-----------------------------")
    print(Fore.YELLOW + "       ERINNERUNGS-APP       ")
    print(Fore.CYAN + "-----------------------------")
    print(Fore.GREEN + "1. Erinnerung hinzufügen")
    print("2. Erinnerung bearbeiten")
    print("3. Erledigte Erinnerung(en) entfernen")
    print("4. Erinnerungen anzeigen")
    print("0. Beenden")
    print(Style.RESET_ALL)

def erinnerungs_app():
    conn = sqlite3.connect("erinnerungen.db")
    cursor = conn.cursor()
    
    # Tabelle erstellen, falls sie noch nicht existiert
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS erinnerungen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    """)
    
    while True:
        print_menu()

        auswahl = input("Wählen Sie eine Option: ")

        if auswahl == "1":
            neue_erinnerung = input("Geben Sie die neue Erinnerung ein: ")
            cursor.execute("INSERT INTO erinnerungen (text) VALUES (?)", (neue_erinnerung,))
            conn.commit()
            print("Erinnerung hinzugefügt.")
        elif auswahl == "2":
            anzeigen_erinnerungen(conn)
            index = int(input("Geben Sie die Nummer der zu bearbeitenden Erinnerung ein: "))
            cursor.execute("SELECT * FROM erinnerungen WHERE id = ?", (index,))
            erinnerung = cursor.fetchone()
            if erinnerung:
                neue_erinnerung = input("Geben Sie die neue Erinnerung ein: ")
                cursor.execute("UPDATE erinnerungen SET text = ? WHERE id = ?", (neue_erinnerung, index))
                conn.commit()
                print("Erinnerung bearbeitet.")
            else:
                print("Ungültige Nummer.")
        elif auswahl == "3":
            anzeigen_erinnerungen(conn)
            index_list = input("Geben Sie die Indexnummern der erledigten Erinnerungen ein (durch Komma getrennt): ")
            index_list = index_list.split(",")
            erledigte_erinnerungen = []
            for index in index_list:
                cursor.execute("SELECT * FROM erinnerungen WHERE id = ?", (index,))
                erinnerung = cursor.fetchone()
                if erinnerung:
                    erledigte_erinnerungen.append(index)
                    cursor.execute("DELETE FROM erinnerungen WHERE id = ?", (index,))
                    conn.commit()
            if erledigte_erinnerungen:
                print(f"{len(erledigte_erinnerungen)} Erinnerung(en) entfernt.")
            else:
                print("Ungültige Indexnummer(n).")
        elif auswahl == "4":
            anzeigen_erinnerungen(conn)
        elif auswahl == "0":
            break
        else:
            print("Ungültige Auswahl.")

        input("\nDrücken Sie die Eingabetaste, um fortzufahren...")
        clear_console()

    clear_console()
    conn.close()

erinnerungs_app()
