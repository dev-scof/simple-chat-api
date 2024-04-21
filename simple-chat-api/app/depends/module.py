from fastapi import Request, WebSocket
from settings import Settings
from controller.websocket import ConnectionManager


def app_settings(request: Request) -> Settings:
    """Settings Controller"""
    return request.app.settings


def websocket_connection(websocket: WebSocket) -> ConnectionManager:
    """Connection Controller"""
    return websocket.app.connection
