.PHONY: run-pg stop-pg run-mongo stop-mongo

run-pg:
	@echo "Stopping existing container if running..."
	@docker stop study_postgres 2>/dev/null || true
	@echo "Starting PostgreSQL container..."
	@cd postgresql && bash run.sh
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3
	@until docker exec study_postgres pg_isready -U postgres > /dev/null 2>&1; do \
		echo "Waiting for database..."; \
		sleep 1; \
	done
	@echo "PostgreSQL is ready!"
	@echo "Running data generation script..."
	@cd postgresql && python3 init_db.py
	@echo "Done! Database is ready to use."

stop-pg:
	@echo "Stopping PostgreSQL container..."
	@docker stop study_postgres 2>/dev/null || true
	@echo "Container stopped."

run-mongo:
	@echo "Stopping existing container if running..."
	@docker stop study_mongo 2>/dev/null || true
	@echo "Starting MongoDB container..."
	@cd mongodb && bash run.sh
	@echo "Waiting for MongoDB to be ready..."
	@sleep 3
	@until docker exec study_mongo mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do \
		echo "Waiting for database..."; \
		sleep 1; \
	done
	@echo "MongoDB is ready!"
	@echo "Running data generation script..."
	@cd mongodb && python3 init_db.py
	@echo "Done! Database is ready to use."

stop-mongo:
	@echo "Stopping MongoDB container..."
	@docker stop study_mongo 2>/dev/null || true
	@echo "Container stopped."
