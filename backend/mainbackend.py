from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .brain import think
from .brain import speak_async, log_memory
from .voice import listen_until_silence  # <-- Import speech recognition

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/api/ping")
async def ping():
    return {"status": "ok", "message": "JARVIS backend is running!"}

class ChatRequest(BaseModel):
    message: str
    agent: str = "gpt-3.5-turbo"

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
    response = think(req.message, model=req.agent)
    # TTS and memory logging in the background
    background_tasks.add_task(speak_async, response)
    background_tasks.add_task(log_memory, f"User: {req.message}\nJARVIS: {response}")
    return {"response": response}

# --- NEW: Speech recognition endpoint ---
@app.post("/api/listen")
async def listen_endpoint():
    """
    Starts listening for a voice command and returns the recognized text.
    """
    recognized = listen_until_silence()
    return {"recognized": recognized}