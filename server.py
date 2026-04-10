import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clients = []
usernames = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

def handle_client(client):
    try:
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)

        print(f"{username} connected.")

        broadcast(f"{username} joined the chat.\n".encode())

        while True:
            message = client.recv(1024)
            if not message:
                break

            full_message = f"{username}: {message.decode()}"
            print(full_message.strip())

            broadcast(full_message.encode(), client)

    except:
        pass
    finally:
        remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]

        clients.remove(client)
        usernames.remove(username)

        print(f"{username} disconnected.")
        broadcast(f"{username} left the chat.\n".encode())

        client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on port {PORT}...")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
