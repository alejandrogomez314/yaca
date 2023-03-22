import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # Accepting incoming connections and returning a new socket object representing the connection,
    # and the address of the server (IP address and port number)
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Receiving data from the server and sending it back until there is no more data to receive
        while True:
            data = conn.recv(1024)
            # if data is empty, it means the client closed the connection, so break out the loop.
            if not data:
                break
            conn.sendall(data)
