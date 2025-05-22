
import socket
import hashlib
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 5005))
session_token = None

print("=== BANKOMAT ===")

try:
    while True:
        if not session_token:
            print("Zaloguj się: login <login> <haslo> <pin>")
        cmd = input("ATM >> ").strip()
        clear_screen()

        if cmd == "help":
            print("""
Dostępne komendy:
  login <login> <haslo> <pin>   - Zaloguj się
  history                       - Pokaż historię transakcji
  withdraw <kwota>             - Wypłać środki
  deposit <kwota>              - Wpłać środki
  logout                       - Wyloguj się
  quit                         - Wyjście
""")
            continue

        if cmd == 'quit':
            break

        if cmd.startswith("login") and session_token is None:
            parts = cmd.split()
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
                session_token = response.split("TOKEN ")[1].strip()
        elif session_token:
            if cmd == 'logout':
                server.send(f"token {session_token} logout".encode('utf8'))
                response = server.recv(1024).decode('utf8')
                print(response)
                session_token = None
                server.close()
                break
            elif cmd.startswith('withdraw') or cmd.startswith('deposit') or cmd == 'history':
                server.send(f"token {session_token} {cmd}".encode('utf8'))
                response = server.recv(4096).decode('utf8')
                print(response)
            else:
                print("Nieznana komenda. Użyj 'help'.")
        else:
            print("Najpierw się zaloguj.")
except KeyboardInterrupt:
    print("\nZamykam połączenie.")
finally:
    server.close()
