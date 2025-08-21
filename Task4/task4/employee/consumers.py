import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from asgiref.sync import sync_to_async
from datetime import datetime
from pymongo import MongoClient

# MongoDB client singleton
_mongo_client = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGO_URL)
    return _mongo_client

@sync_to_async
def save_message_to_mongo(doc):
    client = get_mongo_client()
    db = client[settings.MONGO_DB_NAME]
    coll = db[settings.MONGO_COLLECTION]
    coll.insert_one(doc)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.department_id = str(self.scope['url_route']['kwargs']['department_id'])
        self.group_name = f"dept_{self.department_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        data = json.loads(text_data)
        sender = data.get("sender", "unknown")
        message = data.get("message", "")
        timestamp = datetime.utcnow().isoformat() + "Z"

        payload = {
            "group_name": self.department_id,
            "sender": sender,
            "message": message,
            "timestamp": timestamp,
        }

        # Save to MongoDB
        await save_message_to_mongo(payload)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "payload": payload,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["payload"]))
