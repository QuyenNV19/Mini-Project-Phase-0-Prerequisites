FROM python:3.10-slim

# Cài đặt curl để kiểm tra trạng thái Elasticsearch
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cấp quyền thực thi cho script khởi động
RUN chmod +x entrypoint.sh

# Sử dụng entrypoint script để tự động hóa việc nạp dữ liệu và bật API
CMD ["./entrypoint.sh"]