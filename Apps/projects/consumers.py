import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Aceptar siempre la conexión (invitados incluidos)"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'project_{self.room_id}'

        # Unirse al grupo Redis
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Avisar a los demás que entró un invitado
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_joined",
                "user_name": f"Invitado-{self.channel_name[-5:]}"
            }
        )

    async def disconnect(self, close_code):
        """Salir del grupo"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_left",
                "user_name": f"Invitado-{self.channel_name[-5:]}"
            }
        )

    async def receive(self, text_data):
        """Recibir mensajes de un cliente y reenviar al grupo"""
        try:
            data = json.loads(text_data)
            event_type = data.get("type")

            if event_type == "diagram_update":
                # Broadcast de actualización de diagrama
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "diagram_updated",
                        "diagram_data": data.get("diagram_data", {}),
                        "user_name": f"Invitado-{self.channel_name[-5:]}"
                    }
                )
            elif event_type == "chat_message":
                # Broadcast de chat
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message_broadcast",
                        "message": data.get("message", ""),
                        "user_name": f"Invitado-{self.channel_name[-5:]}"
                    }
                )
            elif event_type == "ping":
                await self.send_json({"type": "pong"})
            else:
                await self.send_json({
                    "type": "error",
                    "message": f"Evento no soportado: {event_type}"
                })

        except Exception as e:
            await self.send_json({
                "type": "error",
                "message": str(e)
            })

    # Handlers de eventos broadcast
    async def handle_diagram_update(self, data):
        """Reenvía a todos la actualización de diagrama tal como viene"""
        diagram_data = data.get("diagram_data", {})

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "diagram_updated",
                "diagram_data": diagram_data,
                "user_name": f"Invitado-{self.channel_name[-5:]}"
            }
        )

    async def diagram_updated(self, event):
        await self.send_json({
            "type": "diagram_updated",
            "diagram_data": event["diagram_data"],
            "updated_by": event["user_name"]
        })
    
    
    
    async def user_joined(self, event):
        await self.send_json({
            "type": "user_joined",
            "user_name": event["user_name"]
        })

    async def user_left(self, event):
        await self.send_json({
            "type": "user_left",
            "user_name": event["user_name"]
        })

    async def diagram_updated(self, event):
        await self.send_json({
            "type": "diagram_updated",
            "diagram_data": event["diagram_data"],
            "updated_by": event["user_name"]
        })

    async def chat_message_broadcast(self, event):
        await self.send_json({
            "type": "chat_message",
            "message": event["message"],
            "user_name": event["user_name"]
        })

    async def send_json(self, data):
        """Enviar JSON al cliente"""
        await self.send(text_data=json.dumps(data))
