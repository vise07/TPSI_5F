import socket
import threading

concerti = {
    "Travis Scott": {"data": "10/10/2026", "prezzo": 50, "posti": 4},
    "Drake": {"data": "23/04/2027", "prezzo": 30, "posti": 5},
    "IDK": {"data": "17/03/2026", "prezzo": 20, "posti": 2}
}

def gestione_client(conn, addr):
    print("Connessione da", addr)

    lista_concerti = ",".join(concerti.keys())
    conn.sendall(lista_concerti.encode())

    while True:
        try:
            data = conn.recv(1024).decode()

            if not data:
                break

            nome, numero = data.split(",")

            try:
                numero = int(numero)

                if numero <= 0:
                    risposta = "Errore: numero non valido"

                elif numero > concerti[nome]["posti"]:
                    risposta = "Errore: posti insufficienti"

                else:
                    prezzo = concerti[nome]["prezzo"]
                    totale = prezzo * numero
                    sconto = 0

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

                    concerti[nome]["posti"] -= numero

            except:
                risposta = "Errore: inserisci numero valido"

            conn.sendall(risposta.encode())

        except:
            break

    print("Client disconnesso", addr)
    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server in ascolto...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target = gestione_client, args = (conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()    