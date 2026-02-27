import socket
import tkinter as tk
from tkinter import messagebox

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(("127.0.0.1", 12347))

menu = {}

def carica_menu():
    risposta = conn.recv(1024).decode()
    elementi = risposta.split(";")

    for voce in elementi:
        if voce:
            nome, prezzo = voce.split("|")
            menu[nome] = float(prezzo)

    crea_interfaccia()

def invia_ordine():
    ordine = ""

    for nome in menu:
        quantita = campi_quantita[nome].get()

        if quantita:
            if not quantita.isdigit() or int(quantita) <= 0:
                messagebox.showerror("Errore", f"Quantità non valida per {nome}")
                return

            ordine += f"{nome}|{quantita};"

    if ordine == "":
        messagebox.showerror("Errore", "Nessun prodotto selezionato")
        return

    conn.sendall(ordine.encode())

    risposta = conn.recv(1024).decode().split("|")

    if risposta[0] == "OK":
        totale, perc, sconto, finale = risposta[1:]

        messaggio = (
            f"Totale: €{totale}\n"
            f"Sconto: {perc}% (-€{sconto})\n"
            f"Importo finale: €{finale}"
        )

        messagebox.showinfo("Ordine completato", messaggio)
        conn.close()
        finestra.destroy()
    else:
        messagebox.showerror("Errore", risposta[1])

def crea_interfaccia():
    global campi_quantita
    campi_quantita = {}

    riga = 0
    for nome, prezzo in menu.items():
        tk.Label(finestra, text=f"{nome} - €{prezzo:.2f}").grid(row=riga, column=0, padx=10, pady=5)
        entry = tk.Entry(finestra, width=5)
        entry.grid(row=riga, column=1)
        campi_quantita[nome] = entry
        riga += 1

    tk.Button(finestra, text="Invia Ordine", command=invia_ordine)\
        .grid(row=riga, columnspan=2, pady=10)


# --- Finestra principale ---

finestra = tk.Tk()
finestra.title("Pizzeria - Ordini")

carica_menu()
finestra.mainloop()