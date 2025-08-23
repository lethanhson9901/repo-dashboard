# Reddit Collector - Hướng dẫn Logging và Rate Limit Detection

## Tổng quan

Hệ thống logging đã được cải thiện để theo dõi chi tiết luồng fetch Reddit và phát hiện rate limit. Tất cả logs được lưu trong thư mục `logs/` với định dạng chi tiết và dễ đọc.

## Các tính năng logging mới

### 1. Logging chi tiết theo từng bước
- ✅ Khởi tạo Reddit client
- ✅ Kiểm tra kết nối API
- ✅ Thu thập danh sách subreddit
- ✅ Xử lý từng subreddit với progress tracking
- ✅ Xử lý posts và comments
- ✅ Lưu dữ liệu với thống kê

### 2. Rate Limit Detection
- ⚠️ Phát hiện `TooManyRequests` exceptions
- ⏳ Tự động chờ và retry
- 📊 Log chi tiết thông tin rate limit
- 🔄 Exponential backoff strategy

### 3. Performance Monitoring
- ⏱️ Thời gian xử lý từng bước
- 📈 Số lượng items xử lý
- 💾 Kích thước file output
- 🚀 Tốc độ xử lý

## Cách sử dụng

### Chạy script chính
```bash
cd backend/reddit
python get_news.py
```

### Chạy test logging
```bash
cd backend/reddit
python test_logging.py
```

## Cấu trúc logs

### File logs chính
- `logs/reddit_news.log` - Log từ script chính
- `logs/test_reddit_logging.log` - Log từ test script

### Format log
```
2024-01-15 10:30:15 - collector - INFO - 🚀 BẮT ĐẦU THU THẬP TIN TỨC REDDIT - 24 GIỜ QUA
2024-01-15 10:30:15 - collector - INFO - 📋 Đang kiểm tra biến môi trường...
2024-01-15 10:30:15 - collector - INFO - ✅ Biến môi trường đã được cấu hình thành công
2024-01-15 10:30:16 - collector - INFO - 🔧 Đang khởi tạo RedditContentCollector...
2024-01-15 10:30:16 - collector - INFO -    👤 Username: your_username
2024-01-15 10:30:16 - collector - INFO -    🆔 Client ID: abc12345...
2024-01-15 10:30:16 - collector - INFO -    🤖 User Agent: ContentCollector/1.0
2024-01-15 10:30:17 - collector - INFO - 🔍 Đang kiểm tra kết nối Reddit API...
2024-01-15 10:30:17 - collector - INFO -    ✅ Kết nối thành công! User: your_username
2024-01-15 10:30:17 - collector - INFO -    📅 Tài khoản tạo: 2020-01-01
2024-01-15 10:30:17 - collector - INFO -    🏆 Karma: 1000 link, 500 comment
```

### Rate Limit Detection
```
2024-01-15 10:35:20 - collector - WARNING - ==================================================
2024-01-15 10:35:20 - collector - WARNING - ⚠️  RATE LIMIT DETECTED!
2024-01-15 10:35:20 - collector - WARNING - ==================================================
2024-01-15 10:35:20 - collector - WARNING - 📍 Context: Fetching posts from r/programming
2024-01-15 10:35:20 - collector - WARNING - ⏰ Time: 2024-01-15 10:35:20
2024-01-15 10:35:20 - collector - WARNING - ⏳ Waiting: 60 seconds
2024-01-15 10:35:20 - collector - WARNING - 📋 Error details: 429 Too Many Requests
2024-01-15 10:35:20 - collector - WARNING - 📊 Response status: 429
2024-01-15 10:35:20 - collector - WARNING - ==================================================
2024-01-15 10:36:20 - collector - INFO - ✅ Rate limit wait completed, resuming...
```

## Thống kê và Performance

### Tổng kết cuối quá trình
```
================================================================================
📊 TỔNG KẾT THU THẬP TIN TỨC:
   - Subreddit đã xử lý: 25
   - Posts đã xử lý: 1250
   - Posts đạt tiêu chuẩn: 89
   - Comments đã xử lý: 445
   - Rate limit hits: 2
   - Tin tức cuối cùng: 89 items
================================================================================
```

### Performance metrics
```
📊 TỔNG KẾT:
   - Tổng thời gian: 45.23 giây
   - Thời gian thu thập: 42.15 giây
   - Thời gian lưu: 3.08 giây
   - Số tin tức thu thập: 89 items
   - Tốc độ thu thập: 2.11 items/giây
```

## Cấu hình logging

### Log levels
- `DEBUG`: Chi tiết nhất, bao gồm thông tin từng post/comment
- `INFO`: Thông tin chính về tiến trình
- `WARNING`: Rate limit và các cảnh báo
- `ERROR`: Lỗi nghiêm trọng

### Thay đổi log level
Trong `get_news.py`:
```python
logging.basicConfig(
    level=logging.INFO,  # Thay đổi thành logging.DEBUG để có thông tin chi tiết hơn
    # ...
)
```

## Troubleshooting

### Rate limit thường xuyên
- Giảm `limit` parameter trong `get_community_news()`
- Tăng thời gian chờ giữa các request
- Kiểm tra Reddit API limits

### Log file quá lớn
- Giảm log level từ `DEBUG` xuống `INFO`
- Xóa log files cũ định kỳ
- Sử dụng log rotation

### Lỗi kết nối
- Kiểm tra credentials trong `.env`
- Kiểm tra internet connection
- Verify Reddit API status

## Monitoring và Alerting

### Key metrics cần theo dõi
1. **Rate limit hits**: Nếu > 5 trong 1 giờ
2. **Error rate**: Nếu > 10% requests fail
3. **Processing time**: Nếu > 5 phút cho 1000 posts
4. **Data quality**: Số lượng items thu thập được

### Alerting suggestions
- Monitor log files cho rate limit patterns
- Set up alerts cho error rates cao
- Track performance degradation over time

## Best Practices

1. **Rate Limiting**: Luôn respect Reddit API limits
2. **Error Handling**: Log đầy đủ thông tin lỗi
3. **Performance**: Monitor và optimize processing time
4. **Data Quality**: Validate data trước khi lưu
5. **Security**: Không log sensitive information

## Support

Nếu gặp vấn đề với logging hoặc rate limiting:
1. Kiểm tra log files trong `logs/`
2. Chạy test script: `python test_logging.py`
3. Review Reddit API documentation
4. Contact development team
