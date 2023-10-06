# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Conversation


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # get the room name to be the query strings conversation_id
        print(self.scope["query_string"].decode("utf-8"))
        self.room_name = self.scope["query_string"].decode("utf-8").split("=")[1]
        self.conversation_id = self.room_name
        self.room_group_name = f"chat_{self.room_name}"

        # make sure user is logged in
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return
        else:
            print(f"User {self.scope['user']} connected to chat room {self.room_name}")

        self.conversation = await Conversation.objects.filter(id=self.conversation_id, user=self.user).afirst()
        if self.conversation is None:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send existing messages
        async for message in self.conversation.messages.all():
            data = {"message": message.text, "role": message.role, "type": "chat.message"}
            await self.channel_layer.group_send(self.room_group_name, data)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"].strip()
        print("Received message: ", message)

        # Save message to database
        new_message = await self.conversation.messages.acreate(text=message, role="user")
        new_message.asave()
        # Send message to room group

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": new_message.text, "role": new_message.role}
        )
        await self.process_message()

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        role = event["role"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "role": role}))

    async def process_message(self):
        # get the assistant response
        last_message = await self.conversation.messages.all().order_by("-created_at").afirst()
        bot_response = "You Said: " + last_message.text
        # Save bot message
        bot_message = await self.conversation.messages.acreate(text=bot_response, role="assistant")
        bot_message.asave()

        data = {"message": bot_message.text, "role": bot_message.role, "type": "chat.message"}
        await self.channel_layer.group_send(self.room_group_name, data)
