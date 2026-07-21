import json
import os
import httpx
from models import TicketType, ClassifiedTicket

class TicketClassifier:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("AITUNEL_API_KEY")
        self.base_url = os.getenv("AITUNEL_BASE_URL", "https://api.aitunel.com/v1")
        
        if not self.api_key:
            print("⚠️ ВНИМАНИЕ: AITUNEL_API_KEY не найден в .env")
            print("📌 Классификация будет работать в демо-режиме с мок-данными")

    def classify(self, text: str) -> ClassifiedTicket:
        """Классифицирует обращение по типу"""
        
        # Проверяем наличие API ключа
        if not self.api_key:
            return self._mock_classify(text)
        
        system_prompt = """
        Ты — классификатор обращений. Определи тип запроса.
        
        Типы:
        - complaint: жалоба на качество, сервис или продукт
        - request: запрос на действие (купить, заменить, настроить)
        - question: вопрос об услугах, продуктах или процессах
        - feedback: обратная связь, идеи, предложения
        - technical: технические проблемы, баги, ошибки
        - other: всё остальное
        
        Верни JSON:
        {
            "type": "тип_запроса",
            "confidence": 0.95,
            "reason": "краткое обоснование классификации"
        }
        """
        
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    "temperature": 0.1,
                    "response_format": {"type": "json_object"},
                    "max_tokens": 500
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                print(f"⚠️ Ошибка AITUNEL API: {response.status_code}")
                return self._mock_classify(text)
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            data = json.loads(content)
            
            return ClassifiedTicket(
                type=TicketType(data["type"]),
                confidence=data["confidence"],
                reason=data["reason"]
            )
            
        except Exception as e:
            print(f"⚠️ Ошибка классификации: {e}")
            return self._mock_classify(text)
    
    def _mock_classify(self, text: str) -> ClassifiedTicket:
        """Демо-режим классификации без API"""
        # Простая логика для демонстрации
        if "жалоб" in text or "не работает" in text or "ошибк" in text:
            return ClassifiedTicket(
                type=TicketType.COMPLAINT,
                confidence=0.85,
                reason="Обнаружены жалобы в тексте"
            )
        elif "вопрос" in text or "подскажите" in text or "как" in text:
            return ClassifiedTicket(
                type=TicketType.QUESTION,
                confidence=0.80,
                reason="Обнаружен вопрос в тексте"
            )
        elif "спасиб" in text or "отличн" in text:
            return ClassifiedTicket(
                type=TicketType.FEEDBACK,
                confidence=0.90,
                reason="Обнаружена положительная обратная связь"
            )
        else:
            return ClassifiedTicket(
                type=TicketType.OTHER,
                confidence=0.60,
                reason="Не удалось определить тип"
            )