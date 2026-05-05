import sys
import os
from elasticsearch import Elasticsearch, helpers

# Thêm project root vào path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_products_collection
from config import settings

def index_data_from_mongodb():
    """
    Đọc dữ liệu từ MongoDB và đẩy vào Elasticsearch.
    """
    es = Elasticsearch([settings.ES_HOST])
    collection = get_products_collection()
    
    print("Đang lấy dữ liệu từ MongoDB...")
    products = list(collection.find({}))
    
    if not products:
        print("Không có dữ liệu trong MongoDB để index.")
        return

    print(f"Đang chuẩn bị index {len(products)} sản phẩm vào Elasticsearch...")
    
    actions = []
    for product in products:
        # Loại bỏ trường _id của MongoDB vì không tương thích trực tiếp với ES
        doc = product.copy()
        doc_id = str(doc.pop("_id"))
        
        actions.append({
            "_index": settings.ES_INDEX,
            "_id": doc_id,
            "_source": doc
        })
    
    try:
        # Sử dụng bulk API để index nhanh hơn
        success, failed = helpers.bulk(es, actions)
        print(f"Hoàn thành! Thành công: {success}, Thất bại: {failed}")
    except Exception as e:
        print(f"Lỗi khi index dữ liệu vào Elasticsearch: {e}")

if __name__ == "__main__":
    print("--- ELASTICSEARCH INDEXER ---")
    index_data_from_mongodb()
