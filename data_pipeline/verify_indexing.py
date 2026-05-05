import os
import sys
import time

# Thêm project root vào path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from elasticsearch import Elasticsearch
from config import settings
from indexer import index_data

def verify_no_duplicates():
    es = Elasticsearch([settings.ES_HOST])
    index_name = settings.ES_INDEX

    print("--- BẮT ĐẦU KIỂM TRA TRÙNG LẶP ---")
    
    # 1. Đếm số lượng hiện tại
    try:
        count_before = es.count(index=index_name)['count']
        print(f"Số lượng sản phẩm TRƯỚC khi index lại: {count_before}")
    except Exception as e:
        print(f"Lỗi khi đếm (có thể index chưa tồn tại): {e}")
        count_before = 0

    # 2. Chạy Indexer lại
    print("\nĐang thực hiện index lại dữ liệu...")
    index_data()
    
    # Đợi một chút để ES cập nhật (refresh)
    time.sleep(1)
    es.indices.refresh(index=index_name)

    # 3. Đếm lại số lượng
    try:
        count_after = es.count(index=index_name)['count']
        print(f"Số lượng sản phẩm SAU khi index lại: {count_after}")
    except Exception as e:
        print(f"Lỗi khi đếm lại: {e}")
        return

    # 4. Kết luận
    print("\n--- KẾT QUẢ ---")
    if count_before == count_after and count_after > 0:
        print("✅ THÀNH CÔNG: Số lượng không thay đổi. Cơ chế chống trùng lặp (Idempotency) hoạt động tốt!")
    elif count_after > count_before:
        print(f"❌ THẤT BẠI: Số lượng tăng từ {count_before} lên {count_after}. Dữ liệu bị trùng lặp!")
    else:
        print("ℹ️ Chú ý: Cần có dữ liệu sẵn trong ES để kiểm tra chính xác nhất.")

if __name__ == "__main__":
    verify_no_duplicates()
