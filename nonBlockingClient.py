import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 5005))
request = None
session_token = None

try:
    while request != 'quit':
        request = input('>> ').strip()
        if not request:
            continue

        # logowanie
        if request.startswith("login") and session_token is None:
            server.send(request.encode('utf8'))
            response = server.recv(1024).decode('utf8')
            print(response)
            if response.startswith("Zalogowano"):
                try:
                    session_token = response.split("TOKEN ")[1].strip()
                except IndexError:
                    print("Nie udało się uzyskać tokenu.")
        elif session_token:
            if request.strip() == 'logout':
                full_request = f"token {session_token} logout"
                server.send(full_request.encode('utf8'))
                response = server.recv(1024).decode('utf8')
                print(response)
                session_token = None  # usuniecie tokenu z pamieci
            else:
                # automatyczne dolaczanie tokenu
                full_request = f"token {session_token} {request}"
                server.send(full_request.encode('utf8'))
                response = server.recv(1024).decode('utf8')
            print(response)
        else:
            print("Najpierw się zaloguj (login <login> <haslo> <pin>).")
except KeyboardInterrupt:
    print("\nZamykam połączenie.")
finally:
    server.close()
