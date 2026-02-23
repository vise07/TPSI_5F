import socket
import threading

concerti = {
    "Travis Scott": {"data": "12/02/2027", "prezzo": 90, "posti": 9},
    "Drake": {"data": "24/07/2026", "prezzo": 70, "posti": 7},
    "Sfera": {"data": "11/08/2026", "prezzo": 40, "posti": 3}
}



def gestione_client(conn, addr):
    print(f"connessione con {addr}.")

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
                    risposta = "Numero biglietti non valido."

                elif numero > concerti[nome]["posti"]:
                    risposta = "Numero biglietti insufficiente"

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
                        f"Prezzo: {prezzo}\n"
                        f"Sconto: {sconto}\n"
                        f"Da pagare: {finale}\n"
                    )

                    concerti[nome]["posti"] -= numero

            except:
                risposta = "Inserimento client errato."

            conn.sendall(risposta.encode())

        except:
            break

    print(f"Chiusura connessione con {addr}")
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