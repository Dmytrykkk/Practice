import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urlparse, urljoin

def get_news_details(url):
    # Отримуємо HTML-код сторінки
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Витягуємо домен з URL
    portal_name = urlparse(url).netloc

    # Парсимо статтю
    article = Article(url)
    article.download()
    article.parse()

    # Заголовок
    title = article.title

    # Основний текст статті у вигляді масиву абзаців
    text_paragraphs = article.text.split("\n")
    text_paragraphs = [para.strip() for para in text_paragraphs if para.strip()]  # Очищаємо абзаци

    # Пошук блоку основного тексту
    article_body = soup.find("article") or soup.find("div", {"class": "post-content"}) or soup.find("div", {"class": "content"}) or soup

    # Пошук першого зовнішнього посилання в основному тексті
    source = "Не знайдено"
    for link in article_body.find_all("a", href=True):
        link_url = urljoin(url, link["href"])  # Обробка відносних URL
        parsed_link = urlparse(link_url)

        # Фільтруємо внутрішні посилання та соцмережі
        if parsed_link.netloc and parsed_link.netloc != portal_name and not any(s in parsed_link.netloc for s in ["t.me", "facebook.com", "twitter.com"]):
            source = link_url  # Беремо перше знайдене зовнішнє посилання
            break

    return {
        "portal": portal_name,
        "source": source,
        "title": title,
        "text": text_paragraphs  # Повертаємо текст у вигляді масиву абзаців
    }

"""# Тест
url = "https://website-categorization.whoisxmlapi.com/api"  
news = get_news_details(url)

print(f"🔹 Портал: {news['portal']}")
print(f"🔹 Джерело: {news['source']}")
print(f"🔹 Заголовок: {news['title']}")
print("🔹 Текст:")
for paragraph in news['text']:
    print(paragraph)
"""