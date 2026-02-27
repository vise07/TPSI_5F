import socket
import tkinter as tk
from tkinter import ttk, messagebox

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(("127.0.0.1", 12348))

catalogo_auto = {}

def carica_auto():
    risposta = conn.recv(1024).decode()
    elementi = risposta.split(";")

    for voce in elementi:
        if voce:
            modello, disp, costo = voce.split("|")
            catalogo_auto[modello] = [int(disp), float(costo)]

    combo_auto["values"] = list(catalogo_auto.keys())

    if catalogo_auto:
        combo_auto.current(0)
        aggiorna_info()

def aggiorna_info(event=None):
    scelta = combo_auto.get()
    if scelta in catalogo_auto:
        disp, costo = catalogo_auto[scelta]
        label_info.config(
            text=f"Disponibili: {disp}  |  Costo giornaliero: €{costo:.2f}"
        )

def noleggia():
    modello = combo_auto.get()
    giorni = campo_giorni.get()

    # Controllo input
    if not giorni.isdigit() or int(giorni) <= 0:
        messagebox.showerror("Errore", "Inserire un numero valido di giorni")
        return

    richiesta = f"{modello}|{giorni}"
    conn.sendall(richiesta.encode())

    risposta = conn.recv(1024).decode().split("|")

    if risposta[0] == "OK":
        totale, perc, sconto, finale = risposta[1:]

        riepilogo = (
            f"Auto: {modello}\n"
            f"Giorni: {giorni}\n"
            f"Totale: €{totale}\n"
            f"Sconto: {perc}% (-€{sconto})\n"
            f"Importo finale: €{finale}"
        )

        messagebox.showinfo("Noleggio confermato", riepilogo)
        conn.close()
        finestra.destroy()
    else:
        messagebox.showerror("Errore", risposta[1])

    campo_giorni.delete(0, tk.END)


# --- Interfaccia grafica ---

finestra = tk.Tk()
finestra.title("Noleggio Auto")

tk.Label(finestra, text="Seleziona un veicolo").pack(pady=8)

combo_auto = ttk.Combobox(finestra, state="readonly", width=25)
combo_auto.pack()
combo_auto.bind("<<ComboboxSelected>>", aggiorna_info)

label_info = tk.Label(finestra, text="")
label_info.pack(pady=5)

tk.Label(finestra, text="Numero di giorni").pack()

campo_giorni = tk.Entry(finestra)
campo_giorni.pack(pady=5)

tk.Button(finestra, text="Noleggia", command=noleggia).pack(pady=10)

carica_auto()
finestra.mainloop()