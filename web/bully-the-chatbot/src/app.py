import os
import uuid
import threading
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llama_cpp import Llama

ROOT = Path(__file__).parent
MODEL_PATH = os.environ.get("MODEL_PATH", str(ROOT / "model.gguf"))
SYSTEM_PROMPT = (ROOT / "system_prompt.txt").read_text()
MAX_MESSAGES = 10  # user turns per session before forced reset

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=int(os.environ.get("LLAMA_THREADS", "4")),
    chat_format="qwen",
    verbose=False,
)
llm_lock = threading.Lock()

app = FastAPI()

# session_id -> list of {role, content}
SESSIONS: Dict[str, List[dict]] = {}
sessions_lock = threading.Lock()


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    messages_used: int
    messages_remaining: int
    session_ended: bool


def new_session() -> str:
    sid = uuid.uuid4().hex
    with sessions_lock:
        SESSIONS[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return sid


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.post("/session")
def create_session():
    return {"session_id": new_session(), "max_messages": MAX_MESSAGES}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    sid = req.session_id or new_session()

    with sessions_lock:
        history = SESSIONS.get(sid)
    if history is None:
        raise HTTPException(status_code=404, detail="Unknown session_id. Start a new session.")

    user_turns = sum(1 for m in history if m["role"] == "user")
    if user_turns >= MAX_MESSAGES:
        return ChatResponse(
            session_id=sid,
            reply="(This session has ended. Start a new session to continue.)",
            messages_used=user_turns,
            messages_remaining=0,
            session_ended=True,
        )

    history.append({"role": "user", "content": req.message})

    with llm_lock:
        result = llm.create_chat_completion(
            messages=history,
            max_tokens=256,
            temperature=0.7,
            top_p=0.9,
        )
    reply = result["choices"][0]["message"]["content"].strip()
    history.append({"role": "assistant", "content": reply})

    user_turns += 1
    remaining = MAX_MESSAGES - user_turns
    ended = remaining <= 0

    if ended:
        # purge to free memory; client must call /session again
        with sessions_lock:
            SESSIONS.pop(sid, None)

    return ChatResponse(
        session_id=sid,
        reply=reply,
        messages_used=user_turns,
        messages_remaining=remaining,
        session_ended=ended,
    )


app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")
