import socket
import threading

# Set the server address and port
SERVER = "192.168.196.234"
PORT = 5555

# Create a socket object using the IPv4 address family and TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the server address and port
    server_socket.bind((SERVER, PORT))
except socket.error as e:
    print(f"Error binding the socket: {str(e)}")
    exit(1)

# Listen for incoming connections (maximum 2 connections allowed in the queue)
server_socket.listen(2)
print("Waiting for a connection. Server started.")


def handle_client(client_socket):
    # Send a connection message to the client
    client_socket.send(b"Connected")

    while True:
        try:
            # Receive data from the client (up to 2048 bytes at a time)
            data = client_socket.recv(2048)
            if not data:
                # If no data is received, the client has disconnected
                print("Client disconnected.")
                break

            reply = data.decode("utf-8")
            # Print the received message and send it back to the client
            print("Received:", reply)
            print("Sending:", reply)

            client_socket.sendall(data)
        except Exception as e:
            print(f"Error handling client: {str(e)}")
            break

    client_socket.close()


while True:
    # Accept incoming connection requests and return a new socket object (client_socket) and the client's address (addr)
    client_socket, addr = server_socket.accept()
    print("Connected to:", addr)

    # Start a new thread for each client to handle multiple connections concurrently
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
