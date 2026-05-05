import sys
import os
import json
from elasticsearch import Elasticsearch, helpers

# Thêm project root vào path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_products_collection
from config import settings

def index_data():
    """
    Đọc dữ liệu từ file JSON (ưu tiên) hoặc MongoDB và đẩy vào Elasticsearch.
    Sử dụng URL làm _id để tránh trùng lặp dữ liệu.
    """
    es = Elasticsearch([settings.ES_HOST])
    
    # Ưu tiên đọc từ file JSON đã xử lý
    json_path = os.path.join(project_root, "data_pipeline", "data_processed.json")
    products = []
    
    if os.path.exists(json_path):
        print(f"Đang đọc dữ liệu từ file: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
    else:
        print("Không thấy file JSON, đang thử lấy dữ liệu từ MongoDB...")
        collection = get_products_collection()
        products = list(collection.find({}))

    if not products:
        print("Không có dữ liệu để index.")
        return

    print(f"Đang chuẩn bị index {len(products)} sản phẩm vào Elasticsearch...")
    
    actions = []
    for product in products:
        # Sử dụng URL làm ID duy nhất để tránh trùng lặp khi chạy lại nhiều lần
        doc_id = product.get("url")
        
        # Sao chép dữ liệu và loại bỏ _id của MongoDB nếu có
        source_data = product.copy()
        if "_id" in source_data:
            source_data.pop("_id")
            
        actions.append({
            "_index": settings.ES_INDEX,
            "_id": doc_id,
            "_source": source_data
        })
    
    try:
        success, failed = helpers.bulk(es, actions)
        print(f"Hoàn thành! Thành công: {success}, Thất bại: {failed}")
    except Exception as e:
        print(f"Lỗi khi index dữ liệu vào Elasticsearch: {e}")

if __name__ == "__main__":
    print("--- ELASTICSEARCH INDEXER ---")
    index_data()
