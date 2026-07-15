from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime

class TicketType(str, Enum):
    """Типы обращений"""
    COMPLAINT = "complaint"           # Жалоба
    REQUEST = "request"               # Запрос
    QUESTION = "question"             # Вопрос
    FEEDBACK = "feedback"             # Обратная связь
    TECHNICAL = "technical"           # Техническая проблема
    OTHER = "other"                   # Другое

class TicketStatus(str, Enum):
    """Статус обработки"""
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class TicketInput(BaseModel):
    """Входные данные"""
    text: str
    user_id: Optional[str] = None
    source: Optional[str] = "api"

class ClassifiedTicket(BaseModel):
    """Результат классификации"""
    type: TicketType
    confidence: float
    reason: str

class SummarizedTicket(BaseModel):
    """Результат суммаризации"""
    summary: str
    key_points: List[str]
    sentiment: str  # positive, negative, neutral

class TicketOutput(BaseModel):
    """Финальный выход"""
    original_text: str
    classification: ClassifiedTicket
    summary: SummarizedTicket
    structured: dict
    processed_at: datetime
    status: TicketStatus