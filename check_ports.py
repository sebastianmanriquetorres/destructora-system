import socket

ports = [8000, 8001]
for port in ports:
    sock = socket.socket()
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    status = "ACTIVO" if result == 0 else "INACTIVO"
    print(f"Puerto {port}: {status}")