import sys

from kafka3 import KafkaProducer
import logging

logging.basicConfig(level=logging.INFO,format=" %(asctime)s - %(levelname)s, %(name)s ,%(message)s"  )


def kafka_Producer(**kwargs):
    try:
        topic = kwargs.get("topic","")
        print("starging producer")

        producer_setting = {"bootstrap_servers": servers}
        producer_setting.setdefault("security_protocol","SASL_SSL")
        producer_setting.setdefault("sas;_mechanisum","SCRAM-SHA-512")

        producer = KafkaProducer(**producer_setting)
        



    except Exception as e:
        print("Hi")