import category
import extract
import AICheck
import emotion
import comparison
import search


def verify_news(url):
    grade = 0

    # 1. Перевіряємо, чи посилання є новиною
    if not category.is_news(url):
        print("Це не новина.")
        return

    # 2. Витягуємо текст новини
    news_details = extract.get_news_details(url)
    news_text = " ".join(news_details["text"])

    # 3. Знаходимо першоджерело
    source_url = news_details["source"]
    if source_url == "Не знайдено":
        source_url = None

    if source_url:
        grade += 2

    # 4. Перевіряємо на слід ШІ
    if not AICheck.check_ai_generated(news_text):
        grade += 4

    # 5. Перевіряємо на нейтральний тон
    if emotion.is_neutral(news_text):
        grade += 4

    # 6. Порівнюємо текст із першоджерелом
    if source_url:
        source_details = extract.get_news_details(source_url)
        source_text = " ".join(source_details["text"])
        similarity = comparison.compare_texts(news_text, source_text)
        if similarity > 0.7:
            grade += 2

    # 7. Шукаємо схожі новини
    similar_news_urls = search.translate_and_search(news_details["title"])

    # 8. Перевіряємо збіги серед знайдених новин
    found_match = False
    for similar_url in similar_news_urls:
        similar_details = extract.get_news_details(similar_url)
        similar_text = " ".join(similar_details["text"])
        similarity = comparison.compare_texts(news_text, similar_text)
        if similarity > 0.8:
            grade += 2
            found_match = True
            break

    # 9. Визначаємо рейтинг
    rating = grade / 16 * 100
    print(f"Ймовірність, що новина не фейк - {rating}%")


# Виклик функції з введеним посиланням
url = input("Введіть посилання: ")
verify_news(url)
