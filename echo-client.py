import socket

# Setting up the HOST IP address and the PORT number
HOST = "127.0.0.1"
PORT = 65432

# Establishing a connection to the server using a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connecting to the server with specified host and port
    s.connect((HOST, PORT))
    # Sending 'hello, world!' as a byte-encoded message to the server
    s.sendall(b"hello, world!")
    # Receiving data from the server, up to a maximum of 1024 bytes
    data = s.recv(1024)

print(f"Received {data!r}")
