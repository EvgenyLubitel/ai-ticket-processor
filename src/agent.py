from models import TicketInput, TicketOutput, TicketStatus
from classifier import TicketClassifier
from summarizer import TicketSummarizer
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TicketProcessor:
    def __init__(self):
        self.classifier = TicketClassifier()
        self.summarizer = TicketSummarizer()
        self.history = []

    def process(self, ticket_input: TicketInput) -> TicketOutput:
        """Основной метод обработки обращения"""
        
        print(f"📨 Обработка: {ticket_input.text[:50]}...")
        
        # 1. Классификация
        print("🔍 Классификация...")
        classification = self.classifier.classify(ticket_input.text)
        
        # 2. Суммаризация
        print("📝 Суммаризация...")
        summary = self.summarizer.summarize(ticket_input.text)
        
        # 3. Структурированный вывод
        structured = {
            "user_id": ticket_input.user_id,
            "source": ticket_input.source,
            "type": classification.type.value,
            "summary": summary.summary,
            "key_points": summary.key_points,
            "sentiment": summary.sentiment,
            "confidence": classification.confidence
        }
        
        # 4. Финальный результат
        output = TicketOutput(
            original_text=ticket_input.text,
            classification=classification,
            summary=summary,
            structured=structured,
            processed_at=datetime.now(),
            status=TicketStatus.COMPLETED
        )
        
        # 5. Сохраняем историю
        self.history.append(output)
        
        return output

    def save_history(self, path: str = "data/tickets.json"):
        """Сохраняет историю в JSON"""
        os.makedirs("data", exist_ok=True)
        
        data = []
        for ticket in self.history:
            data.append({
                "original_text": ticket.original_text,
                "type": ticket.classification.type.value,
                "confidence": ticket.classification.confidence,
                "summary": ticket.summary.summary,
                "key_points": ticket.summary.key_points,
                "sentiment": ticket.summary.sentiment,
                "processed_at": ticket.processed_at.isoformat()
            })
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ История сохранена в {path}")