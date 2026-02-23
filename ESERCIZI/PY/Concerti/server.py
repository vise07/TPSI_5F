import socket
import threading

# Dizionario concerti
concerti = {
    "Vasco Rossi": {"data": "10/07/2026", "prezzo": 50, "posti": 5},
    "Ultimo": {"data": "15/07/2026", "prezzo": 40, "posti": 8},
    "Måneskin": {"data": "20/07/2026", "prezzo": 45, "posti": 6}
}

def gestione_client(conn, addr):
    print("Connessione da", addr)

    # Invio lista concerti al client
    lista_concerti = ""
    for nome in concerti:
        lista_concerti += nome + ","
    conn.sendall(lista_concerti.encode())

    try:
        data = conn.recv(1024).decode()
        nome, numero = data.split(",")

        try:
            numero = int(numero)

            if numero <= 0:
                risposta = "Errore: numero di biglietti non valido"

            elif numero > concerti[nome]["posti"]:
                risposta = "Errore: posti insufficienti"

            else:
                prezzo = concerti[nome]["prezzo"]
                totale = prezzo * numero
                sconto = 0

                # Sconto 10% per 3 o più biglietti
                if numero >= 3:
                    sconto = totale * 0.10

                finale = totale - sconto

                risposta = (
                    f"Concerto: {nome}\n"
                    f"Data: {concerti[nome]['data']}\n"
                    f"Totale: {totale}€\n"
                    f"Sconto: {sconto}€\n"
                    f"Da pagare: {finale}€"
                )

                # Aggiorno posti disponibili
                concerti[nome]["posti"] -= numero

        except:
            risposta = "Errore: inserisci un numero valido"

        conn.sendall(risposta.encode())

    except:
        print("Errore comunicazione")

    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)
    print("Server concerti avviato...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=gestione_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
