import socket
import threading

lista_film = {
        "Inception": {
            "prezzo": 12,
            "biglietti": 4
        },
        "Fight club": {
            "prezzo": 10,
            "biglietti": 5
        },
        "Interstellar": {
            "prezzo": 8,
            "biglietti": 3
        }
    }

lock = threading.lock()

def gestione_client(conn, addr):
    print(f"Connessione effettuata con {addr}")

    conn.sendall(str(lista_film.encode()))

    data = conn.recv(1024).decode()

    if not data:
        return

    nome, numero = data.split(",")
    num = int(numero)

    with lock:
        if nome not in lista_film:
            print("Nome film non valido.")
            return
        
        if num <= 0:
            print("Inserimento numero biglietti non valido")
            return







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
