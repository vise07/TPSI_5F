import socket
import random
import threading

#Definizione funzione istanza di gioco
def gameInstance(conn, addr):
    #Generazione numero casuale tra 1 e 100
    number = random.randint(1,100)
    print(f"Connessione stabilita con {addr}")
    #Loop che riceve il numero inserito dall'utente e risponde
    while True:
        #Ricezione numero dall'utente, decodifica (decode()) e casting in int
        data = conn.recv(1024).decode()
        guess = int(data)
        #Possibili risposte: L'utente indovina; Il numero è >; Il numero è <
        if guess == number:
            response = "Hai vinto!"
            conn.send(response.encode())
            break
        elif guess > number:
            response = "Troppo alto!"
        elif guess < number:
            response = "Troppo basso!"
        #Invio risposta come sequenza di byte (encode()) al client
        conn.send(response.encode())
    #Chiusura connessione con il client una volta indovinato il numero    
    conn.close()
    print(f"Connessione terminata con {addr}")

def start_server():
    #Inizializzazione lato server della socket su porta 12345
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("Server in ascolto sulla porta 12345...")
    #Loop che accetta continuamente le nuove connessioni
    while True:
        conn, addr = server_socket.accept()
        '''Inizializzazione thread(Processo a sè stante che esegue
           la funzione di gioco per l'istanza corrente)'''
        client_thread = threading.Thread(
            #target: Funzione che il thread eseguirà
            target=gameInstance,
            #args: Argomenti che verranno passati alla funzione passata come target
            args=(conn,addr)
        )     
        #Avvio del thread               
        client_thread.start()

#Chiamata della funzione 'start_server' in main
if __name__ == "__main__":
    start_server()        