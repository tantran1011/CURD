from datetime import datetime

# Giả sử đây là dữ liệu lấy từ database (dưới dạng list of dicts hoặc tuples)
products = [
  {
    "user_id": 3,
    "id": 1,
    "product_id": 1,
    "created_at": "2025-05-16T21:02:33.273199",
    "total_price": 1960000,
    "order_day": "2025-05-16T21:02:33.273192",
    "updated_at": "2025-05-16T21:02:33.273199"
  },
  {
    "user_id": 3,
    "id": 2,
    "product_id": 2,
    "created_at": "2025-05-16T21:05:10.481821",
    "total_price": 50000,
    "order_day": "2025-05-16T21:05:10.481813",
    "updated_at": "2025-05-16T21:11:43.547913"
  }
]
# Chuyển string sang datetime và lấy (year, month)
created_months = set(
    (datetime.fromisoformat(p["created_at"]).year, datetime.fromisoformat(p["created_at"]).month)
    for p in products
)

for year, month in created_months:
    avg = sum(p["total_price"] for p in products if datetime.fromisoformat(p["created_at"]).year == year and datetime.fromisoformat(p["created_at"]).month == month) / len([p for p in products if datetime.fromisoformat(p["created_at"]).year == year and datetime.fromisoformat(p["created_at"]).month == month]
    )
    print(f"Average price for {year}-{month}: {avg}")
