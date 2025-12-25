from __future__ import annotations
import logging
import random
import time
from typing import Optional, List, Dict
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
from datetime import datetime

logger = logging.getLogger("krisha_parser")
logger.setLevel(logging.INFO)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
]

KZ_CITIES = [
    'Алматы', 'Алмата', 'Астана', 'Нур-Султан', 'Шымкент', 'Караганда', 
    'Актобе', 'Тараз', 'Павлодар', 'Усть-Каменогорск', 'Семей', 
    'Атырау', 'Костанай', 'Кызылорда', 'Актау', 'Петропавловск', 
    'Талдыкорган', 'Кокшетау', 'Уральск'
]

def parse_price(text: str) -> int:
    """Извлекает цену из текста"""
    pattern = re.compile(r'(?P<num>\d{1,3}(?:[ \u00A0,]\d{3})*|\d+)\s*(?P<cur>₸|тг|тенге)?', re.IGNORECASE)
    candidates = []
    for m in pattern.finditer(text):
        raw = m.group('num').replace(' ', '').replace('\u00A0', '').replace(',', '')
        if not raw.isdigit():
            continue
        val = int(raw)
        cur = m.group('cur')
        candidates.append((val, bool(cur)))

    if not candidates:
        return 0

    with_currency = [v for v, has_cur in candidates if has_cur]
    if with_currency:
        return max(with_currency)

    no_currency = [v for v, has_cur in candidates if not has_cur]
    best = max(no_currency) if no_currency else 0
    return best if best >= 10_000 else 0

def detect_city(text: str) -> str:
    """Определяет город из текста"""
    for c in KZ_CITIES:
        if c in text:
            return c
    return "Не указано"

def now_str() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class KrishaParser:
    def __init__(self, verify_ssl: bool = True, base_delay=(1.1, 2.6)):
        self.verify_ssl = verify_ssl
        self.base_delay = base_delay
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        s = requests.Session()
        s.verify = self.verify_ssl
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        return s

    def _headers(self):
        return {"User-Agent": random.choice(USER_AGENTS)}

    def fetch(self, url: str, timeout: int = 15) -> Optional[bytes]:
        try:
            r = self.session.get(url, headers=self._headers(), timeout=timeout)
            r.raise_for_status()
            time.sleep(random.uniform(*self.base_delay))
            return r.content
        except Exception as e:
            logger.warning(f"fetch failed: {e}")
            return None

    def parse_url(self, url: str) -> List[Dict]:
        """Парсит страницу krisha.kz и возвращает список объявлений"""
        html = self.fetch(url)
        if html is None:
            raise RuntimeError("Не удалось получить страницу. Проверь ссылку/доступ/SSL.")

        soup = BeautifulSoup(html, 'lxml')
        items: List[Dict] = []

        # Различные селекторы для карточек объявлений на krisha.kz
        cards = soup.select(".a-card, .a-card__inc, .card--listing, .a-search-list-item")
        
        for c in cards:
            # Заголовок
            title_el = c.select_one('.a-card__title, a[title], h3, h2, .a-card__title-link')
            title = title_el.get_text(" ", strip=True) if title_el else ""

            # Цена
            price_el = c.select_one(
                '.a-card__price, .a-card__price ~ span, .card__price, .price, [data-price], .a-card__price-value'
            )
            if price_el:
                price_text = price_el.get_text(" ", strip=True)
            else:
                price_text = c.get_text(" ", strip=True)

            price = parse_price(price_text)
            if price <= 0:
                a_price = c.select_one('a[href][title]')
                if a_price:
                    price = parse_price(a_price.get_text(" ", strip=True))
            if price <= 0:
                continue

            # Локация
            location_el = c.select_one('.a-card__subtitle, .a-card__location, .location, .address')
            location_text = location_el.get_text(" ", strip=True) if location_el else ""
            if not location_text:
                location_text = c.get_text(" ", strip=True)
            location = detect_city(location_text)
            
            # Район (попытка извлечь)
            district = "Не указано"
            district_keywords = ['район', 'р-н', 'мкр', 'микрорайон']
            for keyword in district_keywords:
                if keyword in location_text.lower():
                    parts = location_text.split(',')
                    for part in parts:
                        if keyword in part.lower():
                            district = part.strip()
                            break
                    break

            # Описание
            desc_el = c.select_one('.a-card__description, .desc, p, .a-card__text')
            desc = desc_el.get_text(" ", strip=True) if desc_el else title

            # URL
            a = c.select_one('a[href]')
            href = a['href'] if a and a.has_attr('href') else None
            url_full = urljoin(url, href) if href else "N/A"

            # Площадь (если есть)
            area = None
            area_el = c.select_one('[class*="area"], [class*="square"], [class*="площадь"]')
            if area_el:
                area_text = area_el.get_text(" ", strip=True)
                area_match = re.search(r'(\d+(?:[.,]\d+)?)\s*м²', area_text)
                if area_match:
                    area = float(area_match.group(1).replace(',', '.'))

            # Количество комнат
            rooms = None
            rooms_el = c.select_one('[class*="room"], [class*="комнат"]')
            if rooms_el:
                rooms_text = rooms_el.get_text(" ", strip=True)
                rooms_match = re.search(r'(\d+)\s*(?:комн|комнат)', rooms_text, re.IGNORECASE)
                if rooms_match:
                    rooms = int(rooms_match.group(1))

            items.append({
                'marketplace': 'krisha.kz',
                'title': title,
                'price': price,
                'description': (desc[:200] + '...') if len(desc) > 200 else desc,
                'location': location,
                'district': district,
                'area': area,
                'rooms': rooms,
                'url': url_full,
                'scraped_at': now_str()
            })

        return items

