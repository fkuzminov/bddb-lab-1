docker run \
  -d \
  --rm \
  --name study_postgres \
  -p 5432:5432 \
  -v "$(pwd)/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql" \
  -e POSTGRES_DB=students \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  postgres:14

