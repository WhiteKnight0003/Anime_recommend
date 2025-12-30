## Parent image python 3.10
FROM python:3.12-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container - app là nơi mà ta chạy 1 lần code duy nhất
WORKDIR /app

## Installing system dependancies - cài đặt thư viện
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying ur all contents from local to app - sao chép toàn bộ cấu trúc dự án 
COPY . .

## Run setup.py - kiểu khi chạy dự án sẽ có forder __pycache__ - lệnh --no-cache-dir sẽ bỏ qua nó 
RUN pip install --no-cache-dir -e .

# Used PORTS - streamlit chạy mặc định trên cổng 8501
EXPOSE 8501

# Run the app - docker chỉ viết 1 lệnh để chạy ứng dụng
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0","--server.headless=true"]

# --server.port=8501  - cổng mặc định giúp bạn dễ dàng cấu hình "Port Mapping" (ánh xạ cổng) từ thế giới bên ngoài vào trong container

# --server.address=0.0.0.0 
# Địa chỉ 127.0.0.1 (Localhost): Giống như việc bạn chỉ mở cửa nội bộ cho nhân viên trong nhà. Người đi đường (người dùng internet) không thể vào được
# Địa chỉ 0.0.0.0: Có nghĩa là "Tôi chấp nhận kết nối từ bất cứ đâu". Nó bảo container rằng hãy lắng nghe mọi yêu cầu gửi đến từ internet, không chỉ riêng từ bên trong máy chủ.

# --server.headless=true"
# Khi bạn chạy Streamlit trên máy tính, nó sẽ tự động "nhảy" ra một tab trình duyệt (Chrome/Edge).
# Tuy nhiên, khi deploy lên Server (như AWS, Google Cloud), các máy chủ này không có màn hình và không có trình duyệt.
# Nếu Streamlit cố gắng mở trình duyệt, nó sẽ bị lỗi vì không tìm thấy màn hình đâu cả. headless=true bảo nó: "Đừng cố mở trình duyệt, cứ chạy ngầm và chờ khách truy cập qua mạng thôi".