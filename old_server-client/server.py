import sys
import threading
import socket

#print("argumenty: ", sys.argv[1])















'''
HOST = '0.0.0.0'
PORT = 12000

def handle_communication(client_socket, address):
    print("Connected to: ")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[{address}] recv: {data}")
            client_socket.send(f"RECV: {data}".encode())
        except ConnectionResetError:
            break
    print(f"CONNECTON TERMINATED WITH {address}")
    client_socket.close()
    

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen(2)


while True:
    client_socket, addr = SERVER.accept()
    client_thread = threading.Thread(target=handle_communication, args=(client_socket, addr))
    client_thread.start()'
    '
'''