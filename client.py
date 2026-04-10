import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            print("Disconnected from server.")
            break

def main():
    username = input("Enter your name: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send(username.encode())

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        client.send(msg.encode())

    client.close()

if __name__ == "__main__":
    main()
