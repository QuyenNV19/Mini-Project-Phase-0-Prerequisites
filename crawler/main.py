from strategies import BFSDeepCrawlStrategy
from config import CrawlerRunConfig
from crawler import WebCrawler

if __name__ == "__main__":
    entry_url = "https://chiaki.vn/"

    bfs_strategy = BFSDeepCrawlStrategy()
    config = CrawlerRunConfig(
        deep_crawl_strategy=bfs_strategy,
        max_depth=1,
        max_pages=10,   # 🔥 chỉ lấy 10 sản phẩm
        same_domain_only=True
    )

    crawler = WebCrawler()

    print("\n--- ĐANG CRAWL 10 SẢN PHẨM ---\n")

    results = crawler.run(entry_url, config)

    if results:
        for i, p in enumerate(results[:10], 1):
            print(f"\n[{i}] ------------------------")
            print(f"Tên        : {p.get('name')}")
            print(f"URL        : {p.get('url')}")
            print(f"Image      : {p.get('image_url')}")
            print(f"Giá        : {p.get('price')}")
            print(f"Rating     : {p.get('rating')}")
            print(f"Đã bán     : {p.get('sold')}")
            print(f"Mô tả      : {p.get('description')[:200] if p.get('description') else 'None'}")
    else:
        print("Không tìm thấy sản phẩm nào hoặc có lỗi xảy ra.")
