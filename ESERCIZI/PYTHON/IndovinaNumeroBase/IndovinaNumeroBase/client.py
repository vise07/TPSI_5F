import socket

def start_client():
    # Inizializzazione lato client della socket su porta 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    #Realizzazione logica di gioco 
    while True:
        #Inserimento numero
        guess = input("Inserisci un numero da provare:")
        #Invio il numero sotto forma di sequenza di byte (encode())
        client_socket.sendall(guess.encode())
        #Ricezione risposta server e decodifica della sequenza di byte (decode())
        data = client_socket.recv(1024).decode()
        #Presentazione su schermo della risposta ricevuta
        print(data)
        #Indovinato il numero giusto, si esce dal loop
        if data == 'Hai vinto!':
            break
    #Uscito dal loop si interrompe la connessione del client        
    client_socket.close()

#Chiamata della funzione 'start_client' in main
if __name__ == "__main__":
    start_client()