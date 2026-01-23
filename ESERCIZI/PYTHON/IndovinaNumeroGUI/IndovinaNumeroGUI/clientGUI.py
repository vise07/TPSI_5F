import socket
import tkinter as tk
from tkinter import messagebox

# Inizializzazione lato client della socket su porta 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

#Realizzazione interfaccia di gioco 
def gameInterface():
    #Assegnazione del contenuto della box di testo a 'guess'
    guess = entry.get()
    #Controllo che il contenuto inserito nella box di testo sia un numero
    if not guess.isdigit():
        #Dovesse non essere un numero, mostro un errore
        messagebox.showerror("Errore", "Inserisci un numero valido")
        return
    #Invio del valore inserito nella box di testo al server sotto forma di sequenza di byte
    client_socket.sendall(guess.encode())
    
    #Ricezione risposta server e decodifica
    response = client_socket.recv(1024).decode()
    #Mostro su schermo in un message box la risposta del server
    messagebox.showinfo("Risposta dal server", response)
    Primo 
    '''Dovesse aver indovinato l'utente si chiude la connessione con 
     il client e si chiude la finestra (root.destroy()) '''
    if response == "Hai vinto!":
        client_socket.close()
        root.destroy()

    #Dopo ogni tentativo di indovinare dell'utente, si svuota la box di testo
    entry.delete(0, tk.END)

#Inizializzazione finestra (tk.Tk()) nella variabile root
root = tk.Tk()
#Assegnazione titolo alla finestra
root.title("Gioco dei numeri")
#Creazione testo di sottotitolo (Label) all'interno della finestra
label = tk.Label(root, text="Inserisci un numero") #1° arg:Finestra in cui va il testo, 2° arg: Il testo stesso
#Regolazione posizione del label con padding verticale (pady) di 5
label.pack(pady=5)
#Creazione box di testo (Entry) per inserimento numeri all'interno della finestra
entry = tk.Entry(root) #1° arg:Finestra in cui va la box di testo
#Regolazione posizione della message box con padding verticale (pady) di 5
entry.pack(pady=5)
#Creazione bottone (Button) per invio numero all'interno della finestra
button = tk.Button(root, text = "Invia", command=gameInterface)
#Regolazione posizione del bottone con padding verticale (pady) di 10
button.pack(pady=10)
#Inizializzazione loop principale di Tkinter che tiene aperta la finestra e attende il click del bottone
root.mainloop()