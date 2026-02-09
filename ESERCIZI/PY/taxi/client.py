import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    while True:
        partenza = input("Città di partenza: ")
        if partenza == "exit":
            break
        arrivo = input("Città di arrivo: ")

        richiesta = partenza + "," + arrivo
        client_socket.sendall(richiesta.encode())

        risposta = client_socket.recv(1024).decode()
        print(risposta)

    client_socket.close()

if __name__ == "__main__":
    start_client()
