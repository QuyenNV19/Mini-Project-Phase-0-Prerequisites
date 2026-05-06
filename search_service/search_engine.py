from elasticsearch import Elasticsearch
import sys
import os

# Thêm project root vào path để import settings
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from config import settings

class SearchEngine:
    def __init__(self):
        self.es = Elasticsearch([settings.ES_HOST])
        self.index = settings.ES_INDEX

    def search_by_name(self, query: str, size: int = 10):
        """
        Tìm kiếm sản phẩm theo tên sử dụng match query và fuzziness.
        """
        if not query:
            return []

        search_query = {
            "query": {
                "match": {
                    "name": {
                        "query": query,
                        "operator": "and",
                        "fuzziness": "AUTO"
                    }
                }
            },
            "size": size
        }

        try:
            response = self.es.search(index=self.index, body=search_query)
            hits = response.get("hits", {}).get("hits", [])
            
            results = []
            for hit in hits:
                source = hit.get("_source", {})
                results.append({
                    "name": source.get("name"),
                    "price": source.get("price"),
                    "rating": source.get("rating"),
                    "sold": source.get("sold"),
                    "url": source.get("url"),
                    "image_url": source.get("image_url"),
                    "description": source.get("summary") or (source.get("description")[:200] + "..."),
                    "comments": source.get("comments")
                })
            return results
            
        except Exception as e:
            print(f"Lỗi khi truy vấn Elasticsearch: {e}")
            return []
