import socket






















'''
SERVER = '127.0.0.1'
PORT = 12000

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect((SERVER, PORT))


try:
    while True:
        message = input("-> ")
        if (message.lower() == 'stop'):
            break
        CLIENT.send(message.encode())
        response = CLIENT.recv(1024).decode()
        print(f"[Olympus]: ")

finally:
    CLIENT.close()
'''