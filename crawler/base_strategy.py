import re
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class DeepCrawlStrategy(ABC):
    @abstractmethod
    def crawl(self, start_url, max_depth, max_pages, fetcher, same_domain_only) -> list[dict]:
        pass

    def _extract_links(self, html_content, base_url):
        links = []
        soup = BeautifulSoup(html_content, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(base_url, href)
            full_url, _ = urldefrag(full_url)

            parsed = urlparse(full_url)

            if parsed.scheme in {"http", "https"} and parsed.netloc:
                links.append(full_url)

        return links

    def _extract_info(self, html_content, url):
        soup = BeautifulSoup(html_content, "html.parser")

        products = []
        items = soup.find_all("div", class_="product-item")

        for item in items:
            try:
                a_tag = item.select_one("h3.product-title a")
                if not a_tag:
                    continue

                name = a_tag.get("title") or a_tag.get_text(strip=True)
                product_url = urljoin(url, a_tag["href"])

                # IMAGE
                img_tag = item.select_one("picture source")
                image_url = None
                if img_tag and img_tag.get("srcset"):
                    image_url = img_tag["srcset"]
                else:
                    img2 = item.select_one("img")
                    if img2:
                        image_url = img2.get("src")

                # PRICE
                price_tag = item.select_one("div.product-price span")
                price = int(re.sub(r"[^\d]", "", price_tag.text)) if price_tag else None

                # RATING
                rating_tag = item.select_one("div.rating-star-count")
                rating = float(rating_tag.text) if rating_tag else None

                # SOLD
                sold_tag = item.select_one("div.feature-sold")
                sold = int(re.sub(r"[^\d]", "", sold_tag.text)) if sold_tag else 0

                products.append({
                    "name": name,
                    "url": product_url,
                    "image_url": image_url,
                    "price": price,
                    "rating": rating,
                    "sold": sold,
                    "description": None  # sẽ fill ở bước detail
                })

            except Exception:
                continue

        return products

    def _extract_description(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        selectors = [
            "div.product-description",
            "#description",
            ".product-content",
            ".content"
        ]

        for sel in selectors:
            desc = soup.select_one(sel)
            if desc:
                return desc.get_text(separator="\n", strip=True)

        return None
