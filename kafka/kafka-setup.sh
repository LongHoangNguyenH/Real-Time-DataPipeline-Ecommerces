#/bin/bash
ContainerKafka="kafka"

docker exec -u 0 kafka bash -c "kafka-topics.sh --create --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 --topic Ecommerce_topic"