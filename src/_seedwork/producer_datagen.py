from datetime import datetime
import time
from typing import Optional
from kafka import KafkaProducer, Serializer
import json
from dotenv import load_dotenv
import os
import random_address

load_dotenv()


class Producer:
    producer: KafkaProducer
    user: str

    def __init__(self, user: Optional[str] = None, password: Optional[str] = None) -> None:
        self.user = user if user is not None else os.getenv("AIVEN_SASL_USERNAME")

        dev_args = {
            "bootstrap_servers": "kafka-aiven_kafka_1:9092" # NOSONAR
        }

        prod_args = {
            "bootstrap_servers": os.getenv("AIVEN_BOOTSTRAP_SERVER"),
            "security_protocol": "SASL_SSL",
            "sasl_mechanism": "PLAIN",
            "sasl_plain_username": self.user,
            "sasl_plain_password": password if password is not None else os.getenv("AIVEN_SASL_PASSWORD"),
            "ssl_cafile": "ca.pem"
        }

        args = dev_args if os.getenv("ENVIRONMENT") == "local" else prod_args

        self.producer = KafkaProducer(
            client_id="aiven-producer-pyx",
            acks=0,
            retries=3,
            max_in_flight_requests_per_connection=1,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),

            **args   
        )
    
    def publish_message(
        self,
        message: dict,
        topic: str
    ) -> None: 
        self.producer.send(
            topic,
            message,
            key=b"some.key",
            headers=[
                ('wex.event_name', b'transaction-created'),
                ('wex.producer_name', self.user.encode('utf-8')),
            ],
        ).add_callback(self._on_send_success).add_errback(self._on_send_error)

        self.producer.flush()

    def _on_send_success(self, record_metadata):
        print(record_metadata)
        print(f"{record_metadata.topic}/partition={record_metadata.partition}/offset={record_metadata.offset}")

    def _on_send_error(self, exception):
        print(exception)

if __name__ == "__main__":
    _id = 1
    while True:
        schema = {
            "orderId": _id,
            "orderTime": datetime.now().timestamp(),
            "orderAddress": random_address.real_random_address_by_state('CA')["address1"],
        }

        _id += 1
        print(schema)
     
        producer = Producer()
        producer.publish_message(
            message=schema,
            topic="transactions"
        )
     
        time.sleep(2)
