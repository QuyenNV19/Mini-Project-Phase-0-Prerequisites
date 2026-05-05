import time
import concurrent.futures
from collections import deque
from urllib.parse import urlparse
from base_strategy import DeepCrawlStrategy

class BFSDeepCrawlStrategy(DeepCrawlStrategy):
    def crawl(self, start_url, max_depth, max_pages, fetcher, same_domain_only):
        results = []
        visited = set()
        queue = deque([(start_url, 0)])
        initial_domain = urlparse(start_url).netloc

        product_map = {}  # url -> product

        # Sử dụng ThreadPoolExecutor để tăng tốc độ lấy chi tiết sản phẩm
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while queue and len(results) < max_pages:
                url, depth = queue.popleft()

                if url in visited or depth > max_depth:
                    continue

                visited.add(url)

                content = fetcher.fetch(url)
                if not content:
                    continue

                # -------------------------
                # 1. LIST PAGE
                # -------------------------
                infos = self._extract_info(content, url)
                
                new_infos = []
                for p in infos:
                    if p["url"] not in product_map and len(results) < max_pages:
                        product_map[p["url"]] = p
                        results.append(p)
                        new_infos.append(p)

                # -------------------------
                # 2. DETAIL PAGE (GET DESCRIPTION) - CONCURRENT
                # -------------------------
                if new_infos:
                    def fetch_detail(p):
                        time.sleep(0.5) 
                        detail_html = fetcher.fetch(p["url"])
                        if detail_html:
                            desc = self._extract_description(detail_html)
                            p["description"] = desc
                        return p

                    list(executor.map(fetch_detail, new_infos))

                # -------------------------
                # 3. CRAWL LINKS
                # -------------------------
                if depth < max_depth:
                    for link in self._extract_links(content, url):
                        if link not in visited:
                            if not same_domain_only or urlparse(link).netloc == initial_domain:
                                queue.append((link, depth + 1))

        return results
