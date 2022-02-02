#!/usr/bin/env python3

import os
import sys
from inotify.adapters import Inotify
from kafka import KafkaProducer

def main(watch_folder=os.getcwd()):
    kafka_server='localhost'
    topic='ClipTrafficLight'

    producer = KafkaProducer(bootstrap_servers=kafka_server)

    # for _ in range(5):
    #     producer.send(topic=topic, key=b'test',value=b'some_message_bytes')
    #     producer.flush()

    i = Inotify()
    i.add_watch(watch_folder)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        print("File: {:20} | event: {}".format(filename, type_names))

        # on file write completion, we publish to topic
        key='test'
        if 'IN_CLOSE_WRITE' in type_names:
            print("[Kafka Publishing] key=: {}; value: {}".format(key, filename))
            producer.send(topic=topic, key=str.encode(key), value=str.encode(filename))
            producer.flush()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()