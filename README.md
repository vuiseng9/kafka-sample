# Simple Kafka Deployment

## Host kafka and zookeeper server
---------
```bash
docker-compose -f docker-compose-kafka.yml up -d
```
Do take note of container runtime label
```
# Output
Starting vuiseng9_zookeeper_1 ... done
Starting vuiseng9_kafka_1     ... done
```

## Kafka Listener App
----------------
Simple topic consumer app - a console that prints pushed notifications by producer.
Do change the container and topic name accordingly. 
```bash
# Start consumer app
docker exec -it vuiseng9_kafka_1 /opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ClipTrafficLight
```

## Kafka Producer App
-----------------
We will use OpenVINO DLStreamer Image as base setup for producer app
```bash
# start dlstreamer container
./run_dl_streamer_container.sh
```

```
# within dlstreamer container, install the following packages
apt-get update && apt-get install -y \
    kafkacat inotify-tools
```
**App 1 - Manual Publishing**
```bash
kafkacat -P -b localhost:9092 -t ClipTrafficLight
```
After the execution of the command above, input text message and hit enter! You should see the same message in consumer console above
```bash
testclip:ready
clipx:yready
```
**App 2 - Automated notification with Kafka topic on events
The enclosed ```watch_and_notify.py``` is a python script that loops indefinitely, when a new file is added to its working directory, it notifies kafka consumer with the file name and timestamp.
```bash
# run watch_and_notify.py as background process
export WATCH_DIR=/tmp/target_folder # <folder_to_watch>
export TOPIC=ClipTrafficLight
python watch_and_notify.py $WATCH_DIR $TOPIC &
```
To simulate file creation, we use ffmpeg to split video into multiple clips and store them in the target folder watched by the python script. On execution of the following command line, do observe the consumer console app, you will see the notifications.
```

```
----------
### References
https://github.com/openvinotoolkit/dlstreamer_gst/blob/master/samples/gst_launch/metapublish/listener.md

https://codingharbour.com/apache-kafka/learn-how-to-use-kafkacat-the-most-versatile-cli-client/
