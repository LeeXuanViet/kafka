from kafka import KafkaProducer
import json
import random
import time

# Khởi tạo Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_transaction():
    """Mô phỏng dữ liệu giao dịch chứng khoán"""
    return {
        "transaction_id": random.randint(1000, 9999),
        "stock_symbol": random.choice(["AAPL", "MSFT", "GOOGL", "AMZN"]),
        "price": round(random.uniform(100, 1500), 2),
        "volume": random.randint(10, 1000)
    }

# Gửi dữ liệu vào topic 'stock-transactions' liên tục
try:
    while True:
        transaction = generate_transaction()
        producer.send('stock-transactions', value=transaction)
        print(f"Gửi giao dịch: {transaction}")
        time.sleep(1)  # Dừng 1 giây trước khi gửi giao dịch tiếp theo
except KeyboardInterrupt:
    print("Dừng Producer.")
finally:
    producer.close()
