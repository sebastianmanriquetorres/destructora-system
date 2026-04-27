import socket
import sys

def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

if check_port('127.0.0.1', 8000):
    print("Servidor corriendo en puerto 8000")
else:
    print("Servidor NO corriendo en puerto 8000")

if check_port('127.0.0.1', 8001):
    print("Servidor corriendo en puerto 8001")
else:
    print("Servidor NO corriendo en puerto 8001")