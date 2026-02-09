import socket

def centralInstance(conn, addr):
    messageContainer = ""
    messages = []
    breakCondition = False
    print(f"Connessione stabilita con {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        messageContainer += data.decode()
        while '.' in messageContainer:
            message, messageContainer = messageContainer.split(".", 1)
            messages.append(message)
            if message == 'fine':
                breakCondition = True
        if breakCondition:
            break

    dates = []
    temps = []
    for message in messages:
        if message == "fine":
            continue
        giorno, temp12, temp24 = message.split("|")
        dates.append(giorno)
        temps.append(int(temp12))
        temps.append(int(temp24))

    media, tempMin, tempMax = round(sum(temps) / len(temps)), min(temps), max(temps)
    response = f"{media}|{tempMin}|{tempMax}"
    conn.sendall(response.encode())
    conn.close()
    print(f"Connessione terminata con {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("Server in ascolto sulla porta 12345...")

    conn, addr = server_socket.accept()
    centralInstance(conn, addr)

if __name__ == "__main__":
    start_server()