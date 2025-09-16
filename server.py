import os
import asyncio
import websockets

connected = set()

async def relay(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            # broadcast minden kliensnek (mindenki más kapja)
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        connected.remove(websocket)

PORT = int(os.environ.get("PORT", 8080))
start_server = websockets.serve(relay, "0.0.0.0", PORT)

print(f"Relay szerver elindult a {PORT} porton...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
