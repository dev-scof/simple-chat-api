from fastapi import Depends, WebSocket, WebSocketDisconnect, Request
from app.depends.module import websocket_connection
from controller.websocket import ConnectionManager, Connection
from . import api


@api.get('/simple_chat/room')
async def room(
    connection: ConnectionManager = Depends(websocket_connection)
):
    """Current online users"""
    online_room_info = {}
    for room in connection.connection_dict:
        online_room_info[room] = {}
        online_room_info[room]['member_len'] = len(connection.connection_dict[room])
        online_room_info[room]['members'] = [
            conn.user_id for conn in connection.connection_dict[room]
        ]
    return online_room_info


@api.websocket("/simple_chat/room/{room_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str,
    connection: ConnectionManager = Depends(websocket_connection)
):
    conn = Connection(
        websocket=websocket,
        room_id=room_id,
        user_id=user_id)

    await connection.connect(conn)
    try:
        while True:
            data = await websocket.receive_json()
            if data['type'] == 'message':
                await connection.multicast(
                    message={
                        "user_id": user_id,
                        "message": data['message'],
                        "type": "message",
                    },
                    room_id=room_id,
                )
            elif data['type'] == 'broadcast':
                await connection.broadcast(
                    message={
                        "room_id": room_id,
                        "user_id": user_id,
                        "message": data['message'],
                        "type": "broadcast",
                    },
                )
    except WebSocketDisconnect:
        connection.disconnect(conn)
        await connection.multicast(
            message={
                "user_id": user_id,
                "message": "left the room",
                "type": "system"
            },
            room_id=room_id,
        )
