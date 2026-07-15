from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.agent import TicketProcessor
from src.models import TicketInput

app = FastAPI(
    title="AI-агент для обработки обращений",
    description="Классификация и суммаризация текстовых обращений",
    version="1.0.0"
)

processor = TicketProcessor()

class ProcessRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class ProcessResponse(BaseModel):
    success: bool
    result: dict
    error: Optional[str] = None

@app.get("/")
def read_root():
    return {
        "service": "AI-агент для обработки обращений",
        "status": "running",
        "endpoints": [
            "/process - POST - обработка текста",
            "/health - GET - проверка статуса",
            "/docs - GET - документация Swagger"
        ]
    }

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