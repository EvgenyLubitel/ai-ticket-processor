import json
import os
import httpx
from models import SummarizedTicket

class TicketSummarizer:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("AITUNEL_API_KEY")
        self.base_url = os.getenv("AITUNEL_BASE_URL", "https://api.aitunel.com/v1")
        
        if not self.api_key:
            print("⚠️ ВНИМАНИЕ: AITUNEL_API_KEY не найден в .env")
            print("📌 Суммаризация будет работать в демо-режиме с мок-данными")

    def summarize(self, text: str) -> SummarizedTicket:
        """Суммаризирует обращение"""
        
        if not self.api_key:
            return self._mock_summarize(text)
        
        system_prompt = """
        Ты — AI-агент для суммаризации обращений.

        Задача:
        1. Напиши краткое изложение обращения (1-2 предложения)
        2. Выдели ключевые пункты (3-5 пунктов)
        3. Определи тональность: positive, negative, neutral

        Верни JSON:
        {
            "summary": "краткое изложение",
            "key_points": ["пункт 1", "пункт 2", "пункт 3"],
            "sentiment": "negative"
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
                    "temperature": 0.3,
                    "response_format": {"type": "json_object"},
                    "max_tokens": 500
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                return self._mock_summarize(text)
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            data = json.loads(content)
            
            return SummarizedTicket(
                summary=data["summary"],
                key_points=data["key_points"],
                sentiment=data["sentiment"]
            )
            
        except Exception as e:
            print(f"⚠️ Ошибка суммаризации: {e}")
            return self._mock_summarize(text)
    
    def _mock_summarize(self, text: str) -> SummarizedTicket:
        """Демо-режим суммаризации без API"""
        # Простая имитация
        summary = text[:100] + "..."
        key_points = [f"Пункт {i+1}: {text[i*20:(i+1)*20]}..." for i in range(min(3, len(text)//20 + 1))]
        
        # Определяем тональность
        if "жалоб" in text or "не работает" in text or "ошибк" in text:
            sentiment = "negative"
        elif "спасиб" in text or "отличн" in text:
            sentiment = "positive"
        else:
            sentiment = "neutral"
        
        return SummarizedTicket(
            summary=summary,
            key_points=key_points[:3],
            sentiment=sentiment
        )