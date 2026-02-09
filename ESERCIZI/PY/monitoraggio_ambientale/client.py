import socket
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
nGiorni, counter = 0, 0
daysData = []


def getNumDays(startWindow, entry):
    global nGiorni
    try:
        giorni = int(entry.get())
        if giorni <= 0:
            raise ValueError("Il numero di giorni deve essere maggiore di zero")
    except ValueError:
        messagebox.showinfo("Errore", "Il numero di giorni deve essere in formato numerico e maggiore di zero")
        return
    nGiorni = giorni
    startWindow.destroy()
    root.deiconify()

def clearEntries(window):
    for widget in window.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0, 'end')

def mainInterfaceLogic(entry1, entry2, entry3):
    global daysData, counter
    giorno = entry1.get()
    try:
        datetime.strptime(giorno, "%d/%m/%Y")
    except ValueError:
        messagebox.showinfo("Errore", "Formato non valido. Usa GG/MM/AAAA")
        return
    try:
        temp12 = int(entry2.get())
        temp24 = int(entry3.get())
    except ValueError:
        messagebox.showinfo("Errore", "Le temperature devono essere in formato numerico")
        return
    message = f"{giorno}|{temp12}|{temp24}."
    daysData.append(message)
    counter += 1
    (root.withdraw(), sendData(daysData)) if counter == nGiorni else clearEntries(root)

def sendData(data):
    for message in data:
        client_socket.sendall(message.encode())
    client_socket.sendall("fine.".encode())
    response = client_socket.recv(1024).decode()
    media, tempMin, tempMax = response.split("|")
    showResults(media,tempMin,tempMax)
    if response:
        client_socket.close()

def startWindowInit():
    startWindow = tk.Toplevel(root)
    startWindow.title("Invio Temperature Giornaliere – Stazione Meteo")
    label = tk.Label(startWindow, text="Per quanti giorni vuoi inserire i dati?")
    label.pack(pady=5)
    entry = tk.Entry(startWindow)
    entry.pack(pady=5)
    button = tk.Button(startWindow, text="Conferma", command=lambda: getNumDays(startWindow, entry))
    button.pack(pady=10)
    startWindow.geometry("500x100")
    return startWindow

def rootInit():
    root.geometry("300x250")
    label1 = tk.Label(root, text="Inserisci il giorno di rilevazione (GG/MM/AAAA)")
    label1.pack(pady=5)
    entry1 = tk.Entry(root)
    entry1.pack(pady=5)
    label2 = tk.Label(root, text="Inserisci la temperatura rilevata alle ore 12:00")
    label2.pack(pady=5)
    entry2 = tk.Entry(root)
    entry2.pack(pady=5)
    label3 = tk.Label(root, text="Inserisci la temperatura rilevata alle ore 24:00")
    label3.pack(pady=5)
    entry3 = tk.Entry(root)
    entry3.pack(pady=5)
    button1 = tk.Button(root, text="Invia dati", command=lambda: mainInterfaceLogic(entry1, entry2, entry3))
    button1.pack(pady=10)

def showResults(media, minTemp, maxTemp):
    message = (
        f"Numero giorni analizzati: {nGiorni}\n"
        f"Numero rilevazioni fatte: {nGiorni * 2}\n"
        f"Temperatura media: {media}\n"
        f"Temperatura minima: {minTemp}\n"
        f"Temperatura massima: {maxTemp}"
    )
    messagebox.showinfo("Risultati", message)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    rootInit()
    start_window = startWindowInit()
    root.mainloop()