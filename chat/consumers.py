from channels.consumer import AsyncConsumer
import json
class chatconsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        # responding after connection
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        receive_data = json.loads(event["text"])
        msg = receive_data.get("message")
        if not msg:
            return False
        response = {
            "message":msg
        }
        await self.send({
            "type": 'websocket.send',
            "text": json.dumps(response)
        })
    async def websocket_disconnect(self, event):
        print("disconnect", event)
    