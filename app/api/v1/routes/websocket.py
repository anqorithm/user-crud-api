"""
WebSocket Endpoints
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logging import log

router = APIRouter(tags=["WebSocket"])


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket, user_id: str):
        await ws.accept()
        self.active[user_id] = ws

    def disconnect(self, user_id: str):
        if user_id in self.active:
            del self.active[user_id]

    async def send(self, msg: dict, user_id: str):
        if user_id in self.active:
            await self.active[user_id].send_json(msg)

    async def broadcast(self, msg: dict):
        for ws in self.active.values():
            await ws.send_json(msg)


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def ws_endpoint(ws: WebSocket, user_id: str):
    await manager.connect(ws, user_id)
    try:
        while True:
            data = await ws.receive_json()
            if data.get("type") == "ping":
                await manager.send({"type": "pong"}, user_id)
            elif data.get("type") == "broadcast":
                await manager.broadcast({**data, "from": user_id})
            else:
                await manager.send({"type": "echo", "data": data}, user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)


@router.websocket("/ws")
async def ws_anonymous(ws: WebSocket):
    await ws.accept()
    user_id = str(id(ws))
    manager.active[user_id] = ws
    try:
        while True:
            data = await ws.receive_json()
            await ws.send_json({"type": "echo", "data": data})
    except WebSocketDisconnect:
        if user_id in manager.active:
            del manager.active[user_id]