# microservices-blueprint-python
Thin Blueprint of microservices in python containing : REST API, kafka producer/consumer, grafana dashboard, writing files to S3


Run:
=====

apigateway service: 

```
$pip3 install flask
$pip3 install kafka-python
$python api-gateway.py
```

s3 writer service: 

```
$python upload-to-s3.py
```

Create kafka on docker:
========================
```
$ docker pull wurstmeister/kafka
$ docker pull wurstmeister/zookeeper

$ git clone https://github.com/wurstmeister/kafka-docker.git 
$ cd kafka-docker 
```

### Create the compose file: 
```$ vim docker-compose.yml```

docker-compose.yml:
```
version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper:3.4.6
    ports:
     - "2181:2181"
  kafka:
    build: .
    ports:
     - "9092:9092"
    expose:
     - "9093"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:9093,OUTSIDE://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_LISTENERS: INSIDE://0.0.0.0:9093,OUTSIDE://0.0.0.0:9092
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
```

### Start the container : 
```$ docker-compose up -d```

### Get the docker process ID of the Kafka Docker running so you can acces it
```$docker exec -i -t -u root $(docker ps | grep docker_kafka | cut -d' ' -f1) /bin/bash
   bash>(docker ps | grep docker_kafka | cut -d' ' -f1)
```

### Create a topic
```bash> $KAFKA_HOME/bin/kafka-topics.sh --create --partitions 4 --bootstrap-server kafka:9092 --topic my-first-topic```

Grafana with Docker: 
=====================
```
docker run -d -p 3000:3000 \
  --name=grafana \
  -e 'GF_INSTALL_PLUGINS=grafana-simple-json-datasource' \
  grafana/grafana
```

### Log into Grafana with admin:admin
```http://localhost:3000 ```

### Create a datasource in Grafana with type="SimpleJson" and URL="http://docker.for.mac.localhost:5000".
