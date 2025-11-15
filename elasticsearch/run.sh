docker run \
  -d \
  --rm \
  --name study_elastic \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=true" \
  -e "ELASTIC_PASSWORD=password" \
  -e "ES_JAVA_OPTS=-Xms256m -Xmx256m" \
  -e "xpack.security.http.ssl.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.0
