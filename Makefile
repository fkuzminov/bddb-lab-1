.PHONY: run-pg stop-pg run-mongo stop-mongo run-neo4j stop-neo4j init-spark clean-spark run-es stop-es run-query

run-pg:
	@echo "Stopping existing container if running."
	@docker stop study_postgres 2>/dev/null || true
	@echo "Starting PostgreSQL container."
	@cd postgresql && bash run.sh
	@echo "Waiting for PostgreSQL to be ready."
	@sleep 3
	@until docker exec study_postgres pg_isready -U postgres > /dev/null 2>&1; do \
		echo "Waiting for database."; \
		sleep 1; \
	done
	@echo "PostgreSQL is ready."
	@echo "Running data generation script."
	@cd postgresql && python3 init_db.py
	@echo "Database is ready to use."

stop-pg:
	@echo "Stopping PostgreSQL container."
	@docker stop study_postgres 2>/dev/null || true
	@echo "Container stopped."

run-mongo:
	@echo "Stopping existing container if running."
	@docker stop study_mongo 2>/dev/null || true
	@echo "Starting MongoDB container."
	@cd mongodb && bash run.sh
	@echo "Waiting for MongoDB to be ready."
	@sleep 3
	@until docker exec study_mongo mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do \
		echo "Waiting for database."; \
		sleep 1; \
	done
	@echo "MongoDB is ready."
	@echo "Running data generation script."
	@cd mongodb && python3 init_db.py
	@echo "Database is ready to use."

stop-mongo:
	@echo "Stopping MongoDB container."
	@docker stop study_mongo 2>/dev/null || true
	@echo "Container stopped."

run-neo4j:
	@echo "Stopping existing container if running."
	@docker stop study_neo4j 2>/dev/null || true
	@echo "Starting Neo4j container."
	@cd neo4j && bash run.sh
	@echo "Waiting for Neo4j to be ready."
	@sleep 5
	@until docker exec study_neo4j cypher-shell -u neo4j -p password "RETURN 1" > /dev/null 2>&1; do \
		echo "Waiting for database."; \
		sleep 2; \
	done
	@echo "Neo4j is ready."
	@echo "Running data generation script."
	@cd neo4j && python3 init_db.py
	@echo "Database is ready to use."
	@echo "Neo4j Browser: http://localhost:7474"

stop-neo4j:
	@echo "Stopping Neo4j container."
	@docker stop study_neo4j 2>/dev/null || true
	@echo "Container stopped."

init-spark:
	@echo "Generating Parquet data files."
	@cd spark && python3 init_db.py
	@echo "Converting to Delta Lake tables."
	@cd spark && python3 init_spark.py
	@echo "Spark data is ready."

clean-spark:
	@echo "Cleaning Spark data."
	@rm -rf spark/data spark/delta
	@echo "Spark data cleaned."

run-es:
	@echo "Stopping existing container if running."
	@docker stop study_elastic 2>/dev/null || true
	@echo "Starting Elasticsearch container."
	@cd elasticsearch && bash run.sh
	@echo "Waiting for Elasticsearch to be ready."
	@sleep 10
	@until curl -s -u elastic:password http://localhost:9200/_cluster/health > /dev/null 2>&1; do \
		echo "Waiting for Elasticsearch."; \
		sleep 2; \
	done
	@echo "Elasticsearch is ready."
	@echo "Running data generation script."
	@cd elasticsearch && python3 init_db.py
	@echo "Elasticsearch is ready to use."
	@echo "Elasticsearch: http://localhost:9200"

stop-es:
	@echo "Stopping Elasticsearch container."
	@docker stop study_elastic 2>/dev/null || true
	@echo "Container stopped."

run-query:
ifndef db
	@echo "Error: db parameter is required"
	@echo "Usage: make run-query db=<pg|mongo|neo4j|spark|es> file=<number>"
	@exit 1
endif
ifndef file
	@echo "Error: file parameter is required"
	@echo "Usage: make run-query db=<pg|mongo|neo4j|spark|es> file=<number>"
	@exit 1
endif
ifeq ($(db),pg)
	@cd postgresql && python3 run_query.py --file $(file)
else ifeq ($(db),mongo)
	@cd mongodb && python3 run_query.py --file $(file)
else ifeq ($(db),neo4j)
	@cd neo4j && python3 run_query.py --file $(file)
else ifeq ($(db),spark)
	@cd spark && python3 run_query.py --file $(file)
else ifeq ($(db),es)
	@cd elasticsearch && python3 run_query.py --file $(file)
else
	@echo "Error: Unknown database '$(db)'"
	@echo "Supported databases: pg, mongo, neo4j, spark, es"
	@exit 1
endif
