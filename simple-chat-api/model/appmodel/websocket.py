from fastapi import WebSocket
from pydantic import BaseModel


class Connection(BaseModel):
    websocket: WebSocket
    room_id: str
    user_id: str

    class Config:
        arbitrary_types_allowed = True
