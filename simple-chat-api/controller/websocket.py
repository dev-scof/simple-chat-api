from typing import List, Dict
from collections import defaultdict
from model.appmodel.websocket import Connection


class ConnectionManager:
    def __init__(self):
        self.connection_dict: Dict[str, List[Connection]] = defaultdict(list)

    async def connect(self, conn: Connection):
        await conn.websocket.accept()
        self.connection_dict[conn.room_id].append(conn)

    def disconnect(self, conn: Connection):
        self.connection_dict[conn.room_id].remove(conn)

    async def send_personal_message(
        self,
        message: dict,
        conn: Connection
    ):
        await conn.websocket.send_json(message)

    async def multicast(self, message: dict, room_id: str):
        """Broadcast to specific room"""
        for conn in self.connection_dict[room_id]:
            await conn.websocket.send_json(message)

    async def broadcast(self, message: dict):
        """All broadcast"""
        for room in self.connection_dict:
            for conn in self.connection_dict[room]:
                await conn.websocket.send_json(message)
