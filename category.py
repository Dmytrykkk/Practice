import requests
from bs4 import BeautifulSoup
import re
from newspaper import Article
from datetime import datetime


def is_valid_url(url):
    """Перевіряє, чи існує сторінка (HTTP статус 200)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }
    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=5, allow_redirects=True)
        """print(f"[DEBUG] URL перевірено: {url}, статус: {response.status_code}")"""
        if response.status_code == 403:
            print("[ERROR] Доступ заборонено (403)")
        return response.status_code == 200, response
    except requests.RequestException as e:
        print(f"[ERROR] Неможливо отримати сторінку: {e}")
        return False, None


def is_news_page(response):
    """Перевіряє, чи є на сторінці HTML-елементи, характерні для новин"""
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tags = [
        soup.find("meta", {"property": "og:type", "content": "article"}),
        soup.find("meta", {"name": "news_keywords"}),
        soup.find("article")
    ]
    page_check = any(meta_tags)
    print(f"[DEBUG] HTML-аналіз сторінки: {page_check}")
    return page_check, soup

def extract_text(url):
    """Витягує основний текст статті"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        """print(f"[DEBUG] Довжина тексту: {len(article.text.split())} слів")"""
        return article.text, article.publish_date
    except Exception as e:
        print(f"[ERROR] Неможливо отримати текст статті: {e}")
        return "", None


def is_news_text(text):
    """Перевіряє довжину тексту (мінімальна довжина для новини)"""
    min_words = 100
    is_valid = len(text.split()) > min_words
    """print(f"[DEBUG] Аналіз тексту: {'+' if is_valid else '-'} (знайдено {len(text.split())} слів)")"""
    return is_valid


def extract_date(soup):
    """Шукає дату публікації в мета-тегах і тексті сторінки"""
    date_meta = soup.find("meta", {"property": "article:published_time"}) or \
                soup.find("meta", {"name": "date"}) or \
                soup.find("meta", {"itemprop": "datePublished"}) or \
                soup.find("time")
    if date_meta:
        date_content = date_meta.get("content") or date_meta.text
        try:
            date_parsed = datetime.strptime(date_content[:19], "%Y-%m-%dT%H:%M:%S")
            """print(f"[DEBUG] Дата знайдена: {date_parsed}")"""
            return date_parsed
        except ValueError:
            """print(f"[DEBUG] Формат дати не ISO, використовується оригінальне значення: {date_content}")"""
            return date_content
    """print("[DEBUG] Дата не знайдена")"""
    return None


def is_news(url):
    """Перевіряє URL на новину за допомогою всіх методів"""
    """print(f"\n Аналізуємо: {url}")"""
    page_exists, response = is_valid_url(url)
    if not page_exists:
        print("Сторінка недоступна")
        return False

    page_check, soup = is_news_page(response)
    text, article_date = extract_text(url)
    text_check = is_news_text(text)
    date_check = article_date or extract_date(soup)
    is_news_flag = (page_check or text_check)
    return is_news_flag

"""Тестовий URL
url = "https://www.bloomberg.com/news/articles/2025-02-10/eu-to-review-its-multi-billion-euro-foreign-aid-allocations"
if is_news(url):
    print("Це новина")
else:
    print("Це НЕ новина")
"""