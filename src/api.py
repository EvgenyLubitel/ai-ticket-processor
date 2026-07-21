from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles  # 🆕
from fastapi.responses import FileResponse    # 🆕
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Добавляем путь к src, чтобы импорты работали
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import TicketProcessor
from models import TicketInput

app = FastAPI(
    title="AI-агент для обработки обращений",
    description="Классификация и суммаризация текстовых обращений",
    version="1.0.0"
)

# 🆕 Монтируем папку static для обслуживания статичных файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🆕 Корневой маршрут для веб-интерфейса
@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

processor = TicketProcessor()

class ProcessRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class ProcessResponse(BaseModel):
    success: bool
    result: dict
    error: Optional[str] = None

# ... остальные эндпоинты (/health, /process) остаются без изменений ...
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/process", response_model=ProcessResponse)
def process(request: ProcessRequest):
    try:
        ticket_input = TicketInput(
            text=request.text,
            user_id=request.user_id or "api",
            source="api"
        )
        result = processor.process(ticket_input)
        return ProcessResponse(
            success=True,
            result=result.structured
        )
    except Exception as e:
        return ProcessResponse(
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)