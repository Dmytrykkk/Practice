import requests
from googletrans import Translator

api_key = "AIzaSyD2Zua_arIYdzsVXosjkV9CSPNlKChcL-k"  # API-ключ
cse_id = "307f972032ca64e97"  # Ідентифікатор пошукової системи


def search_google(query):
    print("Пошук статтей")
    # Пошук за запитом
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"

    response = requests.get(url)
    results = []

    if response.status_code == 200:
        search_results = response.json()
        items = search_results.get("items", [])
        for item in items[:5]:
            results.append(item['link'])
    else:
        print(f"Помилка запиту: {response.status_code}")

    return results


def translate_and_search(query):
    translator = Translator()

    # Перевірка мови запиту
    detected_lang = translator.detect(query).lang
    # print(f"Detected language: {detected_lang}")

    results = []

    if detected_lang != 'en':
        # Перекладаємо на англійську
        translated_query = translator.translate(query, src=detected_lang, dest='en').text
        # print(f"Translated query: {translated_query}")

        # Пошук для перекладеного запиту
        results.extend(search_google(translated_query))

    # Пошук для оригінального запиту
    results.extend(search_google(query))

    print(results)
    return results


"""Приклад
query = "ЄС перегляне мільярдні витрати на підтримку інших країн"

results = translate_and_search(query)

print(results)
"""
