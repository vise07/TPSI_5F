import socket
import tkinter as tk
from tkinter import messagebox


def connetti_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))
    return client


def ricevi_concerti(client):
    data = client.recv(1024).decode()
    lista = data.split(",")
    return lista


def acquista():
    concerto = concerto_var.get()
    numero = entry_biglietti.get()

    if numero == "":
        messagebox.showerror("Errore", "Inserisci numero biglietti")
        return
    
    messaggio = concerto + "," + numero
    client.sendall(messaggio.encode())

    risposta = client.recv(1024).decode()
    messagebox.showinfo("Riepilogo acquisto", risposta)

    entry_biglietti.delete(0, tk.END)


client = connetti_server()
concerti_disponibili = ricevi_concerti(client)

root = tk.Tk()
root.title("Vendita Biglietti Concerti")

concerto_var = tk.StringVar(root)
concerto_var.set(concerti_disponibili[0])

tk.Label(root, text = "Seleziona concerto").pack(pady = 5)
tk.OptionMenu(root, concerto_var, *concerti_disponibili).pack(pady = 5)

tk.Label(root, text = "Numero biglietti").pack(pady = 5)
entry_biglietti = tk.Entry(root)
entry_biglietti.pack(pady = 5)

tk.Button(root, text = "Acquista biglietti", command = acquista).pack(pady = 10)

root.mainloop()
client.close()
