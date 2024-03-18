import socket

# Define host and port
HOST = '192.168.86.35'
PORT = 8000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print(f"Server is listening on {HOST}:{PORT}")


def handle_client_response(client_socket):
    # Receive data from the client
    data = client_socket.recv(1024)

    if not data:
        return

    # Decode received data and print it
    print(f"Received data: {data.decode('utf-8')}")

    # Send a response to the client
    response = "HTTP/1.1 200 OK\n\nHello, World! This is your server running at " + "localhost" + ":" + str(PORT)
    client_socket.sendall(response.encode('utf-8'))

    # Close the connection with the client
    client_socket.close()


while True:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Handle client response
    handle_client_response(client_socket)

# Close the server socket
server_socket.close()
