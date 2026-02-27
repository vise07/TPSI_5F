import socket
import threading

# Archivio veicoli: modello -> [disponibili, costo_giornaliero]
veicoli = {
    "Fiat Panda": [3, 35.00],
    "Ford Focus": [2, 50.00],
    "BMW Serie 3": [1, 90.00]
}

# Calcolo sconto per noleggi lunghi
def calcola_sconto(giorni):
    if giorni >= 10:
        return 0.20
    elif giorni >= 5:
        return 0.10
    return 0.0

def gestisci_cliente(client, indirizzo):
    print("Connessione da:", indirizzo)

    # Invio elenco veicoli
    elenco = ""
    for modello, dati in veicoli.items():
        elenco += f"{modello}|{dati[0]}|{dati[1]};"

    client.send(elenco.encode())

    richiesta = client.recv(1024).decode()
    modello_scelto, giorni = richiesta.split("|")

    # Controllo input numerico
    if not giorni.isdigit():
        client.send("ERRORE|Numero giorni non valido".encode())
        client.close()
        return

    giorni = int(giorni)

    if giorni <= 0:
        client.send("ERRORE|I giorni devono essere maggiori di zero".encode())
        client.close()
        return

    if modello_scelto not in veicoli:
        client.send("ERRORE|Veicolo non trovato".encode())
        client.close()
        return

    disponibili, costo = veicoli[modello_scelto]

    if disponibili <= 0:
        client.send("ERRORE|Veicolo non disponibile".encode())
        client.close()
        return

    totale = costo * giorni
    perc_sconto = calcola_sconto(giorni)
    valore_sconto = totale * perc_sconto
    finale = totale - valore_sconto

    # Aggiornamento disponibilità
    veicoli[modello_scelto][0] -= 1

    risposta = f"OK|{totale:.2f}|{perc_sconto*100:.0f}|{valore_sconto:.2f}|{finale:.2f}"
    client.send(risposta.encode())

    client.close()
    print("Connessione chiusa:", indirizzo)

def avvia_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12348))
    server.listen(5)

    print("Server Noleggio Auto attivo sulla porta 12348...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=gestisci_cliente, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    avvia_server()