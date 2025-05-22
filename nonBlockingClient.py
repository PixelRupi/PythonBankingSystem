import socket
import hashlib
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 5005))
request = None
session_token = None

try:
    while request != 'quit':
        request = input('>> ').strip()
        clear_screen()
        if not request:
            continue

        if request == "help":
            print("""
Dostępne komendy:
  login <login> <haslo> <pin>   - Zaloguj się
  balance                       - Sprawdź stan konta
  history                       - Historia transakcji
  transfer <uuid_to> <kwota>   - Przelew
  logout                        - Wyloguj się
  quit                          - Zamknij
""")
            continue

        # logowanie
        if request.startswith("login") and session_token is None:
            parts = request.split()
            if len(parts) != 4:
                print("Użycie: login <login> <haslo> <pin>")
                continue
            login, raw_password, pin = parts[1], parts[2], parts[3]
            hashed_password = sha256_hash(raw_password)
            login_request = f"login {login} {hashed_password} {pin}"
            server.send(login_request.encode('utf8'))
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
                session_token = None
                server.close()
                break
            else:
                full_request = f"token {session_token} {request}"
                server.send(full_request.encode('utf8'))
                response = server.recv(4096).decode('utf8')
                print(response)
        else:
            print("Najpierw się zaloguj (login <login> <haslo> <pin>).")
except KeyboardInterrupt:
    print("\nZamykam połączenie.")
finally:
    server.close()
