import socket
import threading

disponibilita = 10

def gestione_client(conn, addr):
    global disponibilita
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            parti = data.split(",")
            if len(parti) != 2:
                conn.send("Errore richiesta".encode())
                continue

            if disponibilita > 0:
                disponibilita -= 1
                risposta = "Taxi disponibile. Rimasti: " + str(disponibilita)
            else:
                risposta = "Taxi non disponibile"

            conn.send(risposta.encode())
        except:
            break

    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=gestione_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
