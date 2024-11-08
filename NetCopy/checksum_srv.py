import socket
import threading
import time

checksums = {}

def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data:
                break

            parts = data.split('|')
            if parts[0] == 'BE':
                file_id, validity, length, checksum = parts[1], int(parts[2]), int(parts[3]), parts[4]
                checksums[file_id] = (time.time() + validity, length, checksum)
                conn.sendall(b'OK\n')
            elif parts[0] == 'KI':
                file_id = parts[1]
                if file_id in checksums:
                    expiry, length, checksum = checksums[file_id]
                    if time.time() < expiry:
                        conn.sendall(f"{length}|{checksum}\n".encode('utf-8'))
                    else:
                        del checksums[file_id]
                        conn.sendall(b"0|\n")
                else:
                    conn.sendall(b"0|\n")
    finally:
        conn.close()

def main(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, int(port)))
    server.listen()
    print(f"Checksum server running on {ip}:{port}")
    
    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])
