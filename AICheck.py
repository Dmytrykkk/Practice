import requests

API_URL = "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
HEADERS = {"Authorization": "Bearer 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"}

def check_ai_generated(text):
    print("[DEBUG] AI-аналіз")
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    if isinstance(result, list) and isinstance(result[0], list):
        scores = {item["label"]: item["score"] for item in result[0]}
        print("[DEBUG] Результат: False")
        return scores.get("Fake", 0) > 0.75
    else:
        print("[DEBUG] Результат: True")
        return None
"""# Приклад
text = "Цей текст було написано людиною."
is_ai_generated = check_ai_generated(text)
print("Чи є текст AI-згенерований:", is_ai_generated)
"""