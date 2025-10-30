import json
from confluent_kafka import Producer

def report(err, msg):
    if err:
        print(f"❌ Sending to Kafka failed: {err}")
    else:
        # print(f"💬 Message {msg.value().decode('utf-8')}")
        print(f"✅ Sent to Kafka: topic = {msg.topic()}; partition = {msg.partition()}; offset = {msg.offset()}")

def send_output_file_to_kafka(
    output_file:str,
    server:str="localhost:9092",
    topic:str="training.metrics"
    ):
    """Read records from output file and send to Kafka."""
    
    producer = Producer({"bootstrap.servers": server})
    
    with open(output_file, 'r') as file:
        output_file_data = [json.loads(line) for line in file]

    for record in output_file_data:
        # record.update({'record_id': str(uuid.uuid4())})
        value = json.dumps(record).encode("utf-8")
        producer.produce(
            topic=topic,
            value=value,
            callback=report
        )
    producer.flush()
    
class KafkaProducerWrapper:
    def __init__(self, server: str = "localhost:9092"):
        self.kafka_producer = Producer({"bootstrap.servers": server})
    
    def produce(self, topic: str, value: bytes):
        self.kafka_producer.produce(
            topic=topic,
            value=value,
            callback=report
        )
        self.kafka_producer.flush()    