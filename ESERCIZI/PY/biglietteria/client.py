import socket
import tkinter as tk
from tkinter import messagebox

def connetti_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))
    return client

def ricevi_film(client):
    dati = client.recv(1024).decode()
    lista = dati.split(",")
    return [film for film in lista if film != ""]

def acquista():
    film = film_var.get()
    numero = entry_biglietti.get()

    if numero == "":
        messagebox.showerror("Errore", "Inserisci numero biglietti")
        return

    messaggio = film + "," + numero
    client.send(messaggio.encode())

    risposta = client.recv(1024).decode()
    messagebox.showinfo("Risposta server", risposta)

    entry_biglietti.delete(0, tk.END)

# Connessione
client = connetti_server()
film_disponibili = ricevi_film(client)

# GUI
root = tk.Tk()
root.title("Biglietteria Cinema")

film_var = tk.StringVar(root)
film_var.set(film_disponibili[0])

tk.Label(root, text="Seleziona film").pack(pady=5)
tk.OptionMenu(root, film_var, *film_disponibili).pack(pady=5)

tk.Label(root, text="Numero biglietti").pack(pady=5)
entry_biglietti = tk.Entry(root)
entry_biglietti.pack(pady=5)

tk.Button(root, text="Acquista", command=acquista).pack(pady=10)

root.mainloop()
client.close()
