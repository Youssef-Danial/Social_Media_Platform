from channels.consumer import AsyncConsumer
from database.models import notification, thread, message, particpant
from autheno.cipher_auth import get_threadbyid, get_particpantbyid, get_user, get_userbyid, is_user_auth, get_current_datetime, get_userbyid
from main.notifications import create_notification
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
@sync_to_async
def make_message(user_id, thread_id, data):
    print("in the function")
    try:
        print("in the function")
        thread_instance = get_threadbyid(thread_id)
        sender = get_userbyid(user_id)
        creation_date = get_current_datetime()
        message_type = "text"
        message_instance = message(sender = sender, thread=thread_instance, content=data, creation_date=creation_date, message_type=message_type)
        message_instance.save()
        return message_instance
    except:
        return None


class chatconsumer(AsyncConsumer):
    def __init__(self) -> None:
        super().__init__()
        self.useriid = None
        self.counter = 0

    async def websocket_connect(self, event):
        print("connected", event)
        # responding after connection
       
        chat_room = f"user_chatroom_{self.useriid}"
        chat_room = "user_chatroom_"+str(self.useriid)
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type":"websocket.accept"
        })
        
    async def websocket_receive(self, event):
        print("receive", event)
        receive_data = json.loads(event["text"])
        if self.counter == 0:
            self.useriid = receive_data.get("userid")
            self.counter = 1
        msg = receive_data.get("message")
        threadid = receive_data.get("threadid")
        userid = receive_data.get("senderid")
        await make_message(userid, threadid, msg)
       
        if not msg:
            return False
        
        # sending the message to other users in the thread direct messaging
        otheruserid = await self.get_thread_other_user(threadid, userid)
        print(otheruserid)
        other_user_chatroom = f"user_chatroom_{otheruserid}"
        #other_user_chatroom = "user_chatroom_"+str(otheruserid)
        
        response = {
            "message":msg,
            "me":userid,
            "threadiid":threadid,
        }
        # response2 = {
        #     "message":msg,
        #     "me":0,
        #     "threadiid":threadid,
        # }
        
        await self.channel_layer.group_send(
            other_user_chatroom,
            {
                "type":"chat_messagee",
                "text": json.dumps(response)
            }
        )
        # sending the message to the same user chat room
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type":"chat_message",
                "text": json.dumps(response)
            }
        )

        # await self.send({
        #     "type": 'websocket.send',
        #     "text": json.dumps(response)
        # })
    async def websocket_disconnect(self, event):
        print("disconnect", event)

    async def chat_message(self, event):
        print("chat_message", event)
        await self.send({
            "type": 'websocket.send',
            "text": event["text"]
        })
    async def chat_messagee(self, event):
        print("chat_message", event)
        await self.send({
            "type": 'websocket.send',
            "text": event["text"]
        })

    @sync_to_async
    def get_thread_other_user(self, thread_id, user_id):
        try:
            threadinstance = get_threadbyid(thread_id)
            userinstance = get_userbyid(user_id)
            particpants = particpant.objects.filter(thread=threadinstance)
            if userinstance != threadinstance.thread_creator:
                return particpants[0].user.id
            else:
                return particpants[1].user.id
        except:
            return None

