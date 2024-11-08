import socket
import hashlib

def calculate_checksum(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_checksum(chsum_srv_ip, chsum_srv_port, file_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((chsum_srv_ip, int(chsum_srv_port)))
        message = f"KI|{file_id}\n"
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8').strip()
        length, checksum = response.split('|')
        return checksum if length != '0' else None

def main(srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((srv_ip, int(srv_port)))
        server.listen(1)
        conn, _ = server.accept()
        with open(file_path, 'wb') as f:
            while chunk := conn.recv(1024):
                f.write(chunk)
    
    received_checksum = calculate_checksum(file_path)
    expected_checksum = get_checksum(chsum_srv_ip, chsum_srv_port, file_id)
    
    if received_checksum == expected_checksum:
        print("CSUM OK")
    else:
        print("CSUM CORRUPTED")

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

