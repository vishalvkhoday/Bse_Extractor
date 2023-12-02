import sys

from kafka3 import KafkaProducer
import logging

logging.basicConfig(level=logging.INFO,format=" %(asctime)s - %(levelname)s, %(name)s ,%(message)s"  )


def kafka_consumer(args):
    topic = args
    kafkaConsumer = "Kakfaconsumer name"
    is_offset_reset = kafkaConsumer['is_offset_reset']
    offset_reset = 'earliest' if is_offset_reset else 'latest'

    rewind_last_offset = ""
    rewind_nos = 22
    is_partition_set = True
    partitions = 'partition'


    consumer_setting = {
        "bootstrap_server":servers,
        "auto_offset_reset": offset_reset

    }
    producer_setting = {"bootstrap_servers": servers}
    producer_setting.setdefault("security_protocol","SASL_SSL")
    producer_setting.setdefault("sas;_mechanisum","SCRAM-SHA-512")

    consumer = kafkaConsumer(**consumer_setting)

    if is_partition_set:
        for topic in topic:
            partitions_list = consumer.partitions_for_topic(topic)

            if partitions:
                partitions_list = set(partitions).intersection(set(partitions_list))
                partitions_list = list(partitions_list)
                tp_list = p[TopicPartition(topic,p) for p in partitions_list]
                consumer.assign(tp_list)

                if is_last_offset:
                    last_offset = per_partition = consumer.end_offsets(to_list)

                    for tp in tp_list:
                        offset = last_offset_per_partition[tp]
                        