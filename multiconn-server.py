
import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# Define function to wrap accepting a connection


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    # Set connection to non-blocking mode
    conn.setblocking(False)
    # Create data object to hold incoming and outgoing data
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # Register connection with selector object for read and write events
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

# Define function to service a server connection


def service_connection(key, mask):
    # Get socket object and data object from selector key
    sock = key.fileobj
    data = key.data
    # If socket is ready to read
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        # If data received, add it to outgoing data buffer
        if recv_data:
            data.outb += recv_data
        # If no data received, unregister and close socket
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    # If socket is ready to write
    if mask & selectors.EVENT_WRITE:
        # If there is outgoing data
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            # Remove sent data from outgoing data buffer
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
# Register socket with selector object for read events
sel.register(lsock, selectors.EVENT_READ, data=None)

# Enter infinite loop to handle events
try:
    while True:
        # Wait for events to occur
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                # If new connection, wrap it with accept_wrapper function
                accept_wrapper(key.fileobj)
            # If existing connection, service it with service_connection function
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
