import socket
import tkinter as tk
from tkinter import ttk, messagebox

connessione = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connessione.connect(("localhost", 12345))

catalogo = {}

def carica_film():
    risposta = connessione.recv(1024).decode()
    elementi = risposta.split(";")

    for voce in elementi:
        if voce:
            nome, disp, costo = voce.split("|")
            catalogo[nome] = [int(disp), float(costo)]

    combo_film["values"] = list(catalogo.keys())
    if catalogo:
        combo_film.current(0)
        mostra_info()

def mostra_info(event=None):
    film_scelto = combo_film.get()
    if film_scelto in catalogo:
        posti, prezzo = catalogo[film_scelto]
        label_info.config(
            text=f"Disponibili: {posti}  |  Prezzo: €{prezzo:.2f}"
        )

def acquista():
    film = combo_film.get()
    quantita = campo_biglietti.get()

    if not quantita.isdigit() or int(quantita) <= 0:
        messagebox.showerror("Errore", "Inserire un numero valido")
        return

    richiesta = f"{film}|{quantita}"
    connessione.sendall(richiesta.encode())

    esito = connessione.recv(1024).decode().split("|")

    if esito[0] == "OK":
        totale, sconto_perc, sconto_val, finale = esito[1:]

        messaggio = (
            f"Film: {film}\n"
            f"Biglietti: {quantita}\n"
            f"Totale: €{totale}\n"
            f"Sconto: {sconto_perc}% (-€{sconto_val})\n"
            f"Da pagare: €{finale}"
        )

        messagebox.showinfo("Operazione completata", messaggio)
        connessione.close()
        finestra.destroy()
    else:
        messagebox.showerror("Errore", esito[1])

    campo_biglietti.delete(0, tk.END)


# --- Interfaccia grafica ---

finestra = tk.Tk()
finestra.title("Cinema - Prenotazione")

tk.Label(finestra, text="Scegli un film").pack(pady=8)

combo_film = ttk.Combobox(finestra, state="readonly", width=28)
combo_film.pack()
combo_film.bind("<<ComboboxSelected>>", mostra_info)

label_info = tk.Label(finestra, text="")
label_info.pack(pady=5)

tk.Label(finestra, text="Quantità biglietti").pack()

campo_biglietti = tk.Entry(finestra)
campo_biglietti.pack(pady=5)

tk.Button(finestra, text="Conferma acquisto", command=acquista).pack(pady=10)

carica_film()
finestra.mainloop()
