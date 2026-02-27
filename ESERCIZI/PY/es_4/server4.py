import socket
import threading

# Menu pizze: nome -> prezzo
menu_pizze = {
    "Margherita": 6.00,
    "Diavola": 7.50,
    "Capricciosa": 8.00,
    "Quattro Formaggi": 8.50
}

def calcola_sconto(totale):
    if totale >= 30:
        return 0.10
    return 0.0

def gestisci_cliente(client, indirizzo):
    print("Connessione da:", indirizzo)

    # Invio menu al client
    elenco = ""
    for nome, prezzo in menu_pizze.items():
        elenco += f"{nome}|{prezzo};"

    client.send(elenco.encode())

    ordine = client.recv(1024).decode()

    if not ordine:
        client.close()
        return

    totale = 0

    prodotti = ordine.split(";")

    for voce in prodotti:
        if voce:
            nome, quantita = voce.split("|")

            if nome not in menu_pizze:
                client.send("ERRORE|Prodotto non valido".encode())
                client.close()
                return

            if not quantita.isdigit() or int(quantita) <= 0:
                client.send("ERRORE|Quantità non valida".encode())
                client.close()
                return

            quantita = int(quantita)
            totale += menu_pizze[nome] * quantita

    sconto_perc = calcola_sconto(totale)
    valore_sconto = totale * sconto_perc
    finale = totale - valore_sconto

    risposta = f"OK|{totale:.2f}|{sconto_perc*100:.0f}|{valore_sconto:.2f}|{finale:.2f}"
    client.send(risposta.encode())

    client.close()
    print("Connessione chiusa:", indirizzo)

def avvia_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12347))
    server.listen(5)

    print("Server Pizzeria attivo sulla porta 12347...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=gestisci_cliente, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    avvia_server()