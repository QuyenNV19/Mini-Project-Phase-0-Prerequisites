#!/bin/bash

# Hàm kiểm tra Elasticsearch đã sẵn sàng chưa
wait_for_elasticsearch() {
  echo "Đang đợi Elasticsearch tại $ES_HOST sẵn sàng..."
  until curl -s "$ES_HOST" > /dev/null; do
    echo "Elasticsearch chưa sẵn sàng, đang thử lại sau 5 giây..."
    sleep 5
  done
  echo "Elasticsearch đã sẵn sàng!"
}

# Đợi ES
wait_for_elasticsearch

# Tự động nạp dữ liệu từ file JSON vào Elasticsearch
echo "Bắt đầu nạp dữ liệu tự động..."
python data_pipeline/indexer.py

# Khởi động Search API
echo "Khởi động Search API..."
uvicorn search_service.main:app --host 0.0.0.0 --port 8000
