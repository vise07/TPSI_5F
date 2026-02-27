import socket
import threading

# Archivio camere: tipologia -> [disponibili, prezzo_notte]
camere = {
    "Singola": [5, 50.00],
    "Doppia": [4, 80.00],
    "Suite": [2, 150.00]
}

# Calcolo sconto in base alle notti
def calcola_sconto(notti):
    if notti >= 6:
        return 0.20
    elif notti >= 3:
        return 0.10
    return 0.0

def gestisci_cliente(client, indirizzo):
    print("Connessione da:", indirizzo)

    # Invio elenco camere al client
    elenco = ""
    for tipo, dati in camere.items():
        elenco += f"{tipo}|{dati[0]}|{dati[1]};"

    client.send(elenco.encode())

    richiesta = client.recv(1024).decode()
    tipo_camera, notti = richiesta.split("|")

    # Controllo input numerico
    if not notti.isdigit():
        client.send("ERRORE|Numero notti non valido".encode())
        client.close()
        return

    notti = int(notti)

    if notti <= 0:
        client.send("ERRORE|Le notti devono essere maggiori di zero".encode())
        client.close()
        return

    if tipo_camera not in camere:
        client.send("ERRORE|Camera non trovata".encode())
        client.close()
        return

    disponibili, prezzo = camere[tipo_camera]

    if disponibili <= 0:
        client.send("ERRORE|Camere non disponibili".encode())
        client.close()
        return

    totale = prezzo * notti
    perc_sconto = calcola_sconto(notti)
    valore_sconto = totale * perc_sconto
    finale = totale - valore_sconto

    # Aggiornamento disponibilità
    camere[tipo_camera][0] -= 1

    risposta = f"OK|{totale:.2f}|{perc_sconto*100:.0f}|{valore_sconto:.2f}|{finale:.2f}"
    client.send(risposta.encode())

    client.close()
    print("Connessione chiusa:", indirizzo)

def avvia_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12346))
    server.listen(5)

    print("Server Hotel attivo sulla porta 12346...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=gestisci_cliente, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    avvia_server()