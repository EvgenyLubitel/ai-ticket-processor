import sys
import os
import json
import argparse

# Добавляем корневую папку в путь поиска
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Теперь импорты работают
from src.agent import TicketProcessor
from src.models import TicketInput

def demo():
    """Демонстрация работы агента"""
    
    print("=" * 60)
    print("🤖 AI-агент для обработки обращений")
    print("=" * 60 + "\n")
    
    tickets = [
        "У меня не работает приложение, постоянно вылетает при открытии заказов. "
        "Уже третий раз за день! Очень раздражает, срочно почините!",
        
        "Здравствуйте! Подскажите, пожалуйста, как подключить корпоративный тариф "
        "для 10 сотрудников? И сколько это будет стоить?",
        
        "Спасибо за отличный сервис! Операторы очень вежливые и все объяснили "
        "понятно. Отличная работа!",
        
        "Вчера заказывали доставку, привезли не тот товар и в поврежденной упаковке. "
        "Ждем замену и компенсацию."
    ]
    
    processor = TicketProcessor()
    
    for i, text in enumerate(tickets, 1):
        print(f"\n{'='*60}")
        print(f"📝 Обращение #{i}")
        print(f"{'='*60}")
        
        ticket_input = TicketInput(
            text=text,
            user_id=f"user_{i}",
            source="demo"
        )
        
        result = processor.process(ticket_input)
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Тип: {result.classification.type.value}")
        print(f"   Уверенность: {result.classification.confidence:.2%}")
        print(f"   Тональность: {result.summary.sentiment}")
        print(f"\n   📝 Резюме: {result.summary.summary}")
        print(f"   🔑 Ключевые пункты:")
        for point in result.summary.key_points:
            print(f"      • {point}")
        
        print(f"\n   📋 Структурированный вывод:")
        print(json.dumps(result.structured, ensure_ascii=False, indent=2))
    
    processor.save_history()
    print("\n✅ Готово!")

def interactive():
    """Интерактивный режим"""
    processor = TicketProcessor()
    
    print("=" * 60)
    print("🤖 AI-агент для обработки обращений (интерактивный)")
    print("=" * 60)
    print("Введите текст обращения (для выхода введите 'exit'):\n")
    
    while True:
        text = input("📨 > ")
        
        if text.lower() in ["exit", "quit", "q"]:
            break
        
        if not text.strip():
            continue
        
        ticket_input = TicketInput(text=text, source="interactive")
        result = processor.process(ticket_input)
        
        print(f"\n📊 Результат:")
        print(f"   Тип: {result.classification.type.value}")
        print(f"   Резюме: {result.summary.summary}")
        print(f"   Ключевые пункты: {', '.join(result.summary.key_points)}")
        print(f"   Тональность: {result.summary.sentiment}")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "interactive"], default="demo")
    args = parser.parse_args()
    
    if args.mode == "interactive":
        interactive()
    else:
        demo()