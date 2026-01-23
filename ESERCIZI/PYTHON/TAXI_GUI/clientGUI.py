import socket
import tkinter as tk
from tkinter import messagebox

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

def richiesta_taxi():
    partenza = entry_partenza.get()
    arrivo = entry_arrivo.get()

    if partenza == "" or arrivo == "":
        messagebox.showerror("Errore", "Inserisci entrambe le città")
        return

    messaggio = partenza + "," + arrivo
    client_socket.sendall(messaggio.encode())

    risposta = client_socket.recv(1024).decode()
    messagebox.showinfo("Risposta server", risposta)

    entry_partenza.delete(0, tk.END)
    entry_arrivo.delete(0, tk.END)

root = tk.Tk()
root.title("Prenotazione Taxi")

label1 = tk.Label(root, text="Città di partenza")
label1.pack(pady=5)

entry_partenza = tk.Entry(root)
entry_partenza.pack(pady=5)

label2 = tk.Label(root, text="Città di arrivo")
label2.pack(pady=5)

entry_arrivo = tk.Entry(root)
entry_arrivo.pack(pady=5)

button = tk.Button(root, text="Verifica disponibilità", command=richiesta_taxi)
button.pack(pady=10)

root.mainloop()
client_socket.close()
