import json

from confluent_kafka import Consumer

class KafkaTracker:
    def __init__(
        self, 
        subscribe_topic: str = "training.metrics",
        server: str = "localhost:9092",
        group_id: str = "record-tracker"):
        
        self.consumer = Consumer({
            "bootstrap.servers": server,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.consumer.subscribe([subscribe_topic])
        print(f"KafkaTracker initialized and subscribed to {subscribe_topic} topic")

    def track(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("❌ Error:", msg.error())
                    continue

                value = msg.value().decode("utf-8")
                record = json.loads(value)
                print(f"🟢 Received record from {record['user_id']}")
        except KeyboardInterrupt:
            print("\nStopping KafkaTracker")
        finally:
            self.consumer.close()