import socket
import hashlib

def calculate_checksum(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def send_checksum(chsum_srv_ip, chsum_srv_port, file_id, checksum):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((chsum_srv_ip, int(chsum_srv_port)))
        message = f"BE|{file_id}|60|{len(checksum)}|{checksum}\n"
        sock.sendall(message.encode('utf-8'))
        sock.recv(1024)  # Expect "OK"

def main(srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, file_path):
    checksum = calculate_checksum(file_path)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((srv_ip, int(srv_port)))
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                sock.sendall(chunk)

    send_checksum(chsum_srv_ip, chsum_srv_port, file_id, checksum)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
