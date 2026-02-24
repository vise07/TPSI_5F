import socket
import threading

lock = threading.Lock()

concerti = {
    "Travis Scott": {"data": "23/02/2027", "prezzo": 60, "posti": 8},
    "drake": {"data": "12/10/2027", "prezzo": 50, "posti": 13},
    "IDK": {"data": "06/05/2026", "prezzo": 30, "posti": 3}
}

def gestione_client(conn, addr):
    print(f"Connessione con {addr}.")

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
                    risposta = "Numero biglietti non valido"

                else:
                    with lock:

                        if nome not in concerti:
                            risposta = "Concerto non trovato"

                        elif numero > concerti[nome]["posti"]:
                            risposta = "Non abbastanza biglietti disponibili"

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
                risposta = "Inserimento dati errato"

            conn.sendall(risposta.encode())

        except:
            break

    print(f"Fine connessione con {addr}.")
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