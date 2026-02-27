import socket
import tkinter as tk
from tkinter import ttk, messagebox

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(("localhost", 12346))

catalogo_camere = {}

def carica_camere():
    risposta = conn.recv(1024).decode()
    elementi = risposta.split(";")

    for voce in elementi:
        if voce:
            tipo, disp, prezzo = voce.split("|")
            catalogo_camere[tipo] = [int(disp), float(prezzo)]

    combo_camere["values"] = list(catalogo_camere.keys())

    if catalogo_camere:
        combo_camere.current(0)
        aggiorna_info()

def aggiorna_info(event=None):
    scelta = combo_camere.get()
    if scelta in catalogo_camere:
        disp, prezzo = catalogo_camere[scelta]
        label_info.config(
            text=f"Disponibili: {disp}  |  Prezzo per notte: €{prezzo:.2f}"
        )

def prenota():
    tipo = combo_camere.get()
    notti = campo_notti.get()

    # Controllo input
    if not notti.isdigit() or int(notti) <= 0:
        messagebox.showerror("Errore", "Inserire un numero valido di notti")
        return

    richiesta = f"{tipo}|{notti}"
    conn.sendall(richiesta.encode())

    risposta = conn.recv(1024).decode().split("|")

    if risposta[0] == "OK":
        totale, perc, sconto, finale = risposta[1:]

        riepilogo = (
            f"Camera: {tipo}\n"
            f"Notti: {notti}\n"
            f"Totale: €{totale}\n"
            f"Sconto: {perc}% (-€{sconto})\n"
            f"Importo finale: €{finale}"
        )

        messagebox.showinfo("Prenotazione confermata", riepilogo)
        conn.close()
        finestra.destroy()
    else:
        messagebox.showerror("Errore", risposta[1])

    campo_notti.delete(0, tk.END)


# --- Interfaccia grafica ---

finestra = tk.Tk()
finestra.title("Prenotazione Hotel")

tk.Label(finestra, text="Seleziona una camera").pack(pady=8)

combo_camere = ttk.Combobox(finestra, state="readonly", width=25)
combo_camere.pack()
combo_camere.bind("<<ComboboxSelected>>", aggiorna_info)

label_info = tk.Label(finestra, text="")
label_info.pack(pady=5)

tk.Label(finestra, text="Numero di notti").pack()

campo_notti = tk.Entry(finestra)
campo_notti.pack(pady=5)

tk.Button(finestra, text="Prenota", command=prenota).pack(pady=10)

carica_camere()
finestra.mainloop()