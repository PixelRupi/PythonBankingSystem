import asyncio


def bankingOperations(operation):
    print(f"operacja: {operation}")
    if operation == "test1":
        return True
    elif operation == "test2":
        return False
    else:
        pass

async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        response = str("aaaaaa")
        #print(str(request) + '\n')
        ###
        if(bankingOperations(request)):
            response = "test 1 poprawny"
        else:
            response = "test 2 poprawny"

        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 15555)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())