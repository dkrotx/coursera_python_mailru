import socket

def handle_connection(conn: socket.socket):
    conn.settimeout(5)
    while True:
        try:
            s = conn.recv(1024)
            if not s:
                break
            print("received {} bytes ('{}')".format(len(s), s.decode('utf-8')))
        except socket.timeout as te:
            print("Error: timed out ({})".format(te))
            break

    print('Finishing work with {}'.format(conn))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.bind(("127.0.0.1", 10000))
    srv.listen(socket.SOMAXCONN)

    print("Listening...")

    conn, addr = srv.accept()
    with conn:
        handle_connection(conn)