from transformers import pipeline
from huggingface_hub import login


login("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")# Токен

# Завантажуємо модель аналізу тону
classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")


def is_neutral(text):
    print("[DEBUG] Емоційний-аналіз")
    result = classifier(text)[0]  # Аналізуємо текст
    label = result["label"]

    # Перевірка на нейтральний тон
    if label.lower() == "neutral":
        print("[DEBUG] Результат: True")
        return True
    print("[DEBUG] Результат: False")
    return False


"""# Приклад використання
text = "Цей текст не містить емоційного забарвлення."
print(is_neutral(text))  # True або False
"""