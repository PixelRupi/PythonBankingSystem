import asyncio
import pymysql


# uwierzytelnianie danych uzytkownika
def authenticate_user(cursor, login, password, pin):
    query = """
        SELECT uuid_client FROM credentials
        WHERE login=%s AND password=%s AND pin=%s
    """
    cursor.execute(query, (login, password, pin))
    result = cursor.fetchone()
    if result:
        return result[0]  # uuid_client
    return None




# główna "maszyna" do operacji bankowych, ale juz nie uzywana
"""
def bankingOperations(ip, operation):
    print(f"{ip}: {operation}")
    if operation == "test1":
        return "test 1 ok"
    elif operation == "test2":
        return "test 2 ok"
    else:
        return "unknown"
"""

# sieciowe rzeczy
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='PythonBank' ##<--- zmienic dostep do bazy
)

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')[0]
    cursor = db.cursor()
    uuid = None

    while True:
        request = (await reader.read(255)).decode('utf8').strip()
        if not request:
            continue
        if request == 'quit':
            break

        parts = request.split()
        command = parts[0]


        ## logowanie
        if command == 'login' and len(parts) == 4:
            login, password, pin = parts[1], parts[2], parts[3]
            uuid_client = authenticate_user(cursor, login, password, pin)
            if uuid_client:
                uuid = uuid_client
                response = f"Zalogowano pomyślnie. UUID: {uuid}"
            else:
                response = "Błędne dane logowania"
        elif not uuid:
            response = "Najpierw się zaloguj (użyj komendy: login <login> <haslo> <pin>)"
        
        #stan konta
        elif command == 'balance' or command == 'bal':
            cursor.execute("SELECT funds, max_amount FROM funds WHERE uuid=%s", (uuid))
            result = cursor.fetchone()
            if result:
                funds, max_amount = result
                response = f"Twoje środki: {funds}, Limit: {max_amount}"
            else:
                response = "Nie znaleziono danych konta."

        writer.write(response.encode('utf8'))
        await writer.drain()

    writer.close()
    await writer.wait_closed()


# main
async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 15555)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())
