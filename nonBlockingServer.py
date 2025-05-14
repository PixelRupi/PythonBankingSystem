import asyncio
import pymysql
import uuid

# Połączenie z bazą danych
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='PythonBank'
)

# Mapa sesji: token → uuid_client
session_tokens = {}

# Uwierzytelnianie
def authenticate_user(cursor, login, password, pin):
    query = """
        SELECT uuid_client FROM credentials
        WHERE login=%s AND password=%s AND pin=%s
    """
    cursor.execute(query, (login, password, pin))
    result = cursor.fetchone()
    return result[0] if result else None

# Obsługa klienta
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')[0]
    cursor = db.cursor()

    while True:
        try:
            request = (await reader.read(1024)).decode('utf8').strip()
            if not request:
                continue
            if request == 'quit':
                break

            parts = request.split()
            command = parts[0]

            # logowanie <login> <haslo> <pin>
            if command == 'login' and len(parts) == 4:
                login, password, pin = parts[1], parts[2], parts[3]
                uuid_client = authenticate_user(cursor, login, password, pin)
                if uuid_client:
                    token = str(uuid.uuid4())
                    session_tokens[token] = uuid_client
                    response = f"Zalogowano. TOKEN {token}"
                else:
                    response = "Błędne dane logowania"

            # komendy z tokenem
            elif command == 'token' and len(parts) >= 3:
                token = parts[1]
                subcommand = parts[2]
                args = parts[3:]
                uuid_client = session_tokens.get(token)

                # wlasciwe komendy      \|/
                if not uuid_client:
                    response = "Nieprawidłowy lub wygasły token."
                else:
                    # wylogowanie
                    if subcommand == 'logout':
                        response = "Wylogowano pomyślnie."
                        session_tokens.pop(token, None)
                    # stan konta
                    if subcommand == 'balance' or subcommand == "bal":
                        cursor.execute("SELECT funds, max_amount FROM funds WHERE uuid=%s", (uuid_client,))
                        result = cursor.fetchone()
                        if result:
                            funds, max_amount = result
                            response = f"Twoje środki: {funds}, Limit: {max_amount}"
                        else:
                            response = "Nie znaleziono konta."

                    # historia
                    elif subcommand == 'history':
                        cursor.execute("""
                            SELECT uuid_from, uuid_to, operation, amount
                            FROM history
                            WHERE uuid_from = %s OR uuid_to = %s
                            ORDER BY transaction_id DESC LIMIT 10
                        """, (uuid_client, uuid_client))
                        results = cursor.fetchall()
                        if results:
                            lines = [f"{op}: {f} → {t} | {amt}" for f, t, op, amt in results]
                            response = "\n".join(lines)
                        else:
                            response = "Brak transakcji."

                    # transfer <uuid_to> <kwota>
                    elif subcommand == 'transfer' and len(args) == 2:
                        uuid_to, amount_str = args
                        try:
                            amount = float(amount_str)
                            if amount <= 0:
                                response = "Kwota musi być dodatnia."
                            else:
                                cursor.execute("SELECT 1 FROM funds WHERE uuid = %s", (uuid_to,))
                                if not cursor.fetchone():
                                    response = "Odbiorca nie istnieje."
                                else:
                                    cursor.execute("SELECT funds, max_amount FROM funds WHERE uuid = %s", (uuid_client,))
                                    row = cursor.fetchone()
                                    if not row:
                                        response = "Nie znaleziono konta."
                                    else:
                                        funds, max_amount = row
                                        if amount > (funds + max_amount):
                                            response = f"Brak środków. Dostępne: {funds + max_amount}"
                                        else:
                                            # wykonanie przelewu
                                            cursor.execute("UPDATE funds SET funds = funds - %s WHERE uuid = %s", (amount, uuid_client))
                                            cursor.execute("UPDATE funds SET funds = funds + %s WHERE uuid = %s", (amount, uuid_to))
                                            cursor.execute(
                                                "INSERT INTO history (uuid_from, uuid_to, operation, amount) VALUES (%s, %s, 'transfer', %s)",
                                                (uuid_client, uuid_to, amount)
                                            )
                                            db.commit()
                                            response = f"Przesłano {amount} zł do {uuid_to}"
                        except ValueError:
                            response = "Nieprawidłowa kwota."

                    else:
                        response = "Nieznana komenda."

            else:
                response = "Najpierw się zaloguj (login <login> <haslo> <pin>)"

            writer.write(response.encode('utf8'))
            await writer.drain()
        except Exception as e:
            writer.write(f"Błąd: {str(e)}".encode('utf8'))
            await writer.drain()

    writer.close()
    await writer.wait_closed()

# Uruchomienie serwera
async def run_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 5005)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
