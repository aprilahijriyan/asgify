import json
from datetime import datetime

from asgify.app import Asgify
from asgify.context import WebSocketContext
from asgify.errors import ClientDisconnected


async def websocket_handler(ctx: WebSocketContext):
    await ctx.accept()
    await ctx.send_bytes("Welcome to asgify 🚀".encode())
    while True:
        try:
            data = await ctx.receive_text()
            print("<", data)
            reply = json.dumps({"echo": data, "timestamp": datetime.now().isoformat()})
            await ctx.send_text(reply)
            print(">", reply)
        except ClientDisconnected:
            print("disconnected with client")
            break


app = Asgify(websocket=websocket_handler)
