# Simple Kafka Deployment
No build needed. An example of mini kafka deployment using public containers.

## Host kafka and zookeeper server
---------
```bash
docker-compose -f docker-compose-kafka.yml up -d
```
Do take note of container runtime label
```
# Output
Creating network "kafka-sample_kafka-net" with driver "bridge"
Creating kafka-sample_zookeeper_1 ... done
Creating kafka-sample_kafka_1     ... done
```

## Kafka Listener App
----------------
Simple topic consumer app - a console that prints pushed notifications by producer.
Do change the container and topic name accordingly. 
```bash
# Start consumer app
docker exec -it kafka-sample_kafka_1 /opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ClipTrafficLight
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

# install pip packages
pip install inotify kafka-python
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

**App 2 - Automated notification with Kafka topic on events**

We will need two terminals here.

*Terminal 1* 

The enclosed ```watch_and_notify.py``` is a python script that loops indefinitely, when a new file is added to the directory under supervision, it notifies kafka consumer with the file name and timestamp. The script prints all events pertaining to the directory and looks out for ```'IN_CLOSE_WRITE'``` event for publishing.

```bash
# download this script to dlstreamer runtime
wget 

# run watch_and_notify.py as background process
export WATCH_DIR=/tmp/target_folder # <folder_to_watch>
mkdir -p $WATCH_DIR
python watch_and_notify.py $WATCH_DIR &
```

*Terminal 2* 

To simulate file creation, in dlstreamer container, we use ffmpeg to split video into multiple clips and store them in the target folder watched by the python script. 
```bash
export WATCH_DIR=/tmp/target_folder

ffmpeg -i https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4 -c copy -segment_time 10 -f segment ${WATCH_DIR}/output_video%03d.mp4
```

Expected output in Kafka Consumer Console:
```
vuiseng9@tglxe:~/kafka-sample$ docker exec -it kafka-sample_kafka_1 /opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ClipTrafficLight
output_video000.mp4
output_video001.mp4
output_video002.mp4
output_video003.mp4
output_video004.mp4
output_video005.mp4

```

Expected output in terminal 1:
```
root@tglxe:/opt/intel/openvino_2021.4.752# python3 /hosthome/kafka-sample/watch_and_notify.py $WATCH_DIR &
File: output_video000.mp4  | event: ['IN_CREATE']
File: output_video000.mp4  | event: ['IN_OPEN']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_MODIFY']
File: output_video000.mp4  | event: ['IN_CLOSE_WRITE']
[Kafka Publishing] key=: test; value: output_video000.mp4
File: output_video001.mp4  | event: ['IN_CREATE']
File: output_video001.mp4  | event: ['IN_OPEN']
File: output_video001.mp4  | event: ['IN_MODIFY']
File: output_video001.mp4  | event: ['IN_MODIFY']
File: output_video001.mp4  | event: ['IN_MODIFY']
File: output_video001.mp4  | event: ['IN_MODIFY']
File: output_video001.mp4  | event: ['IN_MODIFY']
File: output_video001.mp4  | event: ['IN_CLOSE_WRITE']
[Kafka Publishing] key=: test; value: output_video001.mp4
File: output_video002.mp4  | event: ['IN_CREATE']
File: output_video002.mp4  | event: ['IN_OPEN']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_MODIFY']
File: output_video002.mp4  | event: ['IN_CLOSE_WRITE']
[Kafka Publishing] key=: test; value: output_video002.mp4
File: output_video003.mp4  | event: ['IN_CREATE']
File: output_video003.mp4  | event: ['IN_OPEN']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_MODIFY']
File: output_video003.mp4  | event: ['IN_CLOSE_WRITE']
[Kafka Publishing] key=: test; value: output_video003.mp4
File: output_video004.mp4  | event: ['IN_CREATE']
File: output_video004.mp4  | event: ['IN_OPEN']
File: output_video004.mp4  | event: ['IN_MODIFY']
File: output_video004.mp4  | event: ['IN_MODIFY']
File: output_video004.mp4  | event: ['IN_MODIFY']
File: output_video004.mp4  | event: ['IN_MODIFY']
File: output_video004.mp4  | event: ['IN_MODIFY']
File: output_video004.mp4  | event: ['IN_CLOSE_WRITE']
[Kafka Publishing] key=: test; value: output_video004.mp4
File: output_video005.mp4  | event: ['IN_CREATE']
File: output_video005.mp4  | event: ['IN_OPEN']
File: output_video005.mp4  | event: ['IN_MODIFY']
File: output_video005.mp4  | event: ['IN_MODIFY']
File: output_video005.mp4  | event: ['IN_MODIFY']
File: output_video005.mp4  | event: ['IN_MODIFY']
File: output_video005.mp4  | event: ['IN_MODIFY']
File: output_video005.mp4  | event: ['IN_CLOSE_WRITE']
[Kafka Publishing] key=: test; value: output_video005.mp4
```
----------
### References
https://github.com/openvinotoolkit/dlstreamer_gst/blob/master/samples/gst_launch/metapublish/listener.md

https://codingharbour.com/apache-kafka/learn-how-to-use-kafkacat-the-most-versatile-cli-client/

https://linuxhint.com/python_inotify_examples/

https://kafka-python.readthedocs.io/en/master/
