import socket
import threading

# Archivio film: titolo -> [posti disponibili, prezzo]
archivio = {
    "Avatar": [50, 8.50],
    "Inception": [30, 7.00],
    "Interstellar": [40, 7.50],
    "The Matrix": [25, 6.50]
}

def sconto(qta):
    if qta >= 5:
        return 0.20
    elif qta >= 3:
        return 0.10
    return 0.0

def gestisci_connessione(client, indirizzo):
    print("Client collegato:", indirizzo)

    # Invio lista film
    elenco = ""
    for titolo, dati in archivio.items():
        elenco += f"{titolo}|{dati[0]}|{dati[1]};"

    client.send(elenco.encode())

    richiesta = client.recv(1024).decode()
    titolo_richiesto, numero = richiesta.split("|")
    numero = int(numero)

    if titolo_richiesto not in archivio:
        client.send("ERRORE|Film inesistente".encode())
        client.close()
        return

    disponibili, prezzo_unit = archivio[titolo_richiesto]

    if numero > disponibili:
        client.send("ERRORE|Posti insufficienti".encode())
        client.close()
        return

    totale = prezzo_unit * numero
    perc_sconto = sconto(numero)
    valore_sconto = totale * perc_sconto
    finale = totale - valore_sconto

    archivio[titolo_richiesto][0] -= numero

    risposta = f"OK|{totale:.2f}|{perc_sconto*100:.0f}|{valore_sconto:.2f}|{finale:.2f}"
    client.send(risposta.encode())

    client.close()
    print("Client disconnesso:", indirizzo)

def avvia_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)

    print("Server attivo sulla porta 12345...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=gestisci_connessione, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    avvia_server()
