import socket
import threading

# Dizionario film
movies = {
    "Oppenheimer": {"biglietti": 5, "prezzo": 8},
    "Interstellar": {"biglietti": 10, "prezzo": 7},
    "Barbie": {"biglietti": 6, "prezzo": 6}
}

def gestione_client(conn, addr):
    print("Connessione da", addr)

    # Invio lista film al client
    lista_film = ""
    for film in movies:
        lista_film += film + ","
    conn.send(lista_film.encode())

    try:
        data = conn.recv(1024).decode()
        film, numero = data.split(",")

        try:
            numero = int(numero)

            if numero <= 0:
                risposta = "Errore: numero non valido"

            elif numero > movies[film]["biglietti"]:
                risposta = "Errore: biglietti insufficienti"

            else:
                prezzo = movies[film]["prezzo"]
                totale = prezzo * numero
                sconto = 0

                if numero >= 3:
                    sconto = totale * 0.1  # 10%

                finale = totale - sconto

                risposta = f"Totale: {totale}€ | Sconto: {sconto}€ | Da pagare: {finale}€"

                # Aggiorno disponibilità
                movies[film]["biglietti"] -= numero

        except:
            risposta = "Errore: inserisci un numero valido"

        conn.send(risposta.encode())

    except:
        print("Errore comunicazione")

    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)
    print("Server cinema avviato...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=gestione_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
