import socket

class Network:
    def __init__(self, server_ip, port=5555):
        # Initialize the network client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Store the server IP and port
        self.server_ip = server_ip
        self.port = port

        # Create a tuple containing the server address
        self.addr = (self.server_ip, self.port)

        # Connect to the server and get the assigned ID
        self.id = self.connect()
        if self.id is not None:
            print("Connected with ID:", self.id)
        else:
            print("Failed to connect to the server.")

    def connect(self):
        try:
            # Attempt to connect to the server
            self.client.connect(self.addr)

            # Receive and decode the ID assigned by the server
            return self.client.recv(2048).decode()
        except ConnectionRefusedError:
            # Connection was refused by the server
            print("Connection to the server failed.")
            return None

    def send(self, data):
        try:
            # Send the data to the server
            self.client.sendall(str.encode(data))

            # Receive and decode the response from the server
            return self.client.recv(2048).decode()
        except (socket.error, AttributeError) as e:
            # Handling socket errors and attribute errors
            print("Sending data failed:", e)
            return None

n = Network("192.168.196.234", 5555)
response = n.send("balls")
print(response)